# Antigravity Session Instructions & Behavioral Rules

These core rules govern all operations in this workspace. Follow them strictly:

## 1. End-to-End Flow Tracing
Whenever asked to make a change, do NOT stop at the surface level of the request.
- Always trace the entire flow of the code change end to end.
- Example: If asked to add or remove a button or UI element from a screen, trace where it is placed on the frontend, how it is styled, what component and state manage it, which handler and function it calls, what backend/API route/database operation is triggered, and how errors/responses are handled.

## 2. Session Audit History Document
Maintain a single markdown document at `documentation/session-audit-log.md` at the root level:
- Record an accurate, detailed explanation of every single action, decision, and code modification made during this session.
- Document the rationale, exact files touched, and technical context.
- Update this document immediately after every single completed action item.

## 3. Strict Scope Adherence
Strictly limit all work to the exact scope requested:
- If asked to fix or modify a screen/component, only touch what was specifically requested.
- Clearly state in the chat what was done.
- **NO unrequested actions**:
  - Do NOT commit to git without explicit user permission.
  - Do NOT push to GitHub without explicit user permission.
  - Do NOT run tests unless explicitly requested.

## 4. Cautious Escalation on Hidden Complexity / Blockers
If a requested task or issue reveals blockers, dependencies, edge cases, or complexity beyond the scope of the original request:
- **STOP immediately**.
- Do NOT make assumptions or implement proactive speculative workarounds.
- Report the full context, technical implications, and trade-offs to the user.
- Wait for user instructions before proceeding.
- Prioritize thoroughness and caution over speed or autonomy.
