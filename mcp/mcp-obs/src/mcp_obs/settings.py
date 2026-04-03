"""Settings for the MCP obs server."""

import os
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for VictoriaLogs and VictoriaTraces connections."""

    victorialogs_url: str = Field(
        default="http://victorialogs:9428",
        description="VictoriaLogs HTTP API URL",
    )
    victoriatraces_url: str = Field(
        default="http://victoriatraces:10428",
        description="VictoriaTraces HTTP API URL (Jaeger-compatible)",
    )


def resolve_settings(
    victorialogs_url: str | None = None,
    victoriatraces_url: str | None = None,
) -> Settings:
    """Resolve settings from environment or arguments."""
    # Check environment variables first
    env_vl = os.environ.get("NANOBOT_VICTORIALOGS_URL")
    env_vt = os.environ.get("NANOBOT_VICTORIATRACES_URL")

    return Settings(
        victorialogs_url=victorialogs_url or env_vl or "http://victorialogs:9428",
        victoriatraces_url=victoriatraces_url or env_vt or "http://victoriatraces:10428",
    )
