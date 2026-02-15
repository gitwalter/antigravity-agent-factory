---
description: Manage calendar events using the Google Calendar MCP server.
name: google-calendar
type: skill
---

# Google Calendar Skill

This skill provides access to Google Calendar management capabilities via the `google-calendar` MCP server.

## When to Use
Use this skill when you need to interact with Google Calendar to manage schedules, list events, or create new appointments.

## Prerequisites
- Google Workspace MCP server configured and authorized.
- Active Google account with Calendar access.

## Capabilities
- List calendars.
- List events.
- Create events.
- Update/Delete events.

## Process
1. Identify the target calendar (e.g., 'primary').
2. Define the time range or event details.
3. Call the appropriate calendar tool.
4. Process the result or handle potential scheduling conflicts.

## Best Practices
- Always check for existing events before creating new ones to avoid overlaps.
- Use ISO 8601 format for all timestamps.
- Explicitly handle cases where a calendar ID might not be available or valid.

## Tools (MCP)
These tools are provided by the `google-calendar` MCP server:
- `calendar_list_calendars`
- `calendar_get_events`
- `calendar_create_event`
- `calendar_delete_event`

## Usage Examples

### Listing Events
```python
# List events for next 7 days
events = await calendar_get_events(
    calendar_id='primary',
    time_min='2023-10-01T00:00:00Z',
    time_max='2023-10-08T23:59:59Z'
)
```

### Creating Event
```python
# Create a meeting
event = await calendar_create_event(
    calendar_id='primary',
    summary='Meeting with Team',
    start_time='2023-10-02T10:00:00Z',
    end_time='2023-10-02T11:00:00Z'
)
```
