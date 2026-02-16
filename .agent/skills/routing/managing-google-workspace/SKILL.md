---
description: Tactical Blueprint for managing Google Workspace (Drive, Gmail, Calendar).
  Focuses on prescriptive search, organization, and high-fidelity communication.
name: managing-google-workspace
type: skill
---
# Capability Manifest: Google Workspace Mastery

This blueprint provides the **procedural truth** for managing the user's digital ecosystem with precision and beauty.

## Process

Follow these procedures to interact with Google Workspace components:

### Procedure 1: Precise Information Retrieval (Drive & Gmail)
1.  **Query Decomposition**: Never run a broad search. Use specific operators:
    - *Gmail*: `from:name`, `has:attachment`, `after:YYYY/MM/DD`.
    - *Drive*: `name contains 'X'`, `mimeType = 'application/pdf'`.
2.  **Metadata Audit**: When retrieving information, always check the `modifiedTime` and `lastModifyingUser` to ensure you are viewing the current Truth.

### Procedure 2: Axiomatic Scheduling (Calendar)
1.  **Conflict Check**: Run `list_events` for the target day *and* the days surrounding it to identify context.
2.  **Buffer Implementation**: When creating an event, check the end time of the previous event. If the gap is <15m, suggest a later start time.
3.  **Description Truth**: Every event must have a clear description, a location (or link), and relevant context attached.

### Procedure 3: High-Fidelity Communication (Gmail)
1.  **Contextual Grounding**: Before drafting an email, search the thread history to maintain continuity.
2.  **Drafting Gate**:
    - Use clear, action-oriented subject lines.
    - Use professional, context-aware greetings.
    - Include a clear "Call to Action" or "Closure Statement."
3.  **Attachment Protocol**: Use `gmail.send_email` with the `attachments` argument to include local files or drive documents (after downloading).
4.  **Verification**: For sensitive emails, present the draft alongside a "Context Summary" (e.g., "This email addresses the points raised by X on Tuesday regarding Y").

## Process (Fail-State & Recovery)

| Symptom | Probable Cause | Recovery Operation |
| :--- | :--- | :--- |
| **Search Zero-Result** | Too restrictive query or expired token. | Broaden the search; check for typos in the query; trigger a permission/auth check if necessary. |
| **Event Conflict** | Simultaneous booking. | Propose "Alternative Intelligence": Provide 3 distinct time slots that satisfy all axioms (including buffers). |
| **Auth Error** | OAuth key missing or expired. | Ensure `gcp-oauth.keys.json` is in the workspace root and re-authenticate via browser. |

## Prerequisites

| Action | Tool / Command |
| :--- | :--- |
| Find Email | `gmail.search_emails(query="...")` |
| Send Email | `gmail.send_email(to="...", subject="...", content="...", attachments=["..."])` |
| Book Meeting | `google-calendar.list_events(...)` |
| Organize File | `gdrive.list_files(q="...")` |

## When to Use
Use this blueprint whenever managing personal or professional operations involving the Google Workspace ecosystem. It is the authoritative source for "How we assist" vs "What Google Workspace is."

## Best Practices
- Follow the system axioms (A1-A5)
- Ensure all changes are verifiable
- Maintain clean label structures using `gmail.create_label` and `gmail.list_email_labels`.
