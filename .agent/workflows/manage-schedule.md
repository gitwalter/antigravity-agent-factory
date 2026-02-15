---
## Overview

description: Manage daily schedule and communications
---

# Manage Schedule Workflow

This workflow demonstrates how the Personal Assistant agent can check the schedule and send emails.

**Version:** 1.0.0

## Trigger Conditions

This workflow is activated when:
- User asks to check their schedule
- Schedule summary requested
- Email summary of calendar events needed

**Trigger Examples:**
- "Check my schedule for today"
- "Summarize my meetings and email me"

## Steps

1.  **Check Calendar**: The agent checks the primary calendar for today's events.
    ```python
    # Pseudo-code for agent action
    events = calendar_get_events(calendar_id='primary', time_min=NOW, time_max=END_OF_DAY)
    ```

2.  **Summarize Schedule**: The agent summarizes the events found.

3.  **Send Summary Email** (Optional): If requested, the agent sends an email with the schedule summary.
    ```python
    # Pseudo-code for agent action
    run_command("python scripts/send_gmail.py --to user@example.com --subject 'Daily Schedule' --body 'Here is your schedule...'")
    ```

## Usage
- Ask: "Check my schedule for today and email me a summary"
- The agent will use `google-calendar` skill to get events and `send-email` skill to send the email.


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...
