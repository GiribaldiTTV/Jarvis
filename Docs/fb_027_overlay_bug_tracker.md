# FB-027 Overlay Bug Tracker

## Purpose

This document is a branch-focused working tracker for active and very recently closed bugs on:

- `feature/fb-027-overlay-usability`

It exists to support one-bug-at-a-time follow-through on this branch without turning branch-local bug work into:

- backlog management
- repo-wide bug governance
- PR or release readiness output

This file is a working truth surface for the active branch.
It is not a replacement for:

- `docs/feature_backlog.md`
- `docs/user_test_summary_guidance.md`
- version closeouts
- future milestone rebaseline docs

## Status Meanings

- `Confirmed Active`
- `Suspected / Not Yet Confirmed`
- `Fixed Pending User Confirmation`
- `Closed`

Use these states to keep bug work explicit and narrow.

## Evidence Normalization

The latest desktop:

- `C:\Users\anden\OneDrive\Desktop\User Test Summary.txt`

is still useful evidence, but it reflects an older mirroring-focused retest and does not fully represent the latest branch truth by itself.

Current normalized branch truth is:

- first-open immediate typing from both overlay hotkeys is working
- the mirrored-text bug is confirmed fixed
- the no-click `Enter` / desktop-launch leakage bug is confirmed active
- `Shift+Home` line-clearing convenience remains a later non-bug enhancement

This tracker should prefer the newest recoverable evidence, including:

- the latest returned desktop `User Test Summary.txt`
- later direct live test results preserved in chat
- branch-local code and helper state

## Current-Slice Active Bugs

### BUG-001 No-Click Enter Leaks To Desktop Selection

- Status:
  - `Confirmed Active`
- Evidence source:
  - direct live user testing on `2026-04-07`
  - current branch code path inspection
- Exact reproduction summary:
  1. launch Nexus from the normal desktop shortcut
  2. select a harmless desktop or File Explorer item first
  3. open the NCP with `Ctrl+Alt+Home` or `Ctrl+Alt+1`
  4. do not click the NCP input box
  5. type either:
     - a guaranteed zero-match string such as `aaaaazzzz`
     - or a valid command such as `open file explorer`
  6. press `Enter`
- Observed results:
  - harmless desktop text file opened once
  - `OBS` opened multiple times
  - `Wave Link` opened
  - `AIDA64` attempted to open
  - in one confirm-path run, the NCP showed the confirm state while external desktop launch still happened
  - in a zero-match run, the NCP showed `No saved action or alias matched that request.` while an external app still launched
- Current leading hypothesis:
  - the no-click entry path still uses fallback global key forwarding
  - fallback forwarding can mirror typed keys into the NCP without truly suppressing desktop or File Explorer key ownership underneath
  - leaked printable text may change which desktop item is selected before leaked `Enter` opens it
  - confirm-path `Enter` may also be vulnerable when the overlay still does not truly own the key event
- What is still unknown:
  - whether confirm-path failure is only key leakage or partly capture-expiry timing too
  - whether leaked printable text is always present or only intermittent before leaked `Enter`
- Next narrow move:
  - add explicit submit-path tracing for:
    - fallback submit received
    - local submit received
    - `submit()` result
    - foreground window ownership at submit time
  - reproduce with a controlled harmless selected target
  - patch no-click submit containment without widening into unrelated interaction changes

### BUG-002 Caret Keeps Flashing After Focus Leaves The NCP

- Status:
  - `Confirmed Active`
- Evidence source:
  - direct user report after mirrored typing was already closed
- Exact reproduction summary:
  1. open the NCP
  2. type or otherwise engage the entry path
  3. click into another app or control
  4. observe that the caret continues flashing as though the NCP is still ready for typing
- Observed results:
  - typing capture does not necessarily continue
  - but the visual typing-ready signal remains active
- Current leading hypothesis:
  - visual typing-ready state and real input ownership are not fully synchronized after focus leaves the NCP
- What is still unknown:
  - whether this is purely visual
  - or whether it occasionally correlates with residual fallback-capture state
- Next narrow move:
  - inspect visual-state updates alongside the click-away and focus-loss path
  - fix visual-state sync only after the no-click `Enter` bug is stable, unless shared evidence proves the same root cause

## Recently Closed On This Branch

### BUG-003 Mirrored Typing After Focus Moves Elsewhere

- Status:
  - `Closed`
- Evidence source:
  - direct user confirmation after the no-click reproduction path was corrected
- Exact reproduction summary:
  1. open the NCP
  2. type into it
  3. click into another app
  4. type there
  5. text previously mirrored back into the NCP
- Current closure understanding:
  - no-click outside-click handling now stops the mirrored-text path reliably enough to treat it as closed on this branch
- Why it stays in this file:
  - the active `Enter` leak may share adjacent ownership logic, so keeping the closed bug visible helps avoid reopening it silently

### BUG-004 First-Open Typing Required Manual Click Or Cut Off Mid-Entry

- Status:
  - `Closed`
- Evidence source:
  - later direct user confirmation
- Exact reproduction summary:
  1. open the NCP with `Ctrl+Alt+Home` or `Ctrl+Alt+1`
  2. begin typing immediately without a click
  3. older branch state sometimes dropped characters, stopped mid-entry, or required manual click
- Current closure understanding:
  - first-open immediate typing now works from both overlay hotkeys
  - later random cutoff behavior was also confirmed closed in direct testing
- Why it stays in this file:
  - this branch has already passed through several input-ownership fixes, so keeping the closed path visible helps future drift checks

## Suspected / Not Yet Confirmed

- none currently separated from the active bugs above

If a new bug is not yet reproducible enough to count as `Confirmed Active`, add it here first rather than silently upgrading it into active bug work.

## Later Ideas / Non-Bug Follow-Through

- `Shift+Home` line-clearing / line-selection convenience

This is a later usability idea, not a current-slice bug.
Do not fold it into active bug-fix work unless separately approved.

## Merge / Retirement Guidance

This tracker should remain branch-local while:

- the branch is active
- one-bug-at-a-time follow-through is still happening
- branch-local bug state would otherwise be lost between passes

After merge, preferred handling is:

- retire it if all tracked items are closed and no longer needed
- or preserve only if it still provides useful audit context for a closeout, rebaseline, or post-merge follow-through

Default recommendation:

- do not turn this file into a permanent repo-wide bug database
- treat it as a useful branch working artifact first
