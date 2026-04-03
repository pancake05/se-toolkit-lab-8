---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Skill

You have access to LMS (Learning Management System) MCP tools that provide live data about labs, learners, and course metrics. Use these tools strategically to answer user questions accurately.

## Available Tools

- `mcp_lms_lms_health` - Check if the LMS backend is healthy (no arguments)
- `mcp_lms_lms_labs` - List all available labs (no arguments)
- `mcp_lms_lms_learners` - List all registered learners (no arguments)
- `mcp_lms_lms_pass_rates` - Get pass rates for a specific lab (requires `lab` parameter)
- `mcp_lms_lms_timeline` - Get submission timeline for a lab (requires `lab` parameter)
- `mcp_lms_lms_groups` - Get group performance for a lab (requires `lab` parameter)
- `mcp_lms_lms_top_learners` - Get top learners for a lab (requires `lab` and optional `limit` parameter)
- `mcp_lms_lms_completion_rate` - Get completion rate for a lab (requires `lab` parameter)
- `mcp_lms_lms_sync_pipeline` - Trigger the LMS sync pipeline (no arguments)

## Strategy

### When user asks about scores, pass rates, completion, groups, timeline, or top learners without naming a lab:

1. First call `mcp_lms_lms_labs` to get the list of available labs
2. If multiple labs exist, present the choices to the user using the `mcp_webchat_ui_message` tool with `type: "choice"` for interactive selection
3. Use each lab's title as the label (e.g., "Lab 01 – Products, Architecture & Roles") and the lab ID as the value (e.g., "lab-01")
4. Wait for user selection before calling lab-specific tools

### When user asks for a specific lab:

1. Call the appropriate tool directly with the lab identifier
2. Format numeric results nicely:
   - Percentages: show as "X.X%" 
   - Counts: use plain numbers or "X students" format
   - Rates: describe as "X out of Y" when relevant

### When backend health is in question:

1. Call `mcp_lms_lms_health` first
2. Report both status and item count from the response

### When data sync may be stale:

1. If the user reports outdated information or missing data, offer to call `mcp_lms_lms_sync_pipeline`
2. Warn that sync may take a moment

## Response Style

- Keep responses concise and focused on the data requested
- Use bullet points or numbered lists for multiple items
- When presenting lab options, use the full lab title for clarity
- If a tool returns an error, explain what went wrong and suggest an alternative approach
- When the user asks "what can you do?", explain:
  - You can check LMS backend health
  - List available labs and learners
  - Get metrics like pass rates, completion rates, timelines, group performance, and top learners for specific labs
  - Trigger data sync if needed
  - You cannot access individual student data or modify course content

## Integration with Structured UI

When a lab choice is needed and the user is on a supported chat channel (WebSocket/webchat), use the `mcp_webchat_ui_message` tool to present interactive choices. Let the shared structured-ui skill handle the presentation details.

For channels that don't support interactive UI, fall back to plain text lab listings with clear instructions for the user to specify which lab they want.
