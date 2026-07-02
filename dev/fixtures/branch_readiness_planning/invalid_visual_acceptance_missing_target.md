# Invalid Visual Acceptance Missing Target Fixture

Material Visible Change Classification: Material visible UI is in scope for an AI diagnostics child window.

Visual Acceptance Target Plan: TBD.

Implementation Authority Classification: Reference-Derived Implementation - no approved template or shared primitive exists for this surface class.

Accepted Reference Set / Comparative Synthesis: UIREF-001, UIREF-002, AI Dashboard, and AI Control Center are compared element-by-element.

Visual Family Relation Proof: Row-by-row comparison maps title stack and window controls.

Implementation Authority Table: Current branch declares reference-derived implementation only.

Functionality Role Contract: The diagnostics child window has a separate local-readiness role from the AI Dashboard.

Implementation Match Proof Plan: Workstream traces code regions to rendered proof.

Pre-Live Visual Purpose Conformance: Before Live Validation, Codex compares implementation match proof against the target.

Visual Acceptance Chain: Vision Contract -> UIREF / Accepted Reference Set -> Visual Acceptance Target -> Implementation Match Proof -> Pre-Live Visual Purpose Conformance -> Live Validation -> UTS / PR.

Packet Reviewability vs Product Acceptance: Reviewability remains separate from product acceptance.

| Surface / Window | Role Classification | Implementation Authority | Accepted Reference | Element Group | Invariant Traits | Feature-Specific Traits | Rendered Evidence | Visual Match | Functional Match | Verdict | Next Legal Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AI diagnostics child window | Detached child diagnostics surface | Reference-Derived Implementation | UIREF-001 and AI Control Center | Window frame | NDAI frame and glow | Diagnostics content | Focused screenshot set | Match planned | Match planned | CONFORMING WHEN PROVEN | Continue after proof |

| Surface / Window | Approved Template? | Approved Shared Primitive? | Promoted Reference Consumed? | Reference-Derived? | One-Off? | Gap / Exception | Proof Required |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AI diagnostics child window | No | No | Yes - UIREF-001 | Yes - comparator synthesis | No | No gap; proof required | Element-by-element proof |

| Window / Surface | Product Role | Parent / Launch Source | Primary Actions | Secondary Actions | Non-Goals | Backend / State Owner | UI-Visible Truth Mapping | Recovery / Failure Behavior | Separate Surface Justification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AI diagnostics child window | Local readiness surface | AI Dashboard | Run local check | Close | No provider execution | FAM-007 runtime | Status rows map backend truth | Blocked/error rows | Focused diagnostics |

| Gate | Required Visual Proof | What Cannot Prove It | Blocking Condition | USER Decision Needed? |
| --- | --- | --- | --- | --- |
| BP2/BP3 | Target and comparator | UIREF citation alone | Visual Acceptance Target Missing | Yes |
