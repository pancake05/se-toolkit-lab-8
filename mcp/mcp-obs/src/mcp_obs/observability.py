"""Client for VictoriaLogs and VictoriaTraces HTTP APIs."""

from __future__ import annotations

import json
import logging
from typing import Any

import httpx
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class LogEntry(BaseModel):
    """Single log entry from VictoriaLogs."""

    time_: str | None = Field(default=None, alias="_time", description="Timestamp")
    message: str | None = Field(default=None, description="Log message")
    level: str | None = Field(default=None, description="Log level")
    service: str | None = Field(default=None, description="Service name")
    event: str | None = Field(default=None, description="Event name")
    trace_id: str | None = Field(default=None, description="Trace ID")
    span_id: str | None = Field(default=None, description="Span ID")
    raw: dict[str, Any] = Field(default_factory=dict, description="Raw log data")


class ErrorCount(BaseModel):
    """Error count for a service."""

    service: str = Field(description="Service name")
    count: int = Field(description="Number of errors")
    time_window: str = Field(description="Time window used for counting")


class TraceSummary(BaseModel):
    """Summary of a trace."""

    trace_id: str = Field(description="Trace ID")
    service: str = Field(description="Primary service name")
    start_time: str = Field(description="Trace start time")
    duration_ms: int = Field(description="Trace duration in milliseconds")
    span_count: int = Field(description="Number of spans")
    error: bool = Field(default=False, description="Whether trace contains errors")


class TraceDetail(BaseModel):
    """Detailed trace information."""

    trace_id: str = Field(description="Trace ID")
    spans: list[dict[str, Any]] = Field(default_factory=list, description="List of spans")
    services: list[str] = Field(default_factory=list, description="Services involved")
    duration_ms: int = Field(default=0, description="Total duration")
    error: bool = Field(default=False, description="Has errors")


class ObservabilityClient:
    """HTTP client for VictoriaLogs and VictoriaTraces APIs."""

    def __init__(
        self,
        victorialogs_url: str,
        victoriatraces_url: str,
    ):
        self.victorialogs_url = victorialogs_url.rstrip("/")
        self.victoriatraces_url = victoriatraces_url.rstrip("/")
        self._http_client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> ObservabilityClient:
        self._http_client = httpx.AsyncClient(timeout=30.0)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._http_client:
            await self._http_client.aclose()

    @property
    def http_client(self) -> httpx.AsyncClient:
        if self._http_client is None:
            raise RuntimeError("Client not initialized. Use async context manager.")
        return self._http_client

    async def logs_search(
        self,
        query: str,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """
        Search logs in VictoriaLogs using LogsQL.

        VictoriaLogs query API: GET /select/logsql/query?query=<LogsQL>&limit=<N>
        Example query: '_time:10m service.name:"Learning Management Service" severity:ERROR'
        """
        url = f"{self.victorialogs_url}/select/logsql/query"
        params = {"query": query, "limit": limit}

        try:
            # VictoriaLogs expects GET request with query params
            response = await self.http_client.get(url, params=params)
            response.raise_for_status()
            
            # VictoriaLogs returns newline-delimited JSON
            lines = response.text.strip().split('\n')
            result = []
            for line in lines:
                if line.strip():
                    try:
                        result.append(json.loads(line))
                    except json.JSONDecodeError:
                        result.append({"raw": line})
            return result[:limit]
        except httpx.HTTPError as e:
            logger.error(f"VictoriaLogs search failed: {e}")
            return [{"error": str(e), "query": query}]
        except Exception as e:
            logger.error(f"VictoriaLogs search error: {e}")
            return [{"error": str(e)}]

    async def logs_error_count(
        self,
        time_window: str = "10m",
        service: str | None = None,
    ) -> list[ErrorCount]:
        """
        Count errors per service over a time window.

        Uses LogsQL to count entries with severity:ERROR or level:error.
        """
        # Build query for error counting
        if service:
            base_query = f'_time:{time_window} service.name:"{service}" (severity:ERROR OR level:error)'
        else:
            base_query = f'_time:{time_window} (severity:ERROR OR level:error)'

        # First, get all error logs
        logs = await self.logs_search(query=base_query, limit=10000)

        # Count by service
        service_counts: dict[str, int] = {}
        for log in logs:
            if isinstance(log, dict):
                # Try different field names for service
                svc = (
                    log.get("service.name")
                    or log.get("service")
                    or log.get("serviceName")
                    or log.get("resource.service.name")
                    or "unknown"
                )
                service_counts[svc] = service_counts.get(svc, 0) + 1

        # Convert to ErrorCount list
        result = [
            ErrorCount(service=svc, count=count, time_window=time_window)
            for svc, count in sorted(service_counts.items(), key=lambda x: -x[1])
        ]

        if not result:
            result = [
                ErrorCount(
                    service=service or "all",
                    count=0,
                    time_window=time_window,
                )
            ]

        return result

    async def traces_list(
        self,
        service: str = "Learning Management Service",
        limit: int = 10,
    ) -> list[TraceSummary]:
        """
        List recent traces for a service.

        Uses Jaeger-compatible API: GET /select/jaeger/api/traces?service=<name>&limit=<N>
        """
        url = f"{self.victoriatraces_url}/select/jaeger/api/traces"
        params = {"service": service, "limit": limit}

        try:
            response = await self.http_client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # Jaeger API returns {"data": [...traces...]}
            traces_data = data.get("data", [])
            if not isinstance(traces_data, list):
                traces_data = [traces_data] if traces_data else []

            result = []
            for trace in traces_data[:limit]:
                if not isinstance(trace, dict):
                    continue

                trace_id = trace.get("traceID", "unknown")
                spans = trace.get("spans", [])

                # Calculate duration
                duration_ms = 0
                if spans:
                    start_times = [
                        s.get("startTime", 0) for s in spans if isinstance(s, dict)
                    ]
                    end_times = [
                        s.get("startTime", 0) + s.get("duration", 0)
                        for s in spans
                        if isinstance(s, dict)
                    ]
                    if start_times and end_times:
                        duration_ms = int((max(end_times) - min(start_times)) / 1000)

                # Check for errors
                has_error = False
                for span in spans:
                    if isinstance(span, dict):
                        tags = span.get("tags", [])
                        for tag in tags:
                            if (
                                isinstance(tag, dict)
                                and tag.get("key") == "error"
                                and tag.get("value")
                            ):
                                has_error = True
                                break

                result.append(
                    TraceSummary(
                        trace_id=trace_id,
                        service=service,
                        start_time=trace.get("startTime", ""),
                        duration_ms=duration_ms,
                        span_count=len(spans),
                        error=has_error,
                    )
                )

            return result

        except httpx.HTTPError as e:
            logger.error(f"VictoriaTraces list failed: {e}")
            return [
                TraceSummary(
                    trace_id="error",
                    service=service,
                    start_time="",
                    duration_ms=0,
                    span_count=0,
                    error=True,
                )
            ]
        except Exception as e:
            logger.error(f"VictoriaTraces list error: {e}")
            return []

    async def traces_get(self, trace_id: str) -> TraceDetail:
        """
        Fetch a specific trace by ID.

        Uses Jaeger-compatible API: GET /select/jaeger/api/traces/<traceID>
        """
        url = f"{self.victoriatraces_url}/select/jaeger/api/traces/{trace_id}"

        try:
            response = await self.http_client.get(url)
            response.raise_for_status()
            data = response.json()

            # Jaeger API returns {"data": [...traces...]}
            traces_data = data.get("data", [])
            if not traces_data:
                return TraceDetail(
                    trace_id=trace_id,
                    spans=[],
                    services=[],
                    duration_ms=0,
                    error=False,
                )

            trace = traces_data[0] if isinstance(traces_data, list) else traces_data
            if not isinstance(trace, dict):
                return TraceDetail(
                    trace_id=trace_id,
                    spans=[],
                    services=[],
                    duration_ms=0,
                    error=False,
                )

            spans = trace.get("spans", [])
            services = list(
                {
                    span.get("process", {}).get("serviceName", "unknown")
                    for span in spans
                    if isinstance(span, dict)
                }
            )

            # Calculate duration
            duration_ms = 0
            if spans:
                start_times = [
                    s.get("startTime", 0) for s in spans if isinstance(s, dict)
                ]
                end_times = [
                    s.get("startTime", 0) + s.get("duration", 0)
                    for s in spans
                    if isinstance(s, dict)
                ]
                if start_times and end_times:
                    duration_ms = int((max(end_times) - min(start_times)) / 1000)

            # Check for errors
            has_error = False
            for span in spans:
                if isinstance(span, dict):
                    tags = span.get("tags", [])
                    for tag in tags:
                        if (
                            isinstance(tag, dict)
                            and tag.get("key") == "error"
                            and tag.get("value")
                        ):
                            has_error = True
                            break

            return TraceDetail(
                trace_id=trace_id,
                spans=spans,
                services=services,
                duration_ms=duration_ms,
                error=has_error,
            )

        except httpx.HTTPError as e:
            logger.error(f"VictoriaTraces get failed: {e}")
            return TraceDetail(
                trace_id=trace_id,
                spans=[],
                services=[],
                duration_ms=0,
                error=True,
            )
        except Exception as e:
            logger.error(f"VictoriaTraces get error: {e}")
            return TraceDetail(
                trace_id=trace_id,
                spans=[],
                services=[],
                duration_ms=0,
                error=False,
            )
