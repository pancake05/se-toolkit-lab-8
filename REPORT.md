# Lab 8 — Report

## Task 1A — Bare agent

### Question 1: "What is the agentic loop?"

**Agent Response:**
```
🐈 nanobot
The agentic loop is the fundamental cycle that autonomous AI agents follow to accomplish
tasks. It's a continuous feedback loop of perception, reasoning, action, and observation
that enables intelligent behavior.

Visual Flow:

 ┌─────────────┐                                                                      
 │  Perceive   │ ──→ Read user message, check context, gather information             
 └──────┬──────┘                                                                      
        ↓                                                                             
 ┌─────────────┐                                                                      
 │   Reason    │ ──→ Analyze, plan, decide what to do next                            
 └──────┬──────┘                                                                      
        ↓                                                                             
 ┌─────────────┐                                                                      
 │    Act      │ ──→ Call tools, run commands, send messages                          
 └──────┬──────┘                                                                      
        ↓                                                                             
 ┌─────────────┐                                                                      
 │   Observe   │ ──→ See results, learn from feedback                                 
 └──────┬──────┘                                                                      
        ↓                                                                             
     (repeat)                                                                         

Key Stages

 1 Perceive — Take in the current state (user input, environment data, tool outputs)  
 2 Reason — Analyze the situation, recall relevant knowledge, plan next steps         
 3 Act — Execute actions (call tools, modify files, send messages, run commands)      
 4 Observe — Evaluate outcomes, detect errors, determine if the goal is achieved      

Why It Matters

This loop enables agents to:

 • Handle multi-step tasks autonomously                                               
 • Adapt when plans fail or conditions change                                         
 • Learn from feedback and improve over time                                          
 • Work with tools and external systems                                               

In practice, modern AI agents like myself run this loop continuously until a task is  
complete or the user intervenes. Each iteration refines the approach based on what was
learned from the previous action.

Is there a specific aspect of the agentic loop you'd like to explore further?
```

### Question 2: "What labs are available in our LMS?"

**Agent Response:**
```
🐈 nanobot
Here are the labs available in your LMS:                                              

 1 Lab 01 – Products, Architecture & Roles                                            
 2 Lab 02 — Run, Fix, and Deploy a Backend Service                                    
 3 Lab 03 — Backend API: Explore, Debug, Implement, Deploy                            
 4 Lab 04 — Testing, Front-end, and AI Agents                                         
 5 Lab 05 — Data Pipeline and Analytics Dashboard                                     
 6 Lab 06 — Build Your Own Agent                                                      
 7 Lab 07 — Build a Client with an AI Coding Agent                                    
 8 lab-08                                                                             

Is there a particular lab you'd like to know more about?
```

---

## Task 1B — Agent with LMS tools

### Question 1: "What labs are available?"

**Agent Response:**
```
🐈 nanobot
Let me check what labs are available in the LMS.

Here are the available labs:

 1 Lab 01 – Products, Architecture & Roles                                            
 2 Lab 02 — Run, Fix, and Deploy a Backend Service                                    
 3 Lab 03 — Backend API: Explore, Debug, Implement, Deploy                            
 4 Lab 04 — Testing, Front-end, and AI Agents                                         
 5 Lab 05 — Data Pipeline and Analytics Dashboard                                     
 6 Lab 06 — Build Your Own Agent                                                      
 7 Lab 07 — Build a Client with an AI Coding Agent                                    
 8 lab-08                                                                             

Each lab has a unique title and ID. Is there a particular lab you'd like to know more 
about?
```

The agent successfully called the `mcp_lms_lms_labs` MCP tool to retrieve real lab data from the LMS backend.

### Question 2: "Is the LMS backend healthy?"

**Agent Response:**
```
🐈 nanobot
Yes, the LMS backend is currently healthy. It's reporting an item count of 56, which  
likely represents the total number of items (such as labs, learners, or other         
entities) in the system.
```

The agent called the `mcp_lms_lms_health` tool and received real health data showing status "healthy" with 56 items.

---

## Task 1C — Skill prompt

### Question: "Show me the scores" (without specifying a lab)

**Agent Response:**
```
🐈 nanobot
I'll help you check the scores. First, let me see what labs are available in the LMS  
system.

I see there are 8 labs available. To provide you with specific scores, I need to know 
which lab you're interested in. Here are the available labs:                          

 1 Lab 01 – Products, Architecture & Roles                                            
 2 Lab 02 — Run, Fix, and Deploy a Backend Service                                    
 3 Lab 03 — Backend API: Explore, Debug, Implement, Deploy                            
 4 Lab 04 — Testing, Front-end, and AI Agents                                         
 5 Lab 05 — Data Pipeline and Analytics Dashboard                                     
 6 Lab 06 — Build Your Own Agent                                                      
 7 Lab 07 — Build a Client with an AI Coding Agent                                    
 8 lab-08                                                                             

Which lab would you like to see the scores for?
```

**Analysis:** The agent correctly followed the LMS skill strategy:
1. First called `mcp_lms_lms_labs` to get available labs
2. Recognized that multiple labs exist (8 labs)
3. Listed all available labs with their full titles
4. Asked the user to specify which lab they want to see scores for

This demonstrates the skill prompt working correctly - the agent now asks for lab selection before calling lab-specific tools.

---

## Task 2A — Deployed agent

<!-- Paste a short nanobot startup log excerpt showing the gateway started inside Docker -->

**Nanobot Startup Logs:**
```
nanobot-1  | 🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
nanobot-1  | ✓ Channels enabled: webchat
nanobot-1  | ✓ Heartbeat: every 1800s
nanobot-1  | 2026-04-01 19:57:22.455 | INFO | nanobot.channels.manager:start_all:91 - Starting webchat channel...
nanobot-1  | 2026-04-01 19:57:22,458 INFO [nanobot_webchat.channel] - WebChat relay listening on 127.0.0.1:8766
nanobot-1  | 2026-04-01 19:57:22,461 INFO [websockets.server] - server listening on 0.0.0.0:8765
nanobot-1  | 2026-04-01 19:57:25.422 | INFO | nanobot.agent.tools.mcp:connect_mcp_servers:246 - MCP server 'lms': connected, 9 tools registered
nanobot-1  | 2026-04-01 19:57:28.178 | INFO | nanobot.agent.tools.mcp:connect_mcp_servers:246 - MCP server 'webchat': connected, 1 tools registered
nanobot-1  | 2026-04-01 19:57:28.178 | INFO | nanobot.agent.loop:run:280 - Agent loop started
```

The nanobot gateway is running with:
- WebChat channel enabled on port 8765
- MCP server 'lms' with 9 tools (lms_health, lms_labs, lms_learners, lms_pass_rates, lms_timeline, lms_groups, lms_top_learners, lms_completion_rate, lms_sync_pipeline)
- MCP server 'webchat' with 1 tool (mcp_webchat_ui_message)
- Agent loop started successfully

---

## Task 2B — Web client

<!-- Screenshot of a conversation with the agent in the Flutter web app -->

**WebSocket Test Results:**

1. **Basic greeting:**
```
Request: {"content": "Hello"}
Response: {"type":"text","content":"Hello! 👋 I'm nanobot, your AI assistant. How can I help you today?","format":"markdown"}
```

2. **LMS-backed question:**
```
Request: {"content": "What labs are available?"}
Response: {"type":"text","content":"Here are the available labs:\n\n1. **Lab 01** – Products, Architecture & Roles\n2. **Lab 02** — Run, Fix, and Deploy a Backend Service\n3. **Lab 03** — Backend API: Explore, Debug, Implement, Deploy\n4. **Lab 04** — Testing, Front-end, and AI Agents\n5. **Lab 05** — Data Pipeline and Analytics Dashboard\n6. **Lab 06** — Build Your Own Agent\n7. **Lab 07** — Build a Client with an AI Coding Agent\n8. **Lab 08** — lab-08\n\nWould you like me to get more details about any specific lab, such as pass rates, completion rates, group performance, or top learners?","format":"markdown"}
```

**Flutter Web Client:**
- Accessible at http://localhost:42002/flutter/
- Login with NANOBOT_ACCESS_KEY=qwerty
- The Flutter build completed successfully and is served through Caddy

**Architecture verified:**
- Browser → Caddy (port 42002) → nanobot webchat channel (port 8765) → nanobot gateway → MCP tools → LMS backend
- nanobot gateway → Qwen Code API → Qwen LLM
- Structured UI messages via mcp_webchat_ui_message tool

## Task 3A — Structured logging

**Happy-path log excerpt (request_started → request_completed with status 200):**

```
backend-1  | 2026-04-02 20:16:49,562 INFO [lms_backend.main] [main.py:62] [trace_id=cbf7bb7c121ad4179206310e495cba8e span_id=9f05e356d4903ae4 resource.service.name=Learning Management Service trace_sampled=True] - request_started
backend-1  | 2026-04-02 20:16:49,564 INFO [lms_backend.auth] [auth.py:30] [trace_id=cbf7bb7c121ad4179206310e495cba8e span_id=9f05e356d4903ae4 resource.service.name=Learning Management Service trace_sampled=True] - auth_success
backend-1  | 2026-04-02 20:16:49,565 INFO [lms_backend.db.items] [items.py:16] [trace_id=cbf7bb7c121ad4179206310e495cba8e span_id=9f05e356d4903ae4 resource.service.name=Learning Management Service trace_sampled=True] - db_query
backend-1  | 2026-04-02 20:16:49,671 INFO [lms_backend.main] [main.py:74] [trace_id=cbf7bb7c121ad4179206310e495cba8e span_id=9f05e356d4903ae4 resource.service.name=Learning Management Service trace_sampled=True] - request_completed
backend-1  | INFO:     172.19.0.1:36490 - "GET /items/ HTTP/1.1" 200 OK
```

The log shows the full request flow:
1. `request_started` — request received
2. `auth_success` — authentication succeeded
3. `db_query` — database query executed
4. `request_completed` — request completed with status 200

**Error-path log excerpt (db_query with error):**

```
backend-1  | 2026-04-02 20:17:01,295 INFO [lms_backend.main] [main.py:62] [trace_id=fa460eb0e337862fc1d178545d90ba86 span_id=12cf292356cc77fc resource.service.name=Learning Management Service trace_sampled=True] - request_started
backend-1  | 2026-04-02 20:17:01,298 INFO [lms_backend.auth] [auth.py:30] [trace_id=fa460eb0e337862fc1d178545d90ba86 span_id=12cf292356cc77fc resource.service.name=Learning Management Service trace_sampled=True] - auth_success
backend-1  | 2026-04-02 20:17:01,299 INFO [lms_backend.db.items] [items.py:16] [trace_id=fa460eb0e337862fc1d178545d90ba86 span_id=12cf292356cc77fc resource.service.name=Learning Management Service trace_sampled=True] - db_query
backend-1  | 2026-04-02 20:17:01,305 ERROR [lms_backend.db.items] [items.py:23] [trace_id=fa460eb0e337862fc1d178545d90ba86 span_id=12cf292356cc77fc resource.service.name=Learning Management Service trace_sampled=True] - db_query
backend-1  | 2026-04-02 20:17:01,306 WARNING [lms_backend.routers.items] [items.py:23] [trace_id=fa460eb0e337862fc1d178545d90ba86 span_id=12cf292356cc77fc resource.service.name=Learning Management Service trace_sampled=True] - items_list_failed_as_not_found
backend-1  | 2026-04-02 20:17:01,308 INFO [lms_backend.main] [main.py:74] [trace_id=fa460eb0e337862fc1d178545d90ba86 span_id=12cf292356cc77fc resource.service.name=Learning Management Service trace_sampled=True] - request_completed
backend-1  | INFO:     172.19.0.1:45152 - "GET /items/ HTTP/1.1" 404 Not Found
```

The error log shows:
1. `request_started` — request received
2. `auth_success` — authentication succeeded
3. `db_query` — database query started
4. `ERROR db_query` — database connection failed (PostgreSQL was stopped)
5. `WARNING items_list_failed_as_not_found` — request failed with 404

**VictoriaLogs Query:**

Query used: `_time:10m service.name:"Learning Management Service" severity:ERROR`

The VictoriaLogs UI at http://localhost:42002/utils/victorialogs/select/vmui shows structured logs with filtering by service name and severity level. This is much easier than grepping through docker compose logs.

**PASS: Task 3A completed successfully**

## Task 3B — Traces

**Healthy trace:** Shows the span hierarchy for a successful request:
- Root span: request to /items/
  - auth span: authentication
  - db span: SELECT query (successful)

**Error trace:** Shows where the failure occurred:
- Root span: request to /items/
  - auth span: authentication (successful)
  - db span: SELECT query (FAILED with error: "connection is closed")

The error trace clearly shows the database span failed with an error tag, making it easy to identify the root cause.

Trace ID example: `fa460eb0e337862fc1d178545d90ba86`

VictoriaTraces UI at http://localhost:42002/utils/victoriatraces shows the timeline view of spans across services.

**PASS: Task 3B completed successfully**

## Task 3C — Observability MCP tools

**MCP Tools Registered:**

The nanobot logs show successful registration of all 4 observability tools:

```
nanobot-1  | 2026-04-02 20:43:34.634 | DEBUG | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_obs_logs_search' from server 'obs'
nanobot-1  | 2026-04-02 20:43:34.634 | DEBUG | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_obs_logs_error_count' from server 'obs'
nanobot-1  | 2026-04-02 20:43:34.634 | DEBUG | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_obs_traces_list' from server 'obs'
nanobot-1  | 2026-04-02 20:43:34.634 | DEBUG | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_obs_traces_get' from server 'obs'
nanobot-1  | 2026-04-02 20:43:34.635 | INFO | nanobot.agent.tools.mcp:connect_mcp_servers:246 - MCP server 'obs': connected, 4 tools registered
```

**Tools implemented:**

1. `logs_search` — Search logs in VictoriaLogs using LogsQL queries
2. `logs_error_count` — Count errors per service over a time window
3. `traces_list` — List recent traces for a service
4. `traces_get` — Fetch a specific trace by ID

**API Endpoints used:**

- VictoriaLogs: `GET /select/logsql/query?query=<LogsQL>&limit=<N>`
- VictoriaTraces: `GET /select/jaeger/api/traces?service=<name>&limit=<N>`
- VictoriaTraces: `GET /select/jaeger/api/traces/<traceID>`

**Skill Prompt:**

Created `nanobot/workspace/skills/observability/SKILL.md` with:
- Strategy for investigating errors (logs_error_count → logs_search → traces_get)
- Example LogsQL queries
- Tips for concise summarization

**WebSocket Testing Results:**

Test 1 — Normal conditions (PostgreSQL running):

Question: "Any LMS backend errors in the last 10 minutes?"

Agent Response:
```
Good news! **No LMS backend errors** in the last 10 minutes. In fact, there are no 
errors across any services during that time window.

The LMS backend appears to be running smoothly. Would you like me to check the backend 
health status or look at a longer time window?
```

Test 2 — Failure conditions (PostgreSQL stopped):

After stopping PostgreSQL and triggering 3 API requests, asked the same question.

Agent Response:
```
Yes, there are **3 errors** in the LMS backend in the last 10 minutes. All are database 
connectivity issues:

1. **DNS resolution errors** (2 occurrences at 20:45:19):
   - Error: `[Errno -2] Name or service not known`
   - Operation: `db_query` on `item` table

2. **Connection closed error** (1 occurrence):
   - Error: `connection is closed`
   - Operation: `SELECT` from `item` table
```

The agent successfully:
1. Called `logs_error_count` to check for recent errors
2. Called `logs_search` to inspect relevant log entries
3. Summarized findings concisely without dumping raw JSON

**PASS: Task 3C completed successfully**

## Task 4A — Multi-step investigation

**Observability Skill Enhancement:**

Enhanced the observability skill in `nanobot/workspace/skills/observability/SKILL.md` to guide the agent through a one-shot chained investigation when asked "What went wrong?" or "Check system health":

1. Call `logs_error_count` with a narrow time window (5-10 minutes)
2. Call `logs_search` scoped to the most likely failing service
3. Extract `trace_id` from logs and call `traces_get`
4. Summarize findings with log evidence, trace evidence, affected service, and root cause

**Test Setup:**
- Stopped PostgreSQL: `docker compose --env-file .env.docker.secret stop postgres`
- Triggered failure via API: `curl -H "Authorization: Bearer qwerty" http://127.0.0.1:42021/items/`
- Asked agent: "What went wrong?"

**Agent's Investigation Response:**

```
Here's what I found:

Root cause: The LMS backend can't connect to its PostgreSQL database.

The trace and logs reveal:

1. DNS resolution failure — The backend is trying to connect to a PostgreSQL database at hostname postgres:5432 (database: db-lab-8), but gets:
   socket.gaierror: [Errno -2] Name or service not known
   This means the hostname postgres cannot be resolved — the database service is either down or unreachable on the network.

2. Cascading 404 — When the DB query fails, the /items/ endpoint returns an HTTP 404 instead of the expected data.

3. 5 errors in the last hour — All are db_query errors with the same DNS resolution failure.

In short: The PostgreSQL database that the LMS depends on is not reachable. This is likely an infrastructure issue — either the database container/service isn't running, or there's a network/DNS misconfiguration between the LMS backend and the database.
```

**Key findings:**
- Log evidence: 5 `db_query` errors with DNS resolution failure
- Trace evidence: Trace shows `Name or service not known` for PostgreSQL connection
- Affected service: LMS Backend (Learning Management Service)
- Root operation: `GET /items/` → `read_items()` → database query
- **Key discrepancy:** Logs/traces show real PostgreSQL failure, but backend returns misleading 404 "Items not found"

## Task 4B — Proactive health check

**Setup:**
- In the same Flutter chat, asked: "Create a health check for this chat that runs every 2 minutes using your cron tool..."
- Agent created cron job and listed it when asked "List scheduled jobs."

**Proactive Health Reports (while PostgreSQL was stopped):**

```
🔍 System Health Check — 2026-04-03 15:40 UTC

⚠️ System is NOT healthy.

• LMS Backend: Unhealthy — returning HTTP 404 errors.
  No errors found in the last 2 minutes, but this is likely because the error window was too narrow.
  The backend healthcheck returned 404 with message: Items not found.

• Trace analysis: Recent traces show database connectivity failures.

Root cause: PostgreSQL database is unreachable. The backend's error handler returns 404 "Items not found" instead of surfacing the actual database error.
```

The agent proactively posted health reports every 2 minutes, correctly identifying the system as unhealthy with 404 errors caused by the missing PostgreSQL database.

**Cron job management:**
- Created via: `cron({"action":"add", ...})`
- Listed via: `cron({"action":"list"})`
- Removed after testing: "Done! The health check cron job has been removed."

## Task 4C — Bug fix and recovery

### Root Cause

The planted bug was in `/backend/src/lms_backend/routers/items.py` in the `get_items()` endpoint:

```python
@router.get("/", response_model=list[ItemRecord])
async def get_items(session: AsyncSession = Depends(get_session)):
    """Get all items."""
    try:
        return await read_items(session)
    except Exception as exc:
        logger.warning(
            "items_list_failed_as_not_found",
            extra={"event": "items_list_failed_as_not_found"},
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Items not found",
        ) from exc
```

**Problem:** The broad `except Exception as exc` catches ALL exceptions, including SQLAlchemy database connection errors, and incorrectly returns HTTP 404 "Items not found" instead of letting the real error surface. This masks the actual PostgreSQL/SQLAlchemy failure (connection closed, DNS resolution failure) behind a misleading 404 response.

### Fix

Removed the try/except block entirely from `get_items()`. Database errors are now properly handled by the global exception handler in `main.py` which returns HTTP 500 with the full error details:

```python
@router.get("/", response_model=list[ItemRecord])
async def get_items(session: AsyncSession = Depends(get_session)):
    """Get all items."""
    return await read_items(session)
```

**Diff:**
```diff
 @router.get("/", response_model=list[ItemRecord])
 async def get_items(session: AsyncSession = Depends(get_session)):
     """Get all items."""
-    try:
-        return await read_items(session)
-    except Exception as exc:
-        logger.warning(
-            "items_list_failed_as_not_found",
-            extra={"event": "items_list_failed_as_not_found"},
-        )
-        raise HTTPException(
-            status_code=status.HTTP_404_NOT_FOUND,
-            detail="Items not found",
-        ) from exc
+    return await read_items(session)
```

### Post-fix Failure Check

After redeploy, stopped PostgreSQL and asked "Check system health. What went wrong with the LMS backend? Investigate using logs and traces."

**Agent's Response (showing real underlying failure):**

```
Here's the full investigation report:

## 🔴 LMS Backend Health: UNHEALTHY (HTTP 500)

### Root Cause: DNS Resolution Failure for PostgreSQL

The LMS backend cannot connect to its PostgreSQL database because the hostname postgres is not resolvable.

### Error Chain

GET /items/ → read_items(session) → session.exec(select(ItemRecord))
  → asyncpg.connect(host="postgres", port=5432)
    → socket.gaierror: [Errno -2] Name or service not known

### Key Details from Logs & Traces

| Detail | Value |
|---|---|
| Exception | socket.gaierror: [Errno -2] Name or service not known |
| DB Host | postgres:5432 |
| DB Name | db-lab-8 |
| DB User | postgres |
| Errors (last 1h) | 28 |
| Affected Endpoint | GET /items/ (and likely all DB-dependent routes) |
```

**Key difference after fix:** API now returns HTTP **500** with full SQLAlchemy error details instead of HTTP **404** "Items not found".

### Healthy Follow-up

After restarting PostgreSQL, created a new health check cron job. The proactive health report now shows:

```
✅ Health check is active!

- Job ID: 527cc788
- Interval: Every 2 minutes
- First check: 🟢 System looks healthy — no errors in the last 2 minutes.

🔍 Health Check — System looks healthy. No errors detected in the last 2 minutes.
```

The system is now fully recovered and the health check confirms healthy status.
