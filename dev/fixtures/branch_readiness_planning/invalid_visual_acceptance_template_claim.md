# Invalid Visual Acceptance Template Claim Fixture

Material Visible Change Classification: Material visible UI is in scope for an AI diagnostics child window.

Visual Acceptance Target Plan: Visual Acceptance Target is defined before Workstream from UIREF-001 through UIREF-004 and accepted AI Control Center comparator evidence.

Implementation Authority Classification: Implementation Template Instantiated - AI Control Center template is claimed but no approved template source path exists.

Accepted Reference Set / Comparative Synthesis: UIREF-001, UIREF-002, and AI Control Center are compared element-by-element.

Visual Family Relation Proof: Row-by-row comparison maps frame, title, controls, and rows.

Implementation Authority Table: Current branch claims template implementation.

Functionality Role Contract: The diagnostics child window has a separate diagnostics role from the parent dashboard.

Implementation Match Proof Plan: Workstream traces code regions to rendered proof.

Pre-Live Visual Purpose Conformance: Before Live Validation, implementation match proof is compared against the target.

Visual Acceptance Chain: Vision Contract -> UIREF / Accepted Reference Set -> Visual Acceptance Target -> Implementation Match Proof -> Pre-Live Visual Purpose Conformance -> Live Validation -> UTS / PR.

Packet Reviewability vs Product Acceptance: Reviewability remains separate from product acceptance.

| Surface / Window | Role Classification | Implementation Authority | Accepted Reference | Element Group | Invariant Traits | Feature-Specific Traits | Rendered Evidence | Visual Match | Functional Match | Verdict | Next Legal Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AI diagnostics child window | Detached child diagnostics surface | Implementation Template Instantiated | UIREF-001 and AI Control Center | Window frame | NDAI frame and glow | Diagnostics content | Focused screenshot set | Match planned | Match planned | CONFORMING WHEN PROVEN | Continue after proof |

| Surface / Window | Approved Template? | Approved Shared Primitive? | Promoted Reference Consumed? | Reference-Derived? | One-Off? | Gap / Exception | Proof Required |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AI diagnostics child window | Yes | No | Yes - UIREF-001 | No | No | Template source missing | Approved template source path and element-by-element proof |

| Window / Surface | Product Role | Parent / Launch Source | Primary Actions | Secondary Actions | Non-Goals | Backend / State Owner | UI-Visible Truth Mapping | Recovery / Failure Behavior | Separate Surface Justification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AI diagnostics child window | Local readiness surface | AI Dashboard | Run local check | Close | No provider execution | FAM-007 runtime | Status rows map backend truth | Blocked/error rows | Focused diagnostics |

| Gate | Required Visual Proof | What Cannot Prove It | Blocking Condition | USER Decision Needed? |
| --- | --- | --- | --- | --- |
| BP2/BP3 | Approved template source plus proof | Comparator screenshot only | Template Claim Unsupported | Yes |
