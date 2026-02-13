---
name: google-calendar
description: Manage calendar events using the Google Calendar MCP server.
type: skill
---

# Google Calendar Skill

This skill provides access to Google Calendar management capabilities via the `google-calendar` MCP server.

## Capabilities
- List calendars.
- List events.
- Create events.
- Update/Delete events.

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
