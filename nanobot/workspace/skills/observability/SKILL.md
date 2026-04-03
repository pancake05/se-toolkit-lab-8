# Observability Skill

## Purpose

This skill teaches the agent how to investigate errors and issues using logs and traces.

## Available Tools

You have access to these observability tools:

- `logs_search` — Search logs in VictoriaLogs using LogsQL queries
- `logs_error_count` — Count errors per service over a time window
- `traces_list` — List recent traces for a service
- `traces_get` — Fetch a specific trace by ID

## Strategy

### When the user asks "What went wrong?" or "Check system health":

Perform a **one-shot chained investigation** following this exact flow:

1. **Call `logs_error_count`** with a narrow time window (`minutes=5` or `minutes=10`).
   - This quickly shows which services have recent errors and how many.
   - If the user mentioned a specific service (e.g., "LMS backend"), filter by it.

2. **Call `logs_search`** scoped to the most likely failing service.
   - Use query: `_time:10m service.name:"Learning Management Service" severity:ERROR`
   - Look for `trace_id` fields in the log entries.
   - Identify the failing operation (e.g., `db_query`, `items_list_failed_as_not_found`).

3. **Extract the most recent `trace_id`** from the error logs and call `traces_get`.
   - If `traces_get` needs a trace_id parameter, use the one from the logs.
   - If you don't have a trace_id, call `traces_list` first to get recent traces for the service.
   - The trace shows the full request flow and exactly where it failed.

4. **Summarize findings in one coherent response** — NEVER dump raw JSON.
   - State the affected service name.
   - State the root failing operation.
   - Cite at least one specific error log evidence (quote the error message).
   - Cate at least one matching trace evidence (mention the trace_id and what it shows).
   - Explain the discrepancy if logs/traces show a different error than what the API returned.

### Example Investigation Response

"The **LMS backend** (Learning Management Service) is failing. Here's what I found:

**Log evidence:** 3 errors in the last 10 minutes. The logs show database connection failures — specifically `[Errno -2] Name or service not known` during `db_query` operations on the `item` table. There are also `WARNING` entries for `items_list_failed_as_not_found`, indicating the API returns 404 'Items not found' when the real issue is a database connection failure.

**Trace evidence:** Trace `fa460eb0e337862fc1d178545d90ba86` confirms the failure path — the auth span succeeds, but the db_query span fails with error 'connection is closed'. The request to GET /items/ is being misreported as 404 instead of surfacing the actual database error.

**Root cause:** The PostgreSQL database is unreachable. The backend's error handler catches the database exception but incorrectly returns HTTP 404 'Items not found' instead of a 500 Internal Server Error with the real database failure details."

**If no errors found:** "The system looks healthy. No recent backend errors detected in the last 10 minutes."

## Example Queries

### LogsQL query patterns:

- Recent errors in LMS: `_time:10m service.name:"Learning Management Service" severity:ERROR`
- All errors: `_time:10m severity:ERROR`
- Specific event: `_time:10m event:db_query severity:ERROR`
- Last hour: `_time:1h service.name:"Learning Management Service"`

## Tips

- Always use narrow time windows (5m, 10m) to avoid unrelated historical data
- Filter by service name when the user specifies one
- Look for `trace_id` in logs to correlate with distributed traces
- Traces show timing — identify slow or failing steps
- Don't overwhelm the user with raw JSON; summarize key findings
- When asked "What went wrong?", always chain: error_count → logs_search → traces_get → summary
