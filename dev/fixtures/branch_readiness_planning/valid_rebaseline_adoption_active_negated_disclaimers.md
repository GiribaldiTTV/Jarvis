# Valid Rebaseline Adoption Active Negated Disclaimers Fixture

RAR Stage: RAR3 USER Review Gate remains active for issue-candidate review.
Trigger Reason: origin/main merged UIREF standards affecting existing owned UI surfaces.
Source-Truth Files Loaded: Docs/Main.md, Docs/phase_governance.md, Docs/branch_plans/README.md, Docs/nexus_vision.md, Docs/family_visions/FAM-002_desktop_interface.md, and Docs/ui_reference_catalog/index.md.
Incoming Standard / Change Summary: merged standards require deterministic USER packet evidence and non-green active gate wording.
Merged Standard Source: origin/main governance merge containing RAR and UIREF updates.
Rebaseline / Re-entry Event: FAM-006 branch rebaseline after governance merge.
Current Branch Implementation Inventory: current branch touched Recording Studio controls and records historical HUD evidence.
Owned Surface Inventory: HUD Dashboard, Recording Studio, and Log Viewer Studio surfaces.
Affected File Inventory: desktop/desktop_renderer.py and FAM-006 validation helper surfaces.
Affected Surface Inventory: Recording Studio window controls, Log Viewer Studio controls, HUD Dashboard close control, buttons, rows, and scrollbars.
Affected Branch Artifacts: active external branch plan, refreshed UTS evidence, screenshots, and current USER packet.
Affected Product Surfaces: FAM-006 HUD and studio windows that USER sees.
Implemented / Touched UI-UX Surfaces: Recording Studio controls, Log Viewer Studio controls, folder action buttons, and status text.
Implemented / Touched Runtime-Backend Surfaces: recording state display, folder-open status display, and local log path truth mapping.
Affected Proof Claims: current branch claims compact studio controls are repaired; historical HUD green claims remain unproven under UIREF.
Merged Standard Comparison Result: current studio controls require reference-derived parity proof; historical HUD close treatment becomes an issue candidate.
Frontend / Backend Contract Findings: studio status rows map to local recording and folder state.
Reference / Template / Primitive Classification: Reference-Derived Implementation because no approved shared primitive or implementation template is promoted.
Accepted Reference Set / Comparative Synthesis: UIREF-001, UIREF-002, FAM-002 presentation grammar, and AI Control Center reference seed define invariant control shape, glow, placement, and state behavior.
Accepted Reference / Template / Primitive Comparator Matrix: table below compares window-control and button classes against accepted reference grammar.
UI Reference / Template / Shared Primitive Dependency: UIREF records are accepted references, not implementation templates or shared primitives.
NDAI Product Experience Contract Comparison: deterministic state text, intuitive control placement, immersive Nexus chrome, predictable hover/focus behavior, reliable recovery routing, and consistent same-class control appearance are compared.
UI Element Inventory: window control cluster, primary button, secondary button, status row, card boundary, scrollbar, and folder-action button groups.
Backend / State Ownership Trace: Recording state owner is FAM-006 local runtime; folder-open status owner is local filesystem action result; AI/provider state is out of scope.
Screenshot / Video / Contact-Sheet Evidence: screenshot/contact-sheet proof path is named in the USER packet; proof gaps are explicit for historical HUD issues.
Visual Element / Element-Group Inspection Ledger: studio controls are CONFORMING by current evidence; historical HUD close control is ISSUE CANDIDATE pending USER review.
Vision-To-Proof Matrix: selected FAM-006 visible controls map from Project Vision, FAM-002, UIREF-001, UIREF-002, implementation code, focused screenshot evidence, and USER decision path.
Scope Coverage Manifest: current branch studio surfaces are inventoried; previous HUD Dashboard drift is separated into historical issue candidate scope.
Owned-Surface Nonconformance Ledger: current branch rows are CONFORMING; prior HUD Dashboard large close treatment is ISSUE CANDIDATE and not claimed green.
Current Branch Repair Candidates: none before USER review because current studio control evidence is classified separately from prior HUD issue candidates.
Previous / Historical Branch Issue Candidates: Issue Candidate F6-HIST-001 records HUD Dashboard top-level close-control review against UIREF-002.
Current Violation Findings: no current branch nonconformance is claimed green; historical HUD issue remains USER-reviewed issue candidate.
Issue-Candidate Table: Issue Candidate F6-HIST-001 is pending USER review; GitHub issue mutation approved? No.
Issue Candidate Disposition: Issue Candidate F6-HIST-001 remains pending USER review and GitHub issue mutation is not approved.
Repair / Waiver / Defer / Route Decision Table: USER review pending for Issue Candidate F6-HIST-001; approving the issue candidate authorizes issue creation only if USER separately approves that GitHub action.
Adoption Disposition: Not all adoption checks are green because issue-candidate review remains pending.
Repair / Waiver / Blocker: RAR USER Review Gate remains active until USER reviews issue candidates or waives them; normal phase progression remains blocked.
Validation Summary: branch-readiness fixture validation, branch governance validation, packet validation, and focused visual proof review are required evidence layers.
USER Packet Path: C:\Nexus USER\FAM-006.
USER Packet ZIP Path: timestamped upload packet at `C:\Nexus USER\FAM-006-20260620-120000.zip`.
Next Legal Phase: RAR3 USER Review Gate remains active until USER reviews issue candidates or waives them.
Exact Next USER Decision: USER reviews RAR issue candidates; normal phase progression is not authorized; this does not authorize PR creation, merge, or release.
No Repo Live-State Tracking: active RAR rows stay in C:\Nexus Governance State, USER packets, helper output, Codex digest, or evidence roots; repo docs keep durable rules only.

| Surface | Element Group | Source File / Code Region | Backend / State Owner | Rendered Evidence | Accepted Reference | Visual Match | Behavior Match | Status | Defect / Gap | Next Legal Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Recording Studio | Window control cluster | desktop/desktop_renderer.py studio controls | FAM-006 desktop renderer | focused screenshot packet | UIREF-002 and AI Control Center seed | Match | Match | CONFORMING | None | Continue after USER packet review |
| HUD Dashboard | Top-level close control | historical HUD shell region | FAM-006 HUD owner | USER screenshot evidence | UIREF-002 and AI Control Center seed | Mismatch | Unproven | ISSUE CANDIDATE | Historical large close treatment needs review | USER issue-candidate review |

| Element Class | Implementation Authority | Accepted Reference Set | Invariant Traits | Feature-Specific Traits | Target Surface | Primitive/Template/Reference-Derived/Exception | Evidence | Gap / Issue |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Window control cluster | Accepted Reference | UIREF-002, FAM-002, AI Control Center seed | compact placement, Nexus glow, consistent state behavior | feature text and backend owner differ | Recording Studio and HUD Dashboard | Reference-Derived | screenshot and code trace | HUD historical issue candidate |

| Issue Candidate | Owner FAM | Surface | Element Group | Defect Class | Evidence | Proposed Carrier | GitHub Issue Mutation Approved? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F6-HIST-001 | FAM-006 | HUD Dashboard | Top-level close control | UIREF-002 visual grammar mismatch | USER screenshot and RAR ledger | future FAM-006 branch or approved current-branch repair | No |

| RAR USER Decision | Meaning | What It Authorizes | What It Does Not Authorize |
| --- | --- | --- | --- |
| Review issue candidate | USER agrees the issue candidate is real enough to route | Future issue action only after exact approval | Runtime mutation, sibling mutation, PR, merge, release, or automatic issue creation |
