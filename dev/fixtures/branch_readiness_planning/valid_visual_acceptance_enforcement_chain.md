# Visual Acceptance Enforcement Fixture

Material Visible Change Classification: Material visible UI is in scope for an AI diagnostics child window, so Branch Planning must carry a visual target before Workstream.

Visual Acceptance Target Plan: Visual Acceptance Target is defined before Workstream from UIREF-001 through UIREF-004 and the accepted AI Dashboard / AI Control Center comparator set.

Render Authority Level: Visual Acceptance Target - reviewable target packet exists before Workstream and USER acceptance remains pending.

Reviewable Visual Acceptance Target Path: C:\Nexus USER\FAM-007\Review Aids\AI_Diagnostics_Visual_Acceptance_Target.md.

Implementation Authority Classification: Reference-Derived Implementation - no approved template or shared primitive exists for this surface class.

Accepted Reference Set / Comparative Synthesis: UIREF-001, UIREF-002, UIREF-003, UIREF-004, AI Dashboard, and AI Control Center are compared element-by-element for invariant chrome, controls, rows, cards, spacing, typography, glow, and visible state behavior.

Visual Family Relation Proof: Row-by-row comparison maps title stack, frame, window control cluster, card borders, typography, spacing, glow, states, and scroll behavior against UIREF-001 through UIREF-004.

Implementation Authority Table: Current branch declares reference-derived implementation only.

Functionality Role Contract: The diagnostics child window has a separate role from the AI Dashboard because it opens from the dashboard, runs local diagnostic actions, and reports local readiness without provider/model behavior.

Implementation Match Proof Plan: Workstream must trace code regions to the rendered child window and produce focused screenshots or ordered-frame proof for every listed element group before Pre-Live.

Pre-Live Visual Purpose Conformance: Before Live Validation, Codex must compare implementation match proof against the Visual Acceptance Target and record whether the diagnostic child window preserves the intended role and visual family.

Visual Acceptance Chain: Vision Contract -> UIREF / Accepted Reference Set -> Visual Acceptance Target -> Implementation Match Proof -> Pre-Live Visual Purpose Conformance -> Live Validation -> UTS / PR.

Packet Reviewability vs Product Acceptance: The packet can become reviewable only after the tables are complete; product acceptance remains pending until USER visual acceptance, USER waiver, or approved defer/repair route.

| Surface / Window | Role Classification | Implementation Authority | Accepted Reference | Element Group | Invariant Traits | Feature-Specific Traits | Rendered Evidence | Visual Match | Functional Match | Verdict | Next Legal Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AI diagnostics child window | Detached child diagnostics surface launched from AI Dashboard | Reference-Derived Implementation | UIREF-001, UIREF-002, AI Dashboard, AI Control Center | Window frame and compact control cluster | Seamless rounded NDAI frame, compact top-right control cluster, deterministic glow and spacing | Diagnostics title and local readiness rows may differ by content only | Focused screenshot set and ordered-frame proof | Match planned through row-by-row comparison | Match planned through local diagnostic action proof | CONFORMING WHEN PROVEN | Continue only after Pre-Live proof is green |

| Surface / Window | Approved Template? | Approved Shared Primitive? | Promoted Reference Consumed? | Reference-Derived? | One-Off? | Gap / Exception | Proof Required |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AI diagnostics child window | No | No | Yes - UIREF-001 and UIREF-002 | Yes - AI Dashboard and AI Control Center comparator synthesis | No | No gap; reference-derived proof required | Element-by-element visual family proof before Workstream and Pre-Live. |

| Window / Surface | Product Role | Parent / Launch Source | Primary Actions | Secondary Actions | Non-Goals | Backend / State Owner | UI-Visible Truth Mapping | Recovery / Failure Behavior | Separate Surface Justification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AI diagnostics child window | Local readiness and diagnostic report surface | AI Dashboard local readiness card | Run local check, generate report, copy report | Close or return to dashboard | No provider execution, no prompt send, no memory write | FAM-007 local diagnostics runtime owner | Status rows must map local check, report, prompt/data, persistence, and summary to backend truth | Failed local check reports blocked/error state in the same row grammar | Separate child surface keeps diagnostics focused without overloading the parent dashboard |

| Gate | Required Visual Proof | What Cannot Prove It | Blocking Condition | USER Decision Needed? |
| --- | --- | --- | --- | --- |
| BP2/BP3 | Accepted reference set, implementation authority, role contract, and implementation-match proof plan | UIREF citation alone, packet reviewability, helper green, screenshot path | Visual Acceptance Target Missing or Accepted Reference Not Compared | Yes if target or comparator needs USER selection |
| Pre-Live | Focused screenshots or ordered frames compared row-by-row against accepted references | CSS marker similarity, validator green, attractive screenshot only | Pre-Live Visual Purpose Conformance Missing | Yes if Codex cannot objectively adjudicate |
