"""Tool schemas, handlers, and registry for the MCP obs server."""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass
from typing import Any

from mcp.types import Tool
from pydantic import BaseModel, Field

from mcp_obs.observability import ObservabilityClient


class NoArgs(BaseModel):
    """Empty input model for tools that don't need arguments."""


class LogsSearchQuery(BaseModel):
    """Query parameters for logs_search tool."""

    query: str = Field(
        default="_time:10m",
        description="LogsQL query string. Example: '_time:10m service.name:\"Learning Management Service\" severity:ERROR'",
    )
    limit: int = Field(
        default=100,
        ge=1,
        le=1000,
        description="Max log entries to return (default 100, max 1000)",
    )


class LogsErrorCountQuery(BaseModel):
    """Query parameters for logs_error_count tool."""

    time_window: str = Field(
        default="10m",
        description="Time window for counting errors. Example: '10m', '1h', '24h'",
    )
    service: str | None = Field(
        default=None,
        description="Optional service name filter. Example: 'Learning Management Service'",
    )


class TracesListQuery(BaseModel):
    """Query parameters for traces_list tool."""

    service: str = Field(
        default="Learning Management Service",
        description="Service name to filter traces",
    )
    limit: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Max traces to return (default 10, max 100)",
    )


class TracesGetQuery(BaseModel):
    """Query parameters for traces_get tool."""

    trace_id: str = Field(
        description="Trace ID to fetch. Example: 'fa460eb0e337862fc1d178545d90ba86'",
    )


ToolPayload = BaseModel | Sequence[BaseModel] | dict[str, Any]
ToolHandler = Callable[[ObservabilityClient, BaseModel], Awaitable[ToolPayload]]


@dataclass(frozen=True, slots=True)
class ToolSpec:
    """Tool specification."""

    name: str
    description: str
    model: type[BaseModel]
    handler: ToolHandler

    def as_tool(self) -> Tool:
        """Convert to MCP Tool definition."""
        schema = self.model.model_json_schema()
        schema.pop("$defs", None)
        schema.pop("title", None)
        return Tool(name=self.name, description=self.description, inputSchema=schema)


async def _logs_search(client: ObservabilityClient, args: BaseModel) -> ToolPayload:
    """Search logs using LogsQL query."""
    if not isinstance(args, LogsSearchQuery):
        raise TypeError(f"Expected {LogsSearchQuery.__name__}, got {type(args).__name__}")
    return await client.logs_search(query=args.query, limit=args.limit)


async def _logs_error_count(client: ObservabilityClient, args: BaseModel) -> ToolPayload:
    """Count errors per service over a time window."""
    if not isinstance(args, LogsErrorCountQuery):
        raise TypeError(f"Expected {LogsErrorCountQuery.__name__}, got {type(args).__name__}")
    return await client.logs_error_count(
        time_window=args.time_window,
        service=args.service,
    )


async def _traces_list(client: ObservabilityClient, args: BaseModel) -> ToolPayload:
    """List recent traces for a service."""
    if not isinstance(args, TracesListQuery):
        raise TypeError(f"Expected {TracesListQuery.__name__}, got {type(args).__name__}")
    return await client.traces_list(service=args.service, limit=args.limit)


async def _traces_get(client: ObservabilityClient, args: BaseModel) -> ToolPayload:
    """Fetch a specific trace by ID."""
    if not isinstance(args, TracesGetQuery):
        raise TypeError(f"Expected {TracesGetQuery.__name__}, got {type(args).__name__}")
    return await client.traces_get(trace_id=args.trace_id)


TOOL_SPECS = (
    ToolSpec(
        "logs_search",
        "Search logs in VictoriaLogs using LogsQL query. Use for finding specific log entries, errors, or events.",
        LogsSearchQuery,
        _logs_search,
    ),
    ToolSpec(
        "logs_error_count",
        "Count errors per service over a time window. Use to quickly see which services have errors.",
        LogsErrorCountQuery,
        _logs_error_count,
    ),
    ToolSpec(
        "traces_list",
        "List recent traces for a service. Use to find traces for debugging request flows.",
        TracesListQuery,
        _traces_list,
    ),
    ToolSpec(
        "traces_get",
        "Fetch a specific trace by ID. Use to inspect full request flow across services.",
        TracesGetQuery,
        _traces_get,
    ),
)

TOOLS_BY_NAME = {spec.name: spec for spec in TOOL_SPECS}
