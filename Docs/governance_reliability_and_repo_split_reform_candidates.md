# Governance Reliability And Repo Split Reform Candidates

Document Status: Non-Binding Planning
Created: 2026-05-28
Source Basis: `C:\Nexus USER\Governance\Nexus_Project_Governance_Full_Digest.md`, current repo source truth, and USER-provided ChatGPT recommendation text.
Current Worktree: `C:\Nexus Worktrees\Governance`
Current Branch: `feature/release-readiness-source-truth-intake`
Last Plan Reconciliation Baseline: `origin/main@7c26748bb6d04433a52b19d41dcacadebeb82c8e` after PR #269 merged FAM-007 AI Control Center boundary flow evidence. This is a reconciliation receipt, not a live-state ledger.

## First Step - Post-Idle Rebaseline And Plan Reconciliation

Before any governance reliability reform cycle begins, wait until the active FAM worktrees have finished their current PR / merge / release flow or USER explicitly approves starting earlier.

After the worktrees are idle, rebaseline and reconcile the relevant worktrees against the new `origin/main` baseline. Then analyze this plan against the new baseline before implementation. The analysis must:

- reload `Docs/Main.md` first and follow the routed source-truth owners
- compare this plan against the new repo baseline, current external operational state, and any newly merged FAM-006 / FAM-007 source-truth changes
- identify plan items that are still valid, stale, superseded, duplicated, missing, or now better owned by a different source-truth file
- reconcile Main / Dev / Owner split assumptions against current FAM-007 source truth
- update this planning file with recommendations before any reform cycle mutates binding source truth
- return a digest with changed recommendations, blockers, owner-file impacts, and exact USER decisions needed

This first step is a planning/reconciliation gate. It does not authorize source-truth contract edits, helper code, validator code, PR Readiness, PR creation, merge, release, repo split execution, private repo creation, runtime work, FAM worktree mutation, file movement, file deletion, or file archival.

## Historical No-PR Hold - 2026-06-15

Current USER direction supersedes older planning text that treated PR Readiness as the immediate next phase after the docs-only cycles and final hardening. There will be no PR for this broader governance reliability / vision / proof reliability track until the USER confirms that all admitted work for the track is implemented, including any separately admitted template, golden-reference, design-token, shared UI primitive, helper, validator, fixture, or product-worktree adoption work.

When final hardening reaches a blocker such as `Golden Template / Reference Promotion Blocked`, Codex must stop and wait rather than request PR Readiness. This hold does not approve template creation, golden-reference promotion, design-token implementation, shared UI primitive implementation, helper/validator code, FAM worktree mutation, external-state mutation, PR creation, merge, release, or cleanup. Those remain separate USER decisions under current source truth. The template/reference plan-completion portion is completed by the 2026-06-16 planning completion below, but USER later clarified that all planned template/reference work belongs to the current branch/current PR. Therefore plan completion alone does not permit PR Readiness for this branch.

## Template / Golden Reference Visual Proof Promotion Review Packet - 2026-06-17

Document Status: Non-Binding Evidence Receipt. Binding authority remains with `Docs/nexus_vision.md` for Project UI Vision and proof hierarchy, `Docs/family_visions/FAM-002_desktop_interface.md` for reusable presentation grammar, `Docs/family_feature_visions/F2-FF01.md` for UI reference-system missing-proof rows and promotion-planning boundaries, and `Docs/ui_reference_catalog/` for promoted UI reference records only after explicit USER promotion approval.

Packet: `C:\Nexus USER\Governance`

Timestamped ZIP: `C:\Nexus USER\Governance-20260617-095237.zip`

Disposition: `Evidence reviewable / no promotion`. Existing FAM-006 HUD and PR #269 FAM-007 AI Control Center evidence are useful candidate evidence for later reference promotion, but the packet does not promote any catalog record, create any template, implement design tokens/shared primitives, mutate helpers/validators/fixtures, mutate FAM worktrees, mutate external state, create a PR, merge, release, create issues, move/delete/archive files, or clear `Current Branch Template Work Incomplete`.

Candidate disposition summary:

- HUD/FAM-006 surface reference: `REVISE`.
- PR #269 AI Control Center surface reference: `REVISE`.
- Golden window reference: `REVISE`.
- Golden control-cluster reference: `REVISE`.
- Close/minimize/maximize cluster reference: `REVISE`.
- Full button set, dropdown/menu/list/filter reference, modal/dialog template, status/failure/recovery panel template, tray/menu doorway template, design tokens, shared primitives, negative fixtures/bad examples, helper/validator enforcement, and active FAM-006/FAM-007 adoption mutation: `DEFERRED`.

Catalog result: `Docs/ui_reference_catalog/index.md` remains at `Promoted Reference Count: 0`. No golden reference exists until a future USER-approved promotion record is written.

## Template / Golden Reference Package A Review - 2026-06-17

Document Status: Non-Binding Package Review Receipt. Binding authority remains with `Docs/nexus_vision.md` for Project UI Vision and proof hierarchy, `Docs/family_visions/FAM-002_desktop_interface.md` for Desktop Interface presentation grammar, `Docs/family_feature_visions/F2-FF01.md` for UI reference-system missing-proof rows, `Docs/ui_reference_catalog/` for USER-promoted reference records only after explicit promotion approval, and `Docs/phase_governance.md` for proof/blocker routing.

Package A Scope: `Top-Level Window And Window Control Cluster` only. Reviewed candidates are golden window reference, HUD/FAM-006 surface evidence, PR #269 AI Control Center evidence, golden control-cluster reference, and close/minimize/maximize pill/cluster standard. Package B controls, Package C surface/settings/doorway classes, Package D design-token/shared-rule authority, Package E fixture/helper/validator expectations, and target-FAM adoption remain current-PR scope where recorded below, but they are not reviewed by this Package A receipt.

Package A Result: `REVISE / MISSING PROOF - NO PROMOTION`. Existing FAM-006 and FAM-007 evidence is strong enough to support a later USER-visible promotion packet, but it is not sufficient to promote a golden reference, write a catalog record, create a template, or clear `Golden Reference Promotion Blocked`. `Docs/ui_reference_catalog/index.md` remains at `Promoted Reference Count: 0`.

| Candidate | Evidence Source | Comparison Basis | Current Decision | Missing Proof | Ready For Later Promotion Packet? | Blocks PR Readiness? | Next USER Approval Needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HUD/FAM-006 surface evidence | Existing HUD desktop/focused screenshots, Manage Monitors visual evidence, FAM-006 vision, prior LV/packet evidence | Project UI Vision, FAM-002 grammar, F2-FF01 missing-proof rows, FAM-006 visual-system carrydown, element-group proof rules | `REVISE - candidate comparison evidence only` | Isolated top-level/child-window classification, element-group state matrix, large `CLOSE` pill exception/disposition, hover/focus/disabled proof, applicability/non-applicability, USER acceptance | Yes, only after missing proof is collected or waived in a promotion packet | Yes, while Package A remains current-PR scoped and unresolved | Approve Package A missing-proof collection or explicitly reclassify HUD evidence as comparison-only for this PR |
| PR #269 AI Control Center evidence | AI Control Center default, minimize hover, close hover, corner resize screenshots, PR #269/H4 evidence, FAM-007 trust-boundary vision | Project UI Vision, FAM-002 top-level window/control grammar, F2-FF01 top-level/window-control rows, FAM-007 provider/trust boundaries, USER proof hierarchy | `REVISE - strongest Package A seed, not promotion-ready` | Maximize/restore/hidden-control matrix, disabled/blocked/focus/pressed states, keyboard/focus/hitbox/accessibility proof, multi-surface comparison, provider/private/runtime deferral proof, USER acceptance | Yes, strongest candidate after missing proof is filled | Yes | Approve a Package A promotion packet or proof-collection packet for AI Control Center-derived top-level window/control-cluster evidence |
| Golden window reference | Combined HUD/FAM-006 and AI Control Center candidate surfaces | Project UI Vision, FAM-002 Nexus-native chrome and immersion contract, F2-FF01 `Top-Level Window` reference class, catalog schema | `REVISE - no promoted top-level reference exists` | Complete top-level window schema, eligible/non-eligible window classes, geometry/resize/reset expectations, platform exceptions, multi-surface proof, known limitations, USER acceptance | Not yet; requires the promotion packet to define the reference contract first | Yes | Approve creation of a USER-reviewed promotion packet for the top-level window reference, or reclassify Package A out of current PR scope |
| Golden control-cluster reference | AI Control Center compact close/minimize cluster and hover screenshots | FAM-002 top-level control grammar, F2-FF01 compact window-control cluster category, element-group acceptance rules | `REVISE - candidate-only control cluster` | Close/minimize/maximize/restore applicability by window class, blocked/hidden behavior, focus/pressed/disabled states, tooltip/accessibility names, hitboxes, keyboard/focus proof, child/modal distinction | Not yet; likely paired with golden window promotion after missing proof | Yes | Approve focused control-cluster proof collection / promotion packet |
| Close/minimize/maximize pill/cluster standard | AI Control Center close/minimize hover evidence plus FAM-002 grammar distinguishing top-level clusters from large content/action `CLOSE` pills | Project UI immersion contract, FAM-002 top-level window-control grammar, F2-FF01 control-cluster row, HUD/FAM-006 large `CLOSE` comparison | `REVISE - standard direction accepted for planning, not promoted` | Window-class matrix for top-level/child/modal/dialog/proof/dev/platform exceptions, all visual states, blocked controls, accessibility proof, USER acceptance | Not yet; must be folded into golden control-cluster packet or explicitly waived | Yes | Approve the same focused Package A promotion packet or a USER waiver for limited scope |

| Lane | In Package A? | Current PR Scope? | Current Status | Reason | Deferred Until / Later Package |
| --- | --- | --- | --- | --- | --- |
| HUD/FAM-006 surface reference | Yes | Yes | `REVISE / missing proof` | Candidate evidence helps compare top-level/card/window grammar but is not a promoted reference | Package A missing-proof collection or USER reclassification |
| PR #269 AI Control Center surface reference | Yes | Yes | `REVISE / missing proof` | Strong top-level/control-cluster seed but still lacks complete state/accessibility/class proof | Package A missing-proof collection or USER reclassification |
| Golden window reference | Yes | Yes | `REVISE / no promoted reference` | Catalog requires explicit promotion record and required schema fields | Package A promotion packet after proof |
| Golden control-cluster reference | Yes | Yes | `REVISE / no promoted reference` | Compact cluster is candidate-only until state/class proof exists | Package A promotion packet after proof |
| Close/minimize/maximize cluster standard | Yes | Yes | `REVISE / no promoted reference` | Needs class matrix and state proof before becoming reusable standard | Package A promotion packet after proof |
| Button/dropdown/menu/list/filter standards | No | Yes | Pending | Current-PR authority scope, but outside Package A | Package B |
| Modal/status/tray/Global Settings surface standards | No | Yes | Pending | Current-PR authority scope, but outside Package A; FAM-003 remains required consumer/context input | Package C |
| Design tokens and shared UI rules | No | Yes | Pending | Current-PR authority scope, but implementation remains separately gated | Package D |
| Negative examples / helper / validator expectations | No | Yes | Pending | Current-PR authority scope, but fixture/helper/validator mutation remains separately gated | Package E |
| Target-FAM adoption mutation | No | No | Deferred | FAM-003/FAM-006/FAM-007 consume/adopt only later in their own legal carriers after merge/rebaseline | Target-FAM next legal gate |

| Blocker | Current Status | Cleared By This Cycle? | Reason | Next Legal Action |
| --- | --- | --- | --- | --- |
| `Current Branch Template Work Incomplete` | Active | No | Package A review is complete as analysis, but Package A promotion proof is still missing and Packages B-E remain unresolved current-PR scope | Approve Package A missing-proof collection / promotion-packet generation, or explicitly reclassify Package A missing-proof work out of current PR scope |
| `Golden Reference Promotion Blocked` | Active | No | No USER-approved promotion packet or catalog record exists | Approve a future promotion packet after proof and USER visual acceptance |
| `Promoted Reference Count: 0` | Preserved / blocking for claims of promoted references | No | Empty catalog is correct until promotion proof exists, but it also proves no golden reference has been promoted | Keep count zero until USER approves a catalog promotion record |
| `Template Treated As Existing Proof` | Avoided | Yes for this Package A review | This receipt keeps all visuals as candidate evidence only | Continue blocking any branch that treats candidate evidence as promoted proof |
| `Shared Primitive Promotion Blocked` | Active | No | Package A does not admit design-token/shared-primitive implementation | Package D or later exact USER implementation approval |
| `FAM Worktree Mutation Approval Missing` | Avoided | Yes for this Package A review | FAM-003/FAM-006/FAM-007 remain consumer/context inputs only; no sibling worktree mutation is authorized | Target FAMs reconcile/adopt later in their own legal carriers |

Package A Next Legal Use: USER may approve a bounded Package A missing-proof collection and promotion-packet generation cycle, approve a narrow USER visual promotion path for a named Package A candidate after proof, or explicitly reclassify Package A missing-proof work out of current PR scope. Without one of those decisions, PR Readiness remains blocked.

## Template / Golden Reference Package A Missing-Proof Packet - 2026-06-17

Document Status: Non-Binding Promotion-Packet Generation Receipt. Binding authority remains with `Docs/nexus_vision.md`, `Docs/family_visions/FAM-002_desktop_interface.md`, `Docs/family_feature_visions/F2-FF01.md`, `Docs/ui_reference_catalog/`, `Docs/phase_governance.md`, and `Docs/user_test_summary_guidance.md`.

Packet: `C:\Nexus USER\Governance`

Timestamped ZIP: the current timestamped packet ZIP path and SHA256 are reported in the Codex return packet because embedding a final ZIP name or hash inside the ZIP would mutate the ZIP and create stale packet drift.

Package A Missing-Proof Result: `PROMOTION PACKET GENERATED - NO PROMOTION`. Governance classified existing proof, copied/reused only approved read-only evidence already present in the Governance USER packet, and generated a USER-reviewable packet that defines missing proof, window-class draft rules, control-cluster state requirements, geometry/reset expectations, accessibility/hitbox/focus/pressed/blocked/hidden proof needs, and USER visual acceptance requirements.

| Candidate | Missing Proof | Existing Evidence Found | Proof Classification | Required Source / Collector | Requires Later FAM Runtime Approval? | Requires USER Visual Acceptance? | Blocks Package A Promotion? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HUD/FAM-006 surface evidence | Isolated top-level/child classification, complete element-state matrix, large `CLOSE` pill disposition, hover/focus/disabled proof, applicability/non-applicability, USER acceptance | HUD desktop screenshot, Manage Monitors focused screenshot, Recording Target visual contract screenshot, HUD LV video | Existing proof available but insufficient for promotion | Future FAM-006 legal carrier or USER waiver; Governance can only preserve packet evidence | Yes, if new runtime/visual proof must be collected | Yes | Yes |
| PR #269 AI Control Center evidence | Maximize/restore/hidden-control matrix, disabled/blocked/focus/pressed states, keyboard/focus/hitbox/accessibility proof, multi-surface comparison, provider/private/runtime deferral proof, USER acceptance | Default, close hover, corner resize screenshots; minimize-hover file exists but hashes identical to default and is insufficient as hover proof | Existing proof available but insufficient; one claimed hover proof is not independently proven | Future FAM-007 legal carrier or USER waiver; Governance can only preserve packet evidence | Yes, if new runtime/visual proof must be collected | Yes | Yes |
| Golden window reference | Complete reference schema, eligible/non-eligible class matrix, geometry/resize/reset expectations, platform exceptions, known limitations, USER acceptance | HUD and AI Control Center candidate surfaces | Source-truth draft available; promoted proof missing | Governance/FAM-002 promotion packet after proof; target FAMs supply candidate evidence later if needed | No for schema draft; yes for new runtime proof | Yes | Yes |
| Golden control-cluster reference | Close/minimize/maximize/restore applicability, blocked/hidden controls, hover/focus/pressed/disabled states, tooltip/accessibility names, hitboxes, keyboard/focus proof, child/modal distinction | AI Control Center compact cluster and close-hover proof; minimize-hover file insufficient by hash | Existing proof available but insufficient | Governance/FAM-002 promotion packet plus future FAM evidence or USER waiver | Yes, if new runtime/visual proof must be collected | Yes | Yes |
| Close/minimize/maximize standard | Window-class matrix, all visual states, blocked controls, top-level/child/modal/platform exception rule, USER acceptance | AI Control Center close/minimize cluster and FAM-002 grammar; HUD large `CLOSE` comparison | Source-truth direction exists; promotion proof missing | Governance/FAM-002 promotion packet after proof | Yes, if new runtime/visual proof must be collected | Yes | Yes |

| Candidate | Promotion Readiness | Reason | Can Promote In Later Packet? | Later USER Approval Needed |
| --- | --- | --- | --- | --- |
| HUD/FAM-006 surface evidence | Not ready | Useful comparison evidence, but not isolated or state-complete and large `CLOSE` needs class disposition | Yes, after proof/waiver | USER visual acceptance or explicit comparison-only disposition |
| PR #269 AI Control Center evidence | Not ready, strongest seed | Custom Nexus chrome, compact cluster, and resize evidence exist, but state/accessibility/maximize/restore proof is incomplete | Yes, after proof/waiver | USER visual acceptance plus promotion approval |
| Golden window reference | Not ready | Reference contract is draftable, but no complete promoted schema/proof record exists | Yes, after proof/waiver | USER approval to promote a catalog record |
| Golden control-cluster reference | Not ready | Candidate cluster exists, but full control-state/class proof is missing | Yes, after proof/waiver | USER approval to promote a catalog record |
| Close/minimize/maximize standard | Not ready | Direction is strong for top-level windows, but class matrix/state proof is incomplete | Yes, after proof/waiver | USER approval to promote as part of the control-cluster record |

Package A Packet Boundary: This pass does not promote references, create catalog records, create templates, implement design tokens/shared primitives, mutate helpers/validators/fixtures, mutate FAM-003/FAM-006/FAM-007/main worktrees, mutate external state, create issues, create a PR, merge, release, move/delete/archive repo files, or accept USER visual proof. `Docs/ui_reference_catalog/index.md` remains `Promoted Reference Count: 0`.

Package A Next Legal Use: USER must review the generated Package A packet and choose one of these legal paths before Package A can stop blocking PR Readiness: accept the no-promotion packet and explicitly reclassify Package A missing-proof work out of current PR scope; approve later FAM/runtime proof collection in the owning FAM carriers; approve a narrower USER visual waiver/promotion route for a named Package A candidate; or reject one or more candidates and route the branch to Package B only after the Package A disposition is durable.

## Template / Golden Reference Package A Proof-Route Decision - 2026-06-17

Document Status: Non-Binding Proof-Route Decision Receipt. Binding authority remains with `Docs/nexus_vision.md`, `Docs/family_visions/FAM-002_desktop_interface.md`, `Docs/family_feature_visions/F2-FF01.md`, `Docs/ui_reference_catalog/`, `Docs/phase_governance.md`, and `Docs/user_test_summary_guidance.md`.

Accepted Packet Result: `PROMOTION PACKET GENERATED - NO PROMOTION`. USER accepted the Package A packet as reviewable evidence and clarified that Governance / FAM-002 template-reference authority lanes remain in current Governance PR scope except active FAM-003/FAM-006/FAM-007 adoption mutation. Package A is not reclassified out of current PR scope by this receipt.

Proof-Route Result: Package A cannot promote a reference using existing Governance-only proof. Existing HUD/FAM-006 and PR #269 AI Control Center evidence remains candidate/comparison evidence. Missing visual, state, accessibility, class, reset, and USER acceptance proof must be collected through a later legal proof route before any Package A catalog promotion can occur.

| Candidate | Missing Proof | Current Evidence | Required Proof Route | Can Be Resolved In Governance Only? | Requires FAM/Runtime Approval? | Requires USER Screenshot/Video? | Requires USER Visual Acceptance? | Blocks Package A Promotion? | Recommended Next Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HUD/FAM-006 surface evidence | Isolated top-level/child classification, element-state matrix, large `CLOSE` pill disposition, hover/focus/disabled proof, applicability/non-applicability, USER acceptance | Existing HUD desktop/focused screenshots, Manage Monitors focused screenshot, Recording Target screenshot, HUD LV video | Later FAM-006 runtime proof carrier or USER-provided screenshot/video/waiver packet; Governance can preserve comparison evidence only | No | Yes, unless USER provides sufficient existing proof or waiver | Yes, for missing visual/state proof unless waived | Yes | Yes | Keep as comparison candidate; route missing proof to FAM-006 or USER-provided proof packet |
| PR #269 AI Control Center evidence | Maximize/restore/hidden-control matrix, disabled/blocked/focus/pressed states, keyboard/focus/hitbox/accessibility proof, multi-surface comparison, independent minimize-hover proof, USER acceptance | Default, close-hover, corner-resize screenshots; minimize-hover file exists but hashes identical to default and is not independent proof | Later FAM-007 runtime proof carrier or USER-provided screenshot/video/waiver packet; Governance can preserve candidate evidence only | No | Yes, unless USER provides sufficient existing proof or waiver | Yes, for missing visual/state proof unless waived | Yes | Yes | Treat as strongest seed; collect missing states before any promotion |
| Golden window reference | Complete reference schema, eligible/non-eligible window classes, geometry/resize/reset expectations, platform exceptions, known limitations, USER acceptance | FAM-002 grammar, F2-FF01 missing-proof rows, HUD and AI Control Center candidates | Governance can draft schema in a later approved packet, but promotion requires visual proof and USER acceptance/waiver | Partially for schema only; no for promotion | Yes if new runtime evidence is required | Yes, unless existing proof is accepted or waived | Yes | Yes | Defer promotion; consider a schema-only planning packet only if USER approves that narrower route |
| Golden control-cluster reference | Close/minimize/maximize/restore applicability, blocked/hidden controls, hover/focus/pressed/disabled states, tooltip/accessibility names, hitboxes, keyboard/focus proof, child/modal distinction | AI Control Center compact cluster and close-hover proof; minimize-hover file insufficient by hash | Later FAM/runtime proof or USER-provided screenshot/video/waiver packet; Governance can define required route only | No | Yes, unless USER provides sufficient existing proof or waiver | Yes, for missing state/accessibility proof unless waived | Yes | Yes | Pair with top-level window proof when collecting Package A evidence |
| Close/minimize/maximize standard | Window-class matrix, all visual states, blocked controls, top-level/child/modal/dialog/proof/dev/platform exception rule, USER acceptance | FAM-002 grammar, AI Control Center cluster, HUD large `CLOSE` comparison | Later proof packet proving applicability/non-applicability; USER waiver can narrow scope but cannot imply full promotion | No | Yes, if new runtime evidence is required | Yes, unless waived | Yes | Yes | Preserve as direction; do not promote until class/state proof exists |

| Path | What It Does | Legal Now? | USER Approval Needed | PR Impact | Recommendation |
| --- | --- | --- | --- | --- | --- |
| Package A FAM/runtime proof collection approval | Lets FAM-006/FAM-007 or other owning runtime carriers collect missing live visual/state/accessibility proof | Not under this approval | Later exact FAM/runtime proof approval | Keeps Package A blocked until proof returns | Use when USER wants promotion-grade proof from real owning surfaces |
| Package A USER-provided screenshot/video proof collection | USER supplies missing screenshots/video without Codex mutating FAM worktrees or launching runtime proof | Not executed by this receipt, but can be the next legal approval | Later exact proof-intake approval plus visual acceptance decision | Could reduce FAM-runtime delay if evidence is sufficient | Best near-term no-FAM-mutation route if USER can provide proof |
| Package A narrow USER waiver/promotion route | USER waives named missing proof or narrows promotion scope for a named candidate | Not under this approval | Explicit waiver plus later promotion approval | Can clear a narrow reference only if source truth allows the limited scope | Use only for a named candidate and named waived proof gaps |
| Package A revise/reject/defer route | Rejects or defers candidates without promotion | Partially available as a decision, but not recorded here as final disposition | USER decision naming candidates | Keeps Package A in current PR scope unless explicitly removed | Use if candidates are not worth collecting proof for now |
| Proceed to Package B while Package A remains blocked | Continues Package B-E current-PR work while Package A blockers remain tracked | Yes for planning/next package work; no PR Readiness | USER approval for Package B entry | PR Readiness remains blocked until Package A disposition/proof is resolved or reclassified | Recommended if Package A proof cannot be collected now but current PR work should continue |
| Reclassify Package A out of current PR scope | Removes Package A from current PR blocking scope | Not approved by USER; explicitly excluded unless later stated | Explicit USER reclassification | Would unblock current PR only if all other packages/hardening are complete | Not recommended unless USER later changes scope |

Package A Next Legal Use: choose one explicit route. Recommended next path is either `Package A USER-provided screenshot/video proof collection` if USER can provide missing visual/state proof without FAM mutation, or `Proceed to Package B while Package A remains blocked` if proof collection must wait for later FAM/runtime carriers. `Current Branch Template Work Incomplete`, `Golden Reference Promotion Blocked`, `Promoted Reference Count: 0`, and Package A proof incomplete remain active.

## Template / Golden Reference Package B Packet - 2026-06-17

Document Status: Non-Binding Promotion-Packet Generation Receipt. Binding authority remains with `Docs/nexus_vision.md`, `Docs/family_visions/FAM-002_desktop_interface.md`, `Docs/family_feature_visions/F2-FF01.md`, `Docs/ui_reference_catalog/`, `Docs/phase_governance.md`, and `Docs/user_test_summary_guidance.md`.

Package B Scope: `Buttons, Dropdowns, Menus, Lists, and Filters` only. Package A remains current-PR scope and blocked for promotion. Packages C-E remain current-PR scope and are not reviewed by this Package B receipt. Target-FAM adoption remains post-merge/rebaseline work in each target FAM legal carrier.

Package B Result: `PROMOTION PACKET GENERATED - NO PROMOTION`. Existing HUD/FAM-006 and PR #269 AI Control Center evidence is useful for comparison, but it does not contain complete button/dropdown/menu/list/filter element-state, accessibility, keyboard, empty/loading/error, or USER-acceptance proof. `Docs/ui_reference_catalog/index.md` remains at `Promoted Reference Count: 0`.

| Lane | Candidate Evidence | Current Proof Status | Missing Proof | Disposition | Can Continue Without Stopping? | Later Approval Needed |
| --- | --- | --- | --- | --- | --- | --- |
| Button standards | FAM-002 grammar; F2-FF01 button/control-state row; HUD controls; AI Control Center window-control/button-like evidence | Existing proof available but insufficient | Primary/secondary/danger/default/hover/focus/pressed/disabled/loading/error states, text/icon alignment, spacing, contrast, keyboard activation, hitbox/accessibility proof, USER acceptance | `REVISE - candidate comparison evidence only` | Yes | USER visual acceptance or later FAM/runtime proof |
| Dropdown standards | FAM-002 grammar; F2-FF01 dropdown/menu/list/filter row; Manage Monitors context where applicable | Proof mostly missing | Closed/open states, selected item, hover/focus/keyboard navigation, disabled/empty/error/overflow states, option grouping, accessibility labels, USER acceptance | `DEFER - proof missing` | Yes | Later FAM/runtime proof or USER-provided proof |
| Menu standards | FAM-002 grammar; tray/menu doorway planning context; HUD/AI packet evidence as general visual context only | Proof missing for Package B menu promotion | Open/closed, hover, focus, selected, disabled, separator/grouping, nested/overflow, keyboard navigation, dismissed state, accessibility proof, USER acceptance | `DEFER - proof missing` | Yes | Later FAM/runtime proof or USER-provided proof |
| List standards | FAM-002 grammar; F2-FF01 list row; HUD/monitor/log surface planning context | Proof insufficient | Row density, selected/unselected, hover/focus, empty/loading/error states, sorting/filtering relationship, keyboard traversal, screen-reader/accessibility proof, USER acceptance | `DEFER - proof missing` | Yes | Later FAM/runtime proof or USER-provided proof |
| Filter standards | FAM-002 grammar; F2-FF01 filter row; future log/monitor/search surfaces | Proof missing | Default/active/cleared/invalid states, chip/search/filter combinations, reset/clear behavior, empty result state, keyboard/accessibility proof, USER acceptance | `DEFER - proof missing` | Yes | Later FAM/runtime proof or USER-provided proof |

| Component | Normal | Hover | Focus | Pressed | Disabled | Blocked | Loading | Empty | Error | Required Proof |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Button | Required | Required | Required | Required | Required when unavailable | Required when action is gated | Required for async action | Not applicable unless button group empty state exists | Required for failed action | Screenshot/video or USER-visible proof plus code-to-visual trace and USER acceptance |
| Dropdown | Required | Required for trigger/options | Required for trigger/options | Required for trigger/options | Required when unavailable | Required when gated by state/permission | Required for async options | Required when no options exist | Required for invalid/load failure | Open/closed proof, keyboard proof, option proof, accessibility proof |
| Menu | Required | Required | Required | Required for selectable items | Required when item unavailable | Required when item gated | Required when dynamic menu loads | Required when no actions exist | Required when menu action fails | Open/dismissed proof, grouping/overflow proof, keyboard/accessibility proof |
| List | Required | Required for rows | Required for rows | Required for selection/action rows | Required when row unavailable | Required when gated | Required for data loading | Required | Required for data failure | Row/state proof, selection proof, empty/loading/error proof |
| Filter | Required | Required | Required | Required for active/clear actions | Required when unavailable | Required when gated | Required if filter applies async | Required for no results | Required for invalid query/failure | Active/cleared/invalid/no-result proof plus accessibility proof |

| Candidate Standard | Promotion Readiness | Reason | Can Promote In Later Packet? | Later USER Approval Needed |
| --- | --- | --- | --- | --- |
| Button standard | Not ready | FAM-002 direction exists, but state, accessibility, and USER-accepted evidence are incomplete | Yes, after proof/waiver | USER visual acceptance plus promotion approval |
| Dropdown standard | Not ready | Promotion-grade dropdown state proof is missing | Yes, after proof/waiver | USER visual acceptance plus promotion approval |
| Menu standard | Not ready | Promotion-grade menu/open/dismiss/keyboard proof is missing | Yes, after proof/waiver | USER visual acceptance plus promotion approval |
| List standard | Not ready | Row/selection/empty/loading/error proof is incomplete | Yes, after proof/waiver | USER visual acceptance plus promotion approval |
| Filter standard | Not ready | Active/clear/invalid/no-result proof is missing | Yes, after proof/waiver | USER visual acceptance plus promotion approval |

Package B Packet Boundary: This pass does not promote references, create catalog records, create templates, implement design tokens/shared primitives, mutate helpers/validators/fixtures, mutate FAM-003/FAM-006/FAM-007/main worktrees, mutate external state, create issues, create a PR, merge, release, move/delete/archive repo files, or accept USER visual proof. `Docs/ui_reference_catalog/index.md` remains `Promoted Reference Count: 0`.

Package B Next Legal Use: USER must review the generated Package B packet and choose one of these legal paths: approve later proof collection or USER-provided proof intake for named Package B lanes; approve a narrow USER waiver/promotion route for a named Package B candidate; reject or defer named Package B candidates; or proceed to Package C while Package B remains blocked. Package B is not reclassified out of current PR scope unless USER later says so explicitly.

## Template / Golden Reference Package C Packet - 2026-06-17

Document Status: Non-Binding Promotion-Packet Generation Receipt. Binding authority remains with `Docs/nexus_vision.md` for Project UI Vision and proof hierarchy, `Docs/family_visions/FAM-002_desktop_interface.md` for reusable Desktop Interface presentation grammar, `Docs/family_feature_visions/F2-FF01.md` for UI reference-system missing-proof rows and promotion-planning boundaries, `Docs/family_feature_visions/F3-FF01.md` for resident access, Global Settings entry/routing, quick-access, tray/menu doorway, and compact resident UI planning context, `Docs/ui_reference_catalog/` for promoted UI reference records only after explicit USER promotion approval, `Docs/phase_governance.md` for proof/blocker routing, and `Docs/user_test_summary_guidance.md` for USER-facing proof interpretation.

Package C Scope: `Modal/Dialog, Status/Failure/Recovery Panel, and Tray/Menu Doorway` only. Package A top-level window/control-cluster proof remains incomplete. Package B button/dropdown/menu/list/filter proof remains incomplete. Package D design-token/shared UI rule ownership and Package E negative example/helper/validator expectations remain current-PR scope but are not reviewed by this Package C receipt.

Package C Result: `PROMOTION PACKET GENERATED - NO PROMOTION`. Existing FAM-006 HUD/Manage Monitors/recording evidence, PR #269 FAM-007 AI Control Center evidence, FAM-002 presentation grammar, F2-FF01 reference-system rows, and F3-FF01 resident-access planning are useful comparison evidence, but they are not sufficient to promote any Package C catalog record, create any template, implement tray/settings runtime, or clear `Golden Reference Promotion Blocked`. `Docs/ui_reference_catalog/index.md` remains at `Promoted Reference Count: 0`.

| Lane | Candidate Evidence | Current Proof Status | Missing Proof | Disposition | Can Continue Without Stopping? | Later Approval Needed |
| --- | --- | --- | --- | --- | --- | --- |
| Modal/dialog standards | FAM-002 modal/dialog grammar; F2-FF01 modal, child-window, dialog, confirmation, platform-native exception row; HUD Manage Monitors child-window evidence; AI Control Center top-level comparison evidence | Existing proof available but insufficient | Modal class split, child-window versus modal versus dialog taxonomy, open/close/dismiss/confirm/cancel/destructive flows, focus trap, Escape behavior, keyboard traversal, blocked/disabled states, platform-native exception rule, accessibility names, and USER acceptance | `REVISE - candidate comparison evidence only` | Yes | Later FAM/runtime proof, USER-provided proof, explicit USER waiver, or USER promotion approval |
| Status/failure/recovery panel standards | Project fail-proof UI vision; FAM-002 status/failure/recovery presentation grammar; F2-FF01 status/degraded/blocked/fatal/recovery row; FAM-006 status/recording/log evidence; FAM-007 trust/provider-deferral context | Existing proof available but insufficient | Success/warning/info/degraded/blocked/fatal/recoverable states, retry/reset/manual-report/support-bundle paths, loading/error/empty states, runtime-truth mapping, safe wording, failure-to-recovery sequence, visual proof, and USER acceptance | `DEFER - proof missing` | Yes | Later owning-FAM proof, USER-provided proof, explicit USER waiver, or USER promotion approval |
| Tray/menu doorway standards | F3-FF01 resident access, Global Settings, quick-access, tray/menu doorway, privacy/status doorway planning; FAM-003 family vision; FAM-002 compact resident UI grammar; F2-FF01 tray/menu doorway row | Proof mostly missing | Real tray doorway proof, open/close/dismiss/menu-state proof, compact menu budget, immutable versus configurable entries, privacy/status visibility, Windows tray limitation handling, keyboard/accessibility behavior, link-to-owning-surface proof, settings-category routing proof, and USER acceptance | `DEFER - proof missing` | Yes | Later FAM-003/runtime proof, USER-provided proof, explicit USER waiver, or USER promotion approval |

| Component | Normal | Hover | Focus | Pressed / Selected | Disabled | Blocked | Loading | Empty | Error | Recovery | Required Proof |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Modal/Dialog | Required for eligible modal/dialog class | Required for actionable controls | Required for initial focus and focus trap | Required for confirm/cancel/destructive controls | Required when action unavailable | Required when state/policy prevents action | Required when modal waits on async work | Required when content has no items/options | Required when modal action/load fails | Required for retry, dismiss, reset, or fallback path | Screenshot/video or USER-visible proof for open, interaction, dismiss, keyboard, accessibility, class applicability, and USER acceptance |
| Status/Failure/Recovery Panel | Required for each status class | Required when panel has controls/links | Required for controls/links | Required for retry/reset/report actions | Required when action unavailable | Required when permission/policy/runtime blocks recovery | Required for pending diagnostics/recovery | Required when no data/logs/actions exist | Required for failed action or degraded/fatal state | Required for recovery path and final state | Visual proof plus runtime-truth mapping, claim/evidence class, safe wording, recovery sequence, and USER acceptance |
| Tray/Menu Doorway | Required for icon/menu/compact status | Required for menu rows/actions | Required for keyboard/menu focus | Required for menu selection/toggle rows | Required when a linked surface is unavailable | Required when privacy/provider/policy blocks an action | Required when dynamic menu/status loads | Required when optional quick-access slots are empty | Required when linked surface/action fails | Required for recovery/settings route when tray state is stale or hidden | Real USER-path screenshot/video or USER manual proof covering Windows tray limitation, compact menu budget, link routing, privacy visibility, accessibility, and USER acceptance |

| Candidate Standard | Promotion Readiness | Reason | Can Promote In Later Packet? | Later USER Approval Needed |
| --- | --- | --- | --- | --- |
| Modal/dialog standard | Not ready | Taxonomy and draft expectations are clear, but modal/dialog state, keyboard, focus, platform-exception, and USER-accepted visual proof are incomplete | Yes, after proof/waiver | USER visual acceptance plus promotion approval |
| Status/failure/recovery panel standard | Not ready | FAM-002 and F2-FF01 provide direction, but promotion-grade runtime-truth mapping, failure/recovery sequence proof, and USER acceptance are missing | Yes, after proof/waiver | USER visual acceptance plus promotion approval |
| Tray/menu doorway standard | Not ready | F3-FF01 provides durable resident-access direction, but real tray/menu proof, Windows tray limitation proof, settings/quick-access routing proof, and USER acceptance are missing | Yes, after proof/waiver | USER visual acceptance plus promotion approval |

| Blocker | Current Status | Cleared By This Cycle? | Reason | Next Legal Action |
| --- | --- | --- | --- | --- |
| `Current Branch Template Work Incomplete` | Active | No | Package C packet is generated as evidence only; Package C proof remains incomplete and Packages D-E remain current-PR scope | USER disposition on Package C or continuation to Package D while A-C remain blocked |
| `Golden Reference Promotion Blocked` | Active | No | No USER-approved Package C promotion packet, catalog record, or final disposition exists | Approve later proof collection, USER-provided proof intake, waiver, or promotion for a named candidate |
| `Promoted Reference Count: 0` | Preserved / blocking for claims of promoted references | No | Empty catalog remains correct until USER approves a catalog promotion record | Keep count zero until a valid promotion record exists |
| Package A proof incomplete | Active | No | Top-level window/control-cluster proof is not completed by Package C | Resolve Package A separately or explicitly reclassify it |
| Package B proof incomplete | Active | No | Button/dropdown/menu/list/filter proof is not completed by Package C | Resolve Package B separately or explicitly reclassify it |
| Package C proof incomplete | Active | No | Modal/dialog, status/failure/recovery, and tray/menu doorway proof are classified but not collected, waived, accepted, or promoted | Choose Package C proof intake, waiver, reject/defer disposition, or continue to Package D with Package C blocked |
| Packages D-E incomplete | Active | No | Design-token/shared-rule authority and negative example/helper/validator expectations are outside this Package C receipt | Continue to Package D, then Package E, before final hardening unless USER reclassifies lanes |

Package C Packet Boundary: This pass does not promote references, create catalog records, create templates, implement design tokens/shared primitives, mutate helpers/validators/fixtures, mutate FAM-003/FAM-006/FAM-007/main worktrees, mutate external state, create issues, create a PR, merge, release, move/delete/archive repo files outside clean USER packet regeneration, or accept USER visual proof. `Docs/ui_reference_catalog/index.md` remains `Promoted Reference Count: 0`.

Package C Next Legal Use: USER must review the generated Package C packet and choose one of these legal paths: approve later proof collection or USER-provided proof intake for named Package C lanes; approve a narrow USER waiver/promotion route for a named Package C candidate; reject or defer named Package C candidates; or proceed to Package D while Packages A, B, and C remain blocked. Package C is not reclassified out of current PR scope unless USER later says so explicitly.

## Template / Golden Reference Package D Packet - 2026-06-17

Document Status: Non-Binding Promotion-Packet Generation Receipt. Binding authority remains with `Docs/nexus_vision.md` for Project UI Vision and proof hierarchy, `Docs/family_visions/FAM-002_desktop_interface.md` for reusable Desktop Interface presentation grammar and component anatomy, `Docs/family_feature_visions/F2-FF01.md` for UI reference-system deferred design-token/shared-primitive lanes and missing-proof boundaries, `Docs/ui_reference_catalog/` for promoted UI reference records only after explicit USER promotion approval, `Docs/phase_governance.md` for `Shared Primitive Promotion Blocked` and template/reference blocker routing, and `Docs/user_test_summary_guidance.md` for USER-facing visual-proof interpretation.

Package D Scope: `Design Tokens And Shared UI Rules` only. This includes design-token standards, shared UI rules, visual grammar constants, reusable style constraints, color/spacing/typography/elevation/border/radius/state-token expectations, accessibility/contrast expectations, and future adoption routing. Package A top-level window/control-cluster proof, Package B control proof, and Package C surface-class proof remain incomplete. Package E negative example/helper/validator expectations remain current-PR scope but are not reviewed by this Package D receipt.

Package D Result: `PROMOTION PACKET GENERATED - NO PROMOTION`. Existing FAM-006 HUD and PR #269 FAM-007 AI Control Center evidence are useful candidate evidence for later token extraction, but no design token, shared primitive, CSS module, component library, catalog reference, or reusable implementation is created or promoted here. `Docs/ui_reference_catalog/index.md` remains at `Promoted Reference Count: 0`.

| Lane | Candidate Evidence | Current Proof Status | Missing Proof | Disposition | Can Continue Without Stopping? | Later Approval Needed |
| --- | --- | --- | --- | --- | --- | --- |
| Design token standards | Project UI Vision readability/standard-control language; FAM-002 component anatomy covering size, spacing, radius, border, shadow, glow, density, typography, color, contrast, and state treatment; F2-FF01 deferred design-token lane; HUD/FAM-006 and AI Control Center candidate visuals | Existing proof available but insufficient | Token taxonomy, naming scheme, owner file/location, color/typography/spacing/radius/elevation/border/state token inventory, code-to-visual trace, cross-surface comparison, contrast proof, migration/adoption plan, rollback, and USER visual acceptance | `REVISE - candidate extraction evidence only` | Yes | Later implementation carrier and USER approval for token creation/promotion |
| Shared UI rules | FAM-002 reusable presentation grammar; F2-FF01 shared-primitive deferred lane; visual inheritance matrix and element-group proof rules; candidate HUD/AI surfaces | Existing proof available but insufficient | Rule scope, allowed specialization, exception schema, reference dependency ordering, adoption trigger, target-FAM carrydown, no-live-state boundary, visual parity proof, and USER acceptance | `REVISE - rule direction only` | Yes | Later source-truth or implementation approval before shared rules become code primitives |
| Visual grammar constants | FAM-002 Nexus-native chrome, controls, density, typography, contrast, disabled/degraded/recovery states; F2-FF01 reference classes; existing screenshots/videos | Existing proof available but insufficient | Accepted baseline values or ranges, surface-class applicability, non-applicable/platform exceptions, all visual states, token-to-reference mapping, negative examples, and USER visual acceptance | `DEFER - proof missing` | Yes | Later proof collection, USER waiver, or promotion approval |
| Reusable style constraints | FAM-002 component anatomy; phase proof hierarchy; catalog schema for future promoted references | Existing proof available but insufficient | Constraint hierarchy, override policy, feature-specific specialization rule, no-CSS-by-inference rule, adoption/rebaseline path, and validation expectations | `DEFER - implementation unapproved` | Yes | Later implementation/template approval if constraints become code or fixtures |

| Token / Rule Area | Purpose | Candidate Source | Required States | Missing Proof | Promotion Readiness |
| --- | --- | --- | --- | --- | --- |
| Color tokens | Preserve Nexus color identity, contrast, status meaning, danger/blocked states, and privacy/status clarity | FAM-002 grammar; HUD/FAM-006; AI Control Center candidate evidence | Normal, hover, focus, pressed, selected, disabled, blocked, loading, empty, error, recovery, danger, success, warning, info | Accepted palette, contrast proof, theme/skin boundary, state mapping, USER visual acceptance | Not ready |
| Typography tokens | Preserve readable titles, labels, body text, metadata, button text, status labels, and proof surfaces | Project readability vision; FAM-002 component anatomy; candidate screenshots | Default, dense, large title, small metadata, disabled, error, warning, status, button/control text | Font/weight/size/line-height inventory, platform fallback, scaling/accessibility proof, USER acceptance | Not ready |
| Spacing and density tokens | Keep windows predictable, immersive, and not visually noisy across feature surfaces | FAM-002 spacing/density grammar; HUD and AI Control Center layout evidence | Compact, default, spacious, list row, card, panel, modal, tray/menu, error/recovery | Baseline grid, responsive rules, minimum/maximum spacing, overflow behavior, USER acceptance | Not ready |
| Border/radius/elevation/glow tokens | Preserve shared shape language, depth, control grouping, focus, and hover/active affordances | FAM-002 component anatomy; window/control-cluster evidence | Normal, hover, focus, pressed, disabled, blocked, active, elevated/modal, error/recovery | Accepted values/ranges, surface applicability, focus/glow proof, platform exceptions, USER acceptance | Not ready |
| State tokens | Make UI state deterministic and tied to runtime truth rather than ad hoc color changes | FAM-002 state expectations; phase claim/evidence model; F2-FF01 missing-proof rows | Normal, hover, focus, pressed, selected, dirty, disabled, blocked, loading, empty, error, recovery | State taxonomy, runtime-truth mapping, conflict priority, accessibility/non-color proof, USER acceptance | Not ready |
| Shared UI rule hierarchy | Decide when feature surfaces inherit, specialize, or request exceptions from Project/FAM-002/F2-FF01 grammar | FAM-002 presentation authority; Scope Coverage and Visual Inheritance rules | All UI-bearing branches, especially top-level windows, child/modal/dialog, controls, status panels, tray/menu surfaces | Owner file placement, override/exception schema, adoption routing, helper/validator future guidance | Not ready |

| Candidate Standard | Promotion Readiness | Reason | Can Promote In Later Packet? | Later USER Approval Needed |
| --- | --- | --- | --- | --- |
| Design token standard | Not ready | Durable ownership direction exists, but token files, accepted values, cross-surface proof, contrast proof, and implementation authority are missing | Yes, after references/proof and implementation approval | USER approval for token creation/promotion and visual acceptance |
| Shared UI rule standard | Not ready | FAM-002 grammar is binding, but code-level shared rules and reusable primitive behavior are not implemented or accepted | Yes, after source-truth/implementation approval | USER approval for shared-rule promotion and adoption plan |
| Visual grammar constants | Not ready | Candidate evidence exists, but accepted constants/ranges and applicability exceptions are not proven | Yes, after proof/waiver | USER visual acceptance plus promotion approval |
| Reusable style constraints | Not ready | Constraint direction is useful, but no approved implementation carrier, fixtures, or validator enforcement exists | Yes, after implementation/fixture approval | USER approval for implementation or fixture/helper/validator carrier |

| Blocker | Current Status | Cleared By This Cycle? | Reason | Next Legal Action |
| --- | --- | --- | --- | --- |
| `Current Branch Template Work Incomplete` | Active | No | Package D packet is generated as evidence only; Package D design-token/shared-rule implementation remains unapproved and Package E remains current-PR scope | USER disposition on Package D or continuation to Package E while A-D remain blocked |
| `Golden Reference Promotion Blocked` | Active | No | No USER-approved Package D promotion, catalog record, or final disposition exists | Approve later proof collection, USER-provided proof intake, waiver, or promotion for a named candidate |
| `Shared Primitive Promotion Blocked` | Active | No | This cycle does not implement design tokens, shared UI primitives, shared CSS, reusable components, fixtures, helpers, or validators | Approve a later implementation/template carrier only after proof and ownership are accepted |
| `Promoted Reference Count: 0` | Preserved / blocking for claims of promoted references | No | Empty catalog remains correct until USER approves a catalog promotion record | Keep count zero until a valid promotion record exists |
| Packages A-C proof incomplete | Active | No | Package D does not complete earlier visual-reference proof lanes | Resolve or explicitly reclassify Packages A-C |
| Package D proof incomplete | Active | No | Design-token/shared-rule proof is classified but not collected, waived, accepted, implemented, or promoted | Choose Package D proof intake, implementation planning, waiver, reject/defer disposition, or continue to Package E with Package D blocked |
| Package E incomplete | Active | No | Negative examples/helper/validator expectations are outside this Package D receipt | Continue to Package E before final hardening unless USER reclassifies lanes |

Package D Packet Boundary: This pass does not implement design tokens, create shared primitives, create shared CSS/components, create fixtures, mutate helpers/validators, promote references, create catalog records, create templates, mutate FAM-003/FAM-006/FAM-007/main worktrees, mutate external state, create issues, create a PR, merge, release, move/delete/archive repo files outside clean USER packet regeneration, or accept USER visual proof. `Docs/ui_reference_catalog/index.md` remains `Promoted Reference Count: 0`.

Package D Next Legal Use: USER must review the generated Package D packet and choose one of these legal paths: approve later proof collection or USER-provided proof intake for named Package D lanes; approve a later design-token/shared-rule implementation-planning carrier; approve a narrow USER waiver/promotion route for a named Package D candidate; reject or defer named Package D candidates; or proceed to Package E while Packages A-D remain blocked. Package D is not reclassified out of current PR scope unless USER later says so explicitly.

## Template / Golden Reference Scope Lock And Candidate-Disposition Digestion - 2026-06-17

Document Status: Non-Binding Scope-Lock Receipt. Binding authority remains with `Docs/nexus_vision.md` for Project UI Vision and proof hierarchy, `Docs/family_visions/FAM-002_desktop_interface.md` for reusable Desktop Interface presentation grammar, `Docs/family_feature_visions/F2-FF01.md` for the UI reference-system feature-category vision, missing-proof rows, deferred candidate preservation, and BR/BP context, `Docs/ui_reference_catalog/` for promoted reference records only after explicit USER promotion approval, and `Docs/phase_governance.md` for PR-hold and blocker routing.

Accepted Evidence Packet: `C:\Nexus USER\Governance-20260617-095237.zip` with SHA256 `5FBE740389D8B011DBF0B2A4A460202732070E3FFDE1698BF1A6D4A02E8A69EF` and `35` files is accepted as reviewable evidence only. It does not promote a reference, create a template, create design tokens/shared primitives, mutate helpers/validators/fixtures, mutate FAM worktrees, mutate external operational state, create a PR, merge, release, create or close issues, move/delete/archive files, or clear `Current Branch Template Work Incomplete`.

Scope-Lock Result: Governance / FAM-002 owns reusable template/reference authority creation or promotion. Target FAMs consume approved references later in their own legal worktrees after merge/rebaseline. A target FAM may produce candidate evidence while building, but that evidence remains candidate-only until routed back through the Governance / FAM-002 promotion path.

Scope Correction: USER clarified that the previously deferred template/reference authority lanes remain inside the current Governance branch / current intended PR scope. The only lanes deferred out of this Governance PR are active FAM-006 adoption mutation, active FAM-007 adoption mutation, and future target-FAM implementation changes that consume the approved standards after merge/rebaseline. FAM-003 resident access and Global Settings / settings-category surfaces must be considered before PR because FAM-003 owns resident doorway behavior, Global Settings entry/routing, quick-access slots, and compact resident UI while consuming FAM-002 presentation grammar. This correction does not authorize actual golden-reference promotion, catalog promoted-reference record creation, template creation, design-token/shared-primitive implementation, helper/validator/fixture mutation, runtime work, FAM-003/FAM-006/FAM-007/main mutation, external-state mutation, PR creation, merge, release, issue mutation, cleanup, or USER visual acceptance. If older historical receipts or classification rows in this planning file describe broader template/reference lanes as deferred, future, or separate-carrier leaning, this Scope Correction supersedes them for the current branch posture: Packages A through E are current-PR planning/authority scope, while their promotion, code, fixture, runtime, catalog-record, and target-FAM adoption mutations still require later exact USER approval.

Authority Split:

| Authority Area | Governance/FAM-002 Responsibility | Target-FAM Responsibility | Candidate Evidence Path | Current PR Requirement | Later Adoption Requirement |
| --- | --- | --- | --- | --- | --- |
| Golden window reference | Define/promote reusable top-level Nexus window reference through FAM-002/F2-FF01/catalog path | Consume the promoted reference when creating or repairing eligible windows | HUD/FAM-006 and PR #269 AI Control Center remain candidate evidence | Current-branch authority work; promotion still requires USER visual approval | Target FAMs reconcile at next legal gate after merge |
| Window control cluster and close/minimize/maximize pill | Define/promote compact Nexus-native control grammar by window class | Apply the approved cluster or record a USER-approved exception | AI Control Center cluster remains candidate evidence | Current-branch next package candidate | Target FAMs prove adoption or exception in BP/Hardening/LV |
| Buttons, dropdowns, menus, lists, filters | Define reference classes, state coverage, and promotion proof requirements | Implement feature-specific controls using approved grammar | Existing FAM surfaces may provide candidate evidence | Current-branch authority work if admitted; no code/template implementation yet | Target FAMs consume after reference promotion or use FAM-002 grammar manually |
| Modal/dialog and status/failure/recovery panels | Define reusable surface classes and platform-native exception grammar | Implement feature-specific dialogs, failure states, and recovery UI | FAM-001/FAM-006/FAM-007 evidence may support future reference review | Current-branch authority work if admitted; no product mutation | Target FAMs repair or document exceptions at their own legal gate |
| Tray/menu doorway and Global Settings references | Preserve doorway/settings grammar with FAM-003 behavior split and FAM-002 presentation split | Implement resident access, quick actions, AI status, settings categories, or setup education in owning FAMs | F3-FF01, future tray proof, and future Global Settings proof are candidate evidence | Current-branch authority work; no FAM-003 runtime mutation | Target FAMs adopt when tray/settings/runtime work is admitted |
| Design tokens and shared UI rules | Decide durable ownership and promotion prerequisites after references are stable | Consume tokens/primitives only after they are approved | CSS or component reuse remains evidence, not a standard | Current-branch authority scope; implementation requires later approval | Target FAMs migrate only after approved token/primitive carrier merges |
| Negative examples / bad fixtures | Define bad-example classes and future enforcement expectations | Avoid known-bad patterns and provide candidate defect evidence | PR review/LV failures may become negative fixture candidates | Current-branch authority scope; fixture mutation requires later approval | Target FAMs consume once fixtures/validators exist |
| Helper and validator expectations | Record future machine-check guidance without overclaiming current enforcement | Treat validators as evidence and still perform manual proof | Failed packets and review comments feed future fixtures | Current-branch authority scope; code mutation requires later approval | Target FAMs run updated checks after merge |
| Target-FAM adoption | Define the reusable standard and adoption routing only | FAM-006, FAM-007, and future FAMs repair their own branch-local UI under their own legal carriers | Candidate evidence routes back through Governance/FAM-002 before becoming standard | Not required before this Governance PR | Required at each affected worktree's next legal gate |

Lane Classification:

| Lane | Current-PR Scope? | Current Status | Required Proof / Work | Actual Promotion Needed Later? | Legal Carrier | USER Approval Needed |
| --- | --- | --- | --- | --- | --- | --- |
| HUD/FAM-006 surface reference | Yes | `REVISE`; candidate evidence only | USER visual approval or revise/defer/reject disposition, state proof, consuming-FAM ownership confirmation | Yes, before catalog promotion | Governance/FAM-002 promotion path | USER visual promotion or explicit reclassification |
| PR #269 AI Control Center surface reference | Yes | `REVISE`; candidate evidence only | Compare against Project UI Vision, FAM-002, F2-FF01, HUD, FAM-007 boundaries, and proof hierarchy | Yes, before catalog promotion | Governance/FAM-002 promotion path | USER visual promotion or explicit reclassification |
| Golden window reference | Yes | `REVISE`; missing promoted reference | Promotion packet with applicability, limitations, proof artifacts, and final disposition | Yes | Governance/FAM-002 plus UI catalog | USER promotion approval |
| Golden control-cluster reference | Yes | `REVISE`; candidate-only | Applicability matrix for close/minimize/maximize/restore/blocked controls by window class | Yes | Governance/FAM-002 plus UI catalog | USER promotion approval |
| Close/minimize/maximize cluster standard | Yes | `REVISE`; should group with control cluster | Element-group state proof, accessibility/hitbox proof, and top-level/child-window distinction | Yes, if promoted as catalog reference | Governance/FAM-002 plus UI catalog | USER promotion approval |
| Button standards | Yes | Missing-proof authority lane | State matrix and positive/negative examples for primary/secondary/danger/disabled/hover/focus/pressed states | Yes, if promoted as catalog reference/template | Governance/FAM-002 | USER admission/promotion approval |
| Dropdown standards | Yes | Missing-proof authority lane | Open/closed/hover/focus/selected/disabled/empty/overflow proof | Yes, if promoted | Governance/FAM-002 | USER admission/promotion approval |
| Menu standards | Yes | Missing-proof authority lane | Menu body, row, nesting-depth, compactness, keyboard/focus, and overflow proof | Yes, if promoted | Governance/FAM-002 | USER admission/promotion approval |
| List standards | Yes | Missing-proof authority lane | List-row, selected, empty, disabled, scroll, density, and proof expectations | Yes, if promoted | Governance/FAM-002 | USER admission/promotion approval |
| Filter standards | Yes | Missing-proof authority lane | Filter trigger, state, empty-result, reset, disabled, and accessibility proof | Yes, if promoted | Governance/FAM-002 | USER admission/promotion approval |
| Modal/dialog standards | Yes | Missing-proof authority lane | Modal/child/top-level/platform exception taxonomy and dialog proof | Yes, if promoted | Governance/FAM-002 | USER admission/promotion approval |
| Status/failure/recovery panel standards | Yes | Missing-proof authority lane | FAM-001 meaning, FAM-002 presentation, truth mapping, and recovery proof | Yes, if promoted | Governance/FAM-002/FAM-001 routed package | USER admission/promotion approval |
| Tray/menu doorway standards | Yes | Missing-proof authority lane with FAM-003 dependency | Tray doorway proof, Windows tray limits, quick-access budget, and link-to-owning-surface proof | Yes, if promoted | Governance/FAM-002/F3-FF01 routed package | USER admission/promotion approval |
| Global Settings / settings-category surface standards | Yes | Missing-proof authority lane with FAM-003 dependency | Settings window/category shell, feature section grouping, quick-access configuration, reset-route presentation, and ownership routing proof | Yes, if promoted | Governance/FAM-002/F3-FF01 routed package | USER admission/promotion approval |
| Design tokens and shared UI rules | Yes | Current-PR authority scope; implementation not approved by this pass | Token ownership, naming, state mapping, and code-to-visual trace plan before implementation | Not catalog promotion, but implementation/promotion approval is required | Governance/FAM-002 future implementation/template carrier | USER implementation approval |
| Negative examples / bad fixtures | Yes | Current-PR authority scope; fixture mutation not approved by this pass | Bad examples for default OS chrome, unproven references, weak proof, mismatched states, command-wall settings, and overgrown tray menus | No catalog promotion, but fixture approval is required | Future helper/validator/fixture carrier | USER fixture/code approval |
| Helper/validator expectations | Yes | Current-PR authority scope; code mutation not approved by this pass | Machine-check expectations after false-positive review and fixture coverage | No catalog promotion, but helper/validator approval is required | Future helper/validator carrier | USER code approval |
| Active FAM-006 adoption mutation | No | Deferred target-FAM adoption | Rebaseline adoption packet and branch-local repair in FAM-006 | No | FAM-006 worktree at next legal gate | USER approval in FAM-006 carrier |
| Active FAM-007 adoption mutation | No | Deferred target-FAM adoption | Rebaseline adoption packet and branch-local repair in FAM-007 | No | FAM-007 worktree at next legal gate | USER approval in FAM-007 carrier |

Grouped Packages:

| Package | Included Lanes | Why Grouped | Current-PR Required? | Can Start Next? | Requires Later Approval For Mutation/Promotion? | Recommended Action |
| --- | --- | --- | --- | --- | --- | --- |
| Package A - Top-Level Window And Window Control Cluster | HUD/FAM-006 surface, AI Control Center surface, golden window reference, golden control-cluster reference, close/minimize/maximize standard | These decide the global top-level window baseline and the shared element group most responsible for recent UI drift | Yes | Yes | Yes for USER visual promotion or catalog records | Prepare the next promotion-review / planning packet for these lanes first |
| Package B - Controls, Menus, Lists, And Filters | Button standards, dropdown standards, menu standards, list standards, filter standards | Shared state coverage, interaction anatomy, and bad-example needs overlap | Yes | After Package A or if USER prioritizes controls | Yes for any template, reference record, fixture, helper, or validator mutation | Build state matrix and proof requirements for all basic controls |
| Package C - Surface Classes, Settings, And Doorways | Modal/dialog standards, status/failure/recovery panels, tray/menu doorway standards, Global Settings / settings-category surfaces | These define where users go, how failures/recovery appear, and how FAM-003 Global Settings/tray surfaces remain coherent without becoming a command wall | Yes | After Package A unless USER prioritizes FAM-003 settings/tray standards | Yes for runtime/tray/settings implementation or catalog promotion | Include FAM-003/F3-FF01 as a required source owner and keep runtime implementation deferred |
| Package D - Design Tokens And Shared UI Rules | Design tokens and shared UI rules | Code-level reuse should follow accepted visual references, but the governance authority lane remains in this PR scope | Yes | After visual reference decisions are stable | Yes for design-token/shared-primitive implementation | Define ownership, naming, state mapping, and no-live-state boundaries before implementation |
| Package E - Negative Fixtures And Helper/Validator Expectations | Negative examples / bad fixtures, helper and validator expectations | Machine checks need approved references or precise rules to avoid false positives and Codex comment loops | Yes | After enough reference rules exist to avoid brittle checks | Yes for helper/validator/fixture mutation | Define expected failures and enforcement plan before code mutation |
| Final Package - Integration Hardening And PR Readiness Stage 1 | Full branch diff, source-owner alignment, no-live-state checks, catalog count, scope completeness, and validation | Confirms no package introduced drift or unfinished current-PR authority lanes | Yes | Only after Packages A-E are completed or explicitly reclassified | PR Readiness requires separate USER approval | Run final integration hardening, then request PR Readiness Stage 1 only if blockers clear |
| Target-FAM Adoption Package | FAM-006/FAM-007/future FAM reconciliation | Adoption belongs to each target worktree after merge/rebaseline | No | No | Yes inside each target carrier | Defer to each target FAM's next legal gate |

Before-PR Completion Requirements:

| Required Before Governance PR | Status | Source Owner | Remaining Work | Blocker If Not Done | USER Reclassification Possible? |
| --- | --- | --- | --- | --- | --- |
| Scope-lock digestion recorded | Completed by this section when committed | This plan plus branch record receipt | Validate and push | Scope ambiguity remains | Not needed |
| UI catalog exists and remains empty until promotion | Completed | `Docs/ui_reference_catalog/` | None; `Promoted Reference Count: 0` is required | `Template Treated As Existing Proof` | No |
| FAM-002 / F2-FF01 ownership split clear | Completed | FAM-002, F2-FF01, catalog README | None found | Ownership ambiguity | No |
| Package A - top-level window and control-cluster authority | Proof-route decision recorded; promotion proof remains unresolved | FAM-002/F2-FF01/catalog | USER chooses USER-provided proof intake, later FAM/runtime proof routing, narrow waiver/promotion route, reject/defer path, or Package B continuation while Package A remains blocked | `Current Branch Template Work Incomplete` | Yes, but must be explicit |
| Package B - controls/menu/list/filter authority | Packet generated; promotion proof remains unresolved | FAM-002/F2-FF01/catalog | USER reviews Package B packet and chooses proof intake, narrow waiver/promotion route, reject/defer path, or Package C continuation while Package B remains blocked | `Current Branch Template Work Incomplete` | Yes, but must be explicit |
| Package C - modal/status/tray/Global Settings authority | Packet generated; promotion proof remains unresolved | FAM-002/F2-FF01/F3-FF01 | USER chooses proof intake, narrow waiver/promotion route, reject/defer path, or Package D continuation while Package C remains blocked | `Current Branch Template Work Incomplete` | Yes, but must be explicit |
| Package D - design-token/shared-rule authority | Packet generated; implementation/promotion proof remains unresolved | Future implementation/template carrier after FAM-002/F2-FF01 | USER chooses proof intake, implementation-planning carrier, narrow waiver/promotion route, reject/defer path, or Package E continuation while Package D remains blocked | `Current Branch Template Work Incomplete` | Yes, but must be explicit |
| Package E - fixtures/helper/validator expectations | Packet generated; helper/validator/fixture implementation remains unresolved | Validation registry/future code carrier | USER chose continued proof/promotion work for all Packages A-E; Package E automation waits until visual proof/reference lanes are clearer unless USER separately approves helper/validator/fixture mutation | `Current Branch Template Work Incomplete` | Yes, but must be explicit |
| Target-FAM adoption | Deferred to target FAMs after merge/rebaseline | Affected FAM worktrees at next legal gate | Each FAM inventories, repairs, waives, or issue-candidates its own surfaces | Target-FAM gate blocker later, not Governance PR blocker | No need; already outside this PR |

Current PR Posture: `Current Branch Template Work Incomplete` remains active. PR Readiness remains blocked until Packages A-E complete, or USER explicitly reclassifies a named remaining lane out of current PR scope. Package A has completed review, missing-proof packet generation, and proof-route classification, but remains unresolved for promotion. Package B has completed packet generation and missing-proof classification, but remains unresolved for promotion because promotion-grade proof is missing and no catalog record is promoted. Package C has completed packet generation and missing-proof classification, but remains unresolved for promotion because modal/dialog, status/failure/recovery, tray/menu doorway, and settings-category proof is missing. Package D has completed packet generation and missing-proof classification, but remains unresolved because design-token/shared-rule implementation, visual constants, contrast proof, adoption routing, and USER acceptance remain unapproved. Package E has completed packet generation and expectation classification, but remains unresolved because helper/validator/fixture code mutation, executable negative-example fixtures, and enforcement validation remain unapproved. Final integration hardening and blocker-disposition digestion have now recorded the remaining blockers without clearing, waiving, rejecting, deferring, promoting, or reclassifying them. The recommended next action is the Package A USER-provided proof intake / promotion-route packet for top-level window and window-control cluster. Packages A-E are not reclassified out of current PR scope unless USER later says so explicitly.

## Template / Golden Reference Package E Packet - 2026-06-17

Document Status: Non-Binding Package Review Receipt. Binding authority remains with `Docs/nexus_vision.md` for Project UI Vision and proof hierarchy, `Docs/family_visions/FAM-002_desktop_interface.md` for Desktop Interface presentation grammar, `Docs/family_feature_visions/F2-FF01.md` for UI reference-system missing-proof rows and enforcement expectations, `Docs/ui_reference_catalog/` for USER-promoted reference records only after explicit promotion approval, `Docs/validation_helper_registry.md` for future helper/validator guidance, and `Docs/phase_governance.md` for proof/blocker routing.

Package E Scope: `Negative Examples, Bad Fixtures, Helper Expectations, And Validator Expectations` only. Reviewed lanes are anti-pattern categories, future bad-fixture classes, helper expectations, validator expectations, false-green prevention, missing-proof/no-overclaim classification, and PR-review risk expectations. Package A window/control proof, Package B control/menu/list/filter proof, Package C modal/status/tray/settings proof, Package D design-token/shared-rule implementation, catalog promotion, actual template creation, helper/validator/fixture code mutation, and target-FAM adoption remain outside this Package E execution scope.

Package E Result: `PROMOTION PACKET GENERATED - NO CODE OR FIXTURE MUTATION`. Governance generated a USER-reviewable packet that defines the negative-example classes and future enforcement expectations needed to prevent false greens and Codex review loops. It does not create executable fixtures, mutate helpers, mutate validators, promote references, create templates, create catalog records, implement design tokens/shared primitives, mutate FAM worktrees, mutate external state, create issues, create a PR, merge, release, or clear `Current Branch Template Work Incomplete`.

| Anti-Pattern / Bad Fixture Category | Why It Is Bad | Evidence Source | Future Fixture Needed? | Helper/Validator Expectation | Later Approval Needed |
| --- | --- | --- | --- | --- | --- |
| Default Windows chrome where Nexus-owned chrome is required | Breaks Project UI immersion and bypasses FAM-002 window grammar | Project UI Vision, FAM-002 grammar, F2-FF01 missing-proof rows, PR #269 AI Control Center evidence | Yes | Flag Nexus-owned surfaces that lack admitted Nexus chrome or an approved platform exception | USER approval for fixture/helper/validator mutation |
| Oversized or inconsistent close buttons | Turns window-control language into branch-local styling and risks FAM-006/FAM-007 drift | Package A proof-route findings, HUD/FAM-006 comparison evidence, FAM-002 control grammar | Yes | Require control-class classification and state proof before a close/minimize/maximize candidate can be promoted | USER approval for fixture/helper/validator mutation |
| Missing close/minimize/maximize state proof | Lets a single attractive screenshot stand in for required default/hover/focus/pressed/disabled/blocked states | Package A missing-proof matrix, AI Control Center duplicate-hash hover finding | Yes | Require state matrix coverage or explicit missing-proof row | USER approval for fixture/helper/validator mutation |
| Attractive screenshot without state coverage | Creates false confidence from one good-looking frame while interaction states remain unproven | USER proof hierarchy, Vision-To-Proof Matrix, Scope Coverage Manifest | Yes | Report visual evidence as candidate-only until required states and applicability are proven | USER approval for fixture/helper/validator mutation |
| Duplicate screenshot treated as independent proof | Produces false hover/state proof and hides missing evidence | Package A proof-route classification noted identical AI Control Center default/minimize-hover hashes | Yes | Detect duplicate visual hashes and classify claimed independent state proof as missing | USER approval for fixture/helper/validator mutation |
| Markdown-only visual proof | Replaces USER-visible proof with prose and bypasses photo/video or manual validation requirements | Project proof hierarchy, User Test Summary guidance | Yes | Reject visible UI acceptance claims that lack image/video/frame-sequence proof or USER waiver | USER approval for fixture/helper/validator mutation |
| Validator green treated as visual acceptance | Confuses helper evidence with USER acceptance and repeats prior false-green patterns | Validation helper registry, incident patterns, prior review-loop findings | Yes | Require Codex review of validation adequacy and USER visual acceptance for promoted references | USER approval for fixture/helper/validator mutation |
| Missing Scope Coverage Manifest | Allows partial inspection to masquerade as complete UI review | Phase governance, F2-FF01 proof expectations | Yes | Require manifest coverage for affected surfaces, element groups, and proof claims | USER approval for fixture/helper/validator mutation |
| Missing Vision-To-Proof mapping | Lets implementation drift from Project/FAM/FFV contracts without explicit comparison | Vision carrydown contract, phase governance | Yes | Require claims to cite vision owner, observed behavior, proof artifact, and disposition | USER approval for fixture/helper/validator mutation |
| Target-FAM candidate silently treated as canonical standard | Promotes FAM-006/FAM-007 evidence by inference instead of through FAM-002/catalog authority | F2-FF01, UI catalog empty-count rule, Package A-D receipts | Yes | Block promoted-reference claims unless a catalog record and USER promotion receipt exist | USER approval for fixture/helper/validator mutation |
| Promoted reference count inconsistent with catalog records | Creates canon drift between the catalog index and reference files | `Docs/ui_reference_catalog/index.md` and catalog README | Yes | Validate count, record list, and promotion receipts together | USER approval for fixture/helper/validator mutation |
| Token/shared-rule claims without implementation authority | Treats Package D planning as code-level shared primitives without USER implementation approval | Package D packet receipt and source-truth carrier rules | Yes | Flag token/shared-primitive claims unless an approved implementation carrier exists | USER approval for fixture/helper/validator mutation |
| FAM adoption mutation attempted inside Governance carrier | Violates worktree boundaries and would mutate target-FAM runtime/source truth from the wrong lane | Standing Governance branch record, F2-FF01 cross-FAM dependency map | Yes | Enforce consumer/context-only treatment for FAM-003/FAM-006/FAM-007/FAM-008 during Governance passes | USER approval for fixture/helper/validator mutation |

| Helper Expectation | Purpose | Current Coverage | Missing Coverage | Future Carrier | Blocks PR Readiness? |
| --- | --- | --- | --- | --- | --- |
| Packet stage verification | Prevent stale or wrong-stage USER packets | Clean packet regeneration rule exists in validation registry; generic local packet validation now scans generated packet surfaces for stale stage / unresolved placeholder drift | Package-specific semantic identity proof may still be added later if a future packet family needs stricter stage semantics | Existing `dev/orin_user_review_bundle.py` validation mode plus fixture coverage; future extension only if new false-green appears | Yes while current-PR package packet proof is required |
| Folder/ZIP/hash/file-count verification | Prevent folder/ZIP drift and stale upload artifacts | USER packet rule requires timestamped ZIP and folder/list validation; helper now validates existing local packets for stale same-label ZIPs, stable ZIP rejection, one-primary review file, file-class layout, and folder/ZIP file-list plus content-hash parity | Optional package-specific hash summary remains future-only and must keep hash proof out of USER-facing files | Existing `dev/orin_user_review_bundle.py` validation mode plus fixture coverage; future visual/hash helper only for image-proof lanes | Yes for packet reviewability when generated |
| Promoted-reference count check | Keep catalog index and promoted records consistent | Catalog index owns `Promoted Reference Count: 0`; docs inventory classifier recognizes the catalog | Automated catalog count/record/receipt cross-check | Future governance validator extension | Yes if any promoted-reference claim appears |
| Missing-proof row enforcement | Prevent candidate evidence from becoming proof by inference | F2-FF01 and Package A-D rows preserve missing proof | Machine checks for required row fields and unresolved disposition | Future governance validator/fixture carrier | Yes while promotion is claimed or PR scope requires closure |
| Candidate evidence versus promoted reference separation | Protect repo docs from golden-reference overclaim | UI catalog README and F2-FF01 define the boundary | Helper report when packet prose calls candidate evidence a promoted reference | Future packet helper/validator carrier | Yes for any promotion/reference claim |
| Scope Coverage Manifest presence | Ensure Codex inspected all affected surfaces and states | Phase governance owns the requirement | Automated packet/diff scan for missing coverage manifest | Future branch readiness / PR readiness helper extension | Yes when UI proof completeness is claimed |
| Vision-To-Proof Matrix presence | Tie observed UI behavior back to Project/FAM/FFV contracts | Phase governance and vision contract rules exist | Automated packet scan for missing vision/proof mapping | Future branch readiness / LV helper extension | Yes when UI/proof claims are made |
| Stale packet detection | Stop old stage, old package, or old ZIP content from passing | USER packet clean-regeneration rule exists | Package A-E identity fixtures and stale-title/body checks | Future packet helper fixtures | Yes for packet reviewability |
| Duplicate visual proof hash detection | Prevent duplicate screenshots from proving different states | Package A manually found duplicate hash risk | Automated image hash inventory and state-claim comparison | Future visual proof helper carrier | Yes if visual proof is being used to promote or clear a state |
| False-green risk reporting | Make validators tools, not authority | Validation helper registry requires adequacy review | Standardized false-green risk section in package/PR packets | Future helper/template updates | Yes when unreported false-green risk affects current scope |

| Validator Expectation | Purpose | Current Coverage | Missing Coverage | Future Carrier | Blocks PR Readiness? |
| --- | --- | --- | --- | --- | --- |
| Source-owner validation for `Docs/ui_reference_catalog` | Keep catalog ownership discoverable and not unknown-docs drift | Docs inventory helper classification repaired | Full promoted-record schema validation | Future source-owner/governance validator carrier | No unless catalog claims promotion |
| Promoted-reference count consistency | Ensure index count matches promoted records | Manual zero-count verification in current packets | Automated count/record/promotion receipt consistency | Future governance validator extension | Yes if any promoted records exist or are claimed |
| Packet regeneration shape | Enforce root `START_HERE`, `USER Review`, `Review Aids`, `Source Truth Context`, and timestamped ZIP | Validation registry owns shape; helper now validates existing packet folders and timestamped ZIPs for approved layout, exactly one primary review file, stale same-label ZIP absence, stable ZIP rejection, and folder/ZIP file-list plus content-hash parity | Package-specific stage semantics may still need future fixtures if a new packet family appears | Existing packet helper/fixture carrier | Yes for generated USER packet acceptance |
| No catalog promotion without USER approval | Prevent overclaiming candidate references | Catalog README and F2-FF01 prohibit inference | Machine scan for promotion language without receipt | Future governance validator extension | Yes if promotion language appears |
| No template/reference promotion without proof/approval | Keep templates and golden references USER-gated | Phase governance and F2-FF01 missing-proof rows | Fixture set for overclaim examples | Future fixture/validator carrier | Yes for PR readiness when current scope includes promotion |
| No FAM worktree mutation from Governance carrier | Preserve worktree boundary | Branch record non-includes and cross-FAM dependency map | Automated diff/path guard for target-FAM roots if available | Existing standing gate extension if needed | Yes for any Governance carrier mutation |
| PR readiness blocked while required authority lanes remain incomplete | Prevent premature PR after packet-only work | Plan and branch record carry `Current Branch Template Work Incomplete` | Automated Package A-E completion/reclassification check | Future PR-readiness validator extension | Yes until all lanes are completed or reclassified |

| Enforcement Item | Classification | Source Truth Already Sufficient? | Missing Coverage | Later Approval Needed |
| --- | --- | --- | --- | --- |
| Negative example definitions | Future negative-example catalog work | Partially, as Package E planning evidence | Executable or durable fixture files | USER approval for fixture/catalog work |
| Bad fixture examples | Future fixture work | No executable fixtures created | Positive/negative fixture corpus | USER approval for fixture mutation |
| Helper packet checks | Future helper work | Registry defines expectations | Code implementation and regression coverage | USER approval for helper mutation |
| Validator catalog/count checks | Future validator work | Source-truth boundary is clear | Code implementation and fixtures | USER approval for validator mutation |
| False-green prevention | Source truth already sufficient for manual review; future helper work for automation | Yes for rule intent | Automated reporting | USER approval for helper/validator mutation |
| Missing-proof/no-overclaim classification | Source truth sufficient for current packet | Yes | Automated row completeness checks | USER approval for validator mutation if automated |

| Blocker | Current Status | Cleared By This Cycle? | Reason | Next Legal Action |
| --- | --- | --- | --- | --- |
| `Current Branch Template Work Incomplete` | Active | No | Package E defines enforcement expectations but does not implement helper/validator/fixture code and Packages A-D remain unresolved | USER disposition on Package E, final integration hardening, or explicit reclassification of named remaining lanes |
| `Golden Reference Promotion Blocked` | Active | No | No USER-approved promotion packet or catalog record exists | Approve future promotion after proof and USER visual acceptance |
| `Promoted Reference Count: 0` | Preserved | No | Empty catalog remains correct because no reference is promoted | Keep count zero until promotion approval creates a catalog record |
| `Future Helper/Validator Enforcement` | Active | No | Package E defines expectations only; code/fixture mutation is excluded | Approve future helper/validator/fixture implementation carrier |
| `Template Treated As Existing Proof` | Avoided | Yes for this Package E packet | Packet keeps all examples as anti-pattern expectations or future fixtures, not proof | Continue blocking overclaim language |
| `Shared Primitive Promotion Blocked` | Active | No | Package E does not implement Package D design tokens/shared primitives | Approve later implementation carrier if still desired |
| `FAM Worktree Mutation Approval Missing` | Avoided | Yes for this Package E packet | FAM-003/FAM-006/FAM-007 remain consumer/context inputs only | Target FAMs reconcile/adopt later in their own legal carriers |

Package E Next Legal Use: Superseded by the later final integration hardening and blocker-disposition digestion receipts. USER chose continued proof/promotion work for Packages A-E with no waiver, rejection, deferral out of current PR scope, promotion, or PR Readiness. Package E helper/validator/fixture implementation remains future-gated until USER separately approves that code/fixture carrier; the recommended immediate next package is Package A proof intake because automation should wait until visual proof/reference lanes are clearer.

## Template / Golden Reference Final Integration Hardening Receipt - 2026-06-17

Document Status: Non-Binding Final Hardening Receipt. Binding authority remains with `Docs/nexus_vision.md`, `Docs/family_visions/FAM-002_desktop_interface.md`, `Docs/family_feature_visions/F2-FF01.md`, `Docs/family_feature_visions/F3-FF01.md`, `Docs/ui_reference_catalog/`, `Docs/phase_governance.md`, `Docs/branch_plans/README.md`, `Docs/user_test_summary_guidance.md`, and `Docs/validation_helper_registry.md`.

Hardening Result: `HARDENED - PR READINESS STILL BLOCKED`. Governance completed the current integration-hardening review for Packages A-E, the empty UI reference catalog, package-packet receipts, no-overclaim boundaries, target-FAM adoption boundaries, and validation posture. This hardening pass does not promote a reference, create a template, implement design tokens/shared primitives, mutate helpers/validators/fixtures, mutate external state, mutate FAM worktrees, create issues, create a PR, merge, release, clear `Current Branch Template Work Incomplete`, clear `Golden Reference Promotion Blocked`, or reclassify any Package A-E lane out of current PR scope.

Packet Verification Boundary: `C:\Nexus USER\Governance-20260617-120340.zip` is the only current local Governance upload ZIP after clean same-label packet regeneration. Its SHA256 is `4293349496583D87F7FC825491D1B68A9495EE70654D687D59C3D4A89E52E320`, size is `6863648` bytes, and it contains `58` files for the Package E no-code/no-fixture-mutation packet. Earlier Package A-D upload ZIPs are no longer locally byte-verifiable after the clean packet rule removed same-label stale uploads; their source-truth receipts remain historical evidence only and do not create promoted reference proof.

| Package | Current Status | Packet / Receipt Verification | Promoted Anything? | Proof Complete? | Current PR Scope? | Blocks PR Readiness? | Next Legal Action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Package A - Top-Level Window And Window Control Cluster | Proof-route decision recorded; no promotion | Source-truth receipts verified; prior local ZIP not retained after clean packet regeneration | No | No | Yes | Yes | USER proof intake, later FAM/runtime proof routing, named waiver/reclassification, reject/defer, or promotion path after proof |
| Package B - Buttons, Dropdowns, Menus, Lists, And Filters | Packet generated; no promotion | Source-truth receipt verified; prior local ZIP not retained after clean packet regeneration | No | No | Yes | Yes | USER proof intake, narrow waiver/reclassification, reject/defer, or later promotion path after proof |
| Package C - Modal/Dialog, Status/Failure/Recovery, Tray/Menu Doorway, And Settings Surfaces | Packet generated; no promotion | Source-truth receipt verified; prior local ZIP not retained after clean packet regeneration | No | No | Yes | Yes | USER proof intake, narrow waiver/reclassification, reject/defer, or later promotion path after proof |
| Package D - Design Tokens And Shared UI Rules | Packet generated; no implementation or promotion | Source-truth receipt verified; prior local ZIP not retained after clean packet regeneration | No | No | Yes | Yes | USER implementation-planning carrier, proof intake, narrow waiver/reclassification, reject/defer, or later promotion path after proof |
| Package E - Negative Examples, Bad Fixtures, Helper Expectations, And Validator Expectations | Packet generated; no code or fixture mutation | Current local ZIP verified: `Governance-20260617-120340.zip`, SHA256 `4293349496583D87F7FC825491D1B68A9495EE70654D687D59C3D4A89E52E320`, `58` files | No | No | Yes | Yes | USER helper/validator/fixture implementation carrier, named waiver/reclassification, reject/defer, or blocked posture |
| Final Integration Hardening | Completed as no-overclaim integration review | This receipt records package-state reconciliation and blocker ledger | No | Not applicable | Yes | Yes because Packages A-E remain unresolved | USER must choose continued proof/promotion work, named waiver/reclassification, reject/defer, or remain blocked |

| Blocker | Current Status | Evidence | Blocks PR Readiness? | Clear Path | USER Decision Needed |
| --- | --- | --- | --- | --- | --- |
| `Current Branch Template Work Incomplete` | Active | Packages A-E remain current-PR scope and unresolved for proof, promotion, implementation, waiver, rejection, deferral, or explicit reclassification | Yes | Complete every named lane or explicitly reclassify remaining lanes out of current PR scope | Yes |
| `Golden Reference Promotion Blocked` | Active | `Docs/ui_reference_catalog/index.md` still records `Promoted Reference Count: 0` and no USER-approved promotion receipt exists | Yes for any PR claiming promoted references | USER-approved proof, USER visual acceptance/waiver, and catalog promotion record for named references | Yes |
| `Promoted Reference Count: 0` | Preserved / correct | Catalog is intentionally empty | Yes if any claim implies a promoted reference exists | Keep zero until promotion approval; create promoted records only after exact approval | Yes for any promotion |
| Package A proof incomplete | Active | Missing independent state proof and USER visual acceptance for top-level windows/control cluster | Yes | Proof intake, later FAM/runtime proof route, waiver/reclassification, reject/defer, or promotion after proof | Yes |
| Package B proof incomplete | Active | Controls/menu/list/filter state, accessibility, keyboard, empty/loading/error, and USER acceptance remain incomplete | Yes | Proof intake, waiver/reclassification, reject/defer, or promotion after proof | Yes |
| Package C proof incomplete | Active | Modal/dialog, status/failure/recovery, tray/menu doorway, settings-category, accessibility, and USER acceptance proof remain incomplete | Yes | Proof intake, waiver/reclassification, reject/defer, or promotion after proof | Yes |
| Package D implementation/proof incomplete | Active | Design-token/shared-rule implementation, visual constants, contrast proof, adoption routing, and USER acceptance remain unapproved | Yes | Implementation-planning carrier, proof intake, waiver/reclassification, reject/defer, or promotion after proof | Yes |
| Package E enforcement implementation incomplete | Active | Negative fixtures, helper changes, validator changes, and false-green regression coverage remain unapproved | Yes unless reclassified | Future helper/validator/fixture implementation carrier, waiver/reclassification, reject/defer, or blocked posture | Yes |
| Target-FAM adoption pending | Deferred out of this Governance PR | FAM-003/FAM-006/FAM-007 adoption belongs to target FAM legal gates after merge/rebaseline | No for Governance PR unless overclaimed | Each target FAM inventories and repairs/waives/issues its own surfaces at next legal gate | Yes in target carriers |

| Claim Area | Allowed Claim | Forbidden Overclaim | Current Hardening Finding |
| --- | --- | --- | --- |
| UI reference catalog | The catalog exists and has zero promoted references | Any statement that Package A-E packets promoted catalog records | Clean: `Promoted Reference Count: 0` is consistent |
| Candidate evidence | HUD/FAM-006 and PR #269 AI Control Center are candidate/comparison evidence | Any statement that they are canonical golden references | Clean: receipts preserve candidate-only status |
| Package packets | Packets are USER-reviewable evidence and planning/proof receipts | Any statement that packet generation clears package proof or promotion blockers | Clean after this receipt |
| Design tokens/shared primitives | Package D defines future expectations | Any statement that design tokens, shared CSS/components, or reusable primitives were implemented | Clean: implementation remains blocked |
| Helper/validator/fixture enforcement | Package E defines future enforcement expectations | Any statement that executable fixtures or validator/helper code were added by Package E | Clean: future enforcement remains blocked |
| Target-FAM adoption | Adoption is future work in target FAM legal carriers | Any Governance-branch mutation or adoption claim for FAM-003/FAM-006/FAM-007 | Clean: target FAMs remain consumer/context inputs only |
| PR Readiness | PR Readiness may occur only after blockers clear or USER explicitly reclassifies named lanes | Any request for PR Readiness Stage 1 while blockers remain unresolved | Blocked: next decision must resolve or preserve blockers |

Before-PR Hardening Conclusion: The current branch has enough source-truth clarity to avoid overclaim drift, but it does not have enough completed proof/promotion/implementation/reclassification to enter PR Readiness. The next legal path is one of: continue proof collection or promotion-route work for named Packages A-E; approve a named waiver/reclassification for remaining lanes; reject/defer named lanes while explicitly preserving the blocker; or remain blocked before PR Readiness.

## Template / Golden Reference Blocker-Disposition Digestion And Proof Route Plan - 2026-06-17

Document Status: Non-Binding Disposition And Route-Planning Receipt. Binding authority remains with `Docs/nexus_vision.md`, `Docs/family_visions/FAM-002_desktop_interface.md`, `Docs/family_feature_visions/F2-FF01.md`, `Docs/family_feature_visions/F3-FF01.md`, `Docs/ui_reference_catalog/`, `Docs/phase_governance.md`, `Docs/branch_plans/README.md`, `Docs/user_test_summary_guidance.md`, and `Docs/validation_helper_registry.md`.

USER Disposition: `CONTINUE PROOF / PROMOTION WORK FOR ALL PACKAGES A-E`. USER accepted `C:\Nexus USER\Governance-20260617-121432.zip` as the blocker-disposition packet and chose not to reclassify Packages A-E out of current PR scope, not to waive proof requirements, not to reject/defer those authority lanes out of this Governance PR, not to enter PR Readiness, and not to promote any reference.

Disposition Result: `ROUTE PLAN RECORDED - PR READINESS STILL BLOCKED`. `Docs/ui_reference_catalog/index.md` remains `Promoted Reference Count: 0`; no promoted catalog records exist; no actual golden-reference promotion, catalog promoted-reference record, template, design token, shared primitive, helper, validator, fixture, FAM worktree mutation, runtime proof, external-state mutation, issue mutation, PR, merge, release, cleanup, file movement/deletion/archive, USER visual acceptance, or USER waiver is authorized by this receipt.

| Package | Lane | Current Status | Required Proof / Work | Next Legal Route | Requires USER Evidence? | Requires FAM/Runtime Approval? | Requires Helper/Validator/Fixture Approval? | Blocks PR Readiness? | Recommended Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Package A | HUD/FAM-006 surface reference | Candidate comparison evidence only; no promotion | Isolated top-level/child-window classification, state matrix, large `CLOSE` pill disposition, hover/focus/disabled proof, applicability, and USER acceptance | USER-provided screenshot/video proof intake when available, or later FAM-006 runtime proof collection approval | Yes for visual acceptance and any USER-provided proof | Yes only if new runtime proof must be generated by FAM-006 | No | Yes | Keep as comparison evidence for the Package A proof intake; do not promote without proof |
| Package A | PR #269 AI Control Center surface reference | Strongest Package A seed; no promotion | Maximize/restore/hidden-control matrix, disabled/blocked/focus/pressed states, keyboard/focus/hitbox/accessibility proof, multi-surface comparison, and USER acceptance | USER-provided screenshot/video proof intake from existing approved evidence or later FAM-007 runtime proof collection approval | Yes | Yes only if new runtime proof must be generated by FAM-007 | No | Yes | Use as primary Package A seed for the next proof/promotion packet |
| Package A | Golden window and window-control cluster reference | No promoted top-level/window-control reference exists | Reference schema, eligible/non-eligible window class matrix, geometry/resize/reset expectations, platform exceptions, known limitations, state proof, and USER acceptance | Governance/FAM-002 promotion-route planning after visual proof exists | Yes | Maybe, if runtime proof is needed for state evidence | No | Yes | Next safest grouped package because it can advance through USER-provided proof without target-FAM mutation |
| Package B | Buttons, dropdowns, menus, lists, and filters | No-promotion packet generated; proof incomplete | Control anatomy, state matrix, accessibility, keyboard/focus, empty/loading/error, overflow, selected/disabled states, comparison proof, and USER acceptance | Later proof intake after Package A establishes window/control-cluster baseline, or USER-provided evidence if complete control-state images already exist | Yes | Maybe, if missing states require runtime proof in owning FAMs | No initially; future enforcement waits | Yes | Keep current-PR scope; run after Package A unless USER prioritizes control-state proof |
| Package C | Modal/dialog, status/failure/recovery, tray/menu doorway, and settings surfaces | No-promotion packet generated; proof incomplete | Surface class matrix, failure/recovery runtime truth, modal focus/keyboard proof, tray/menu doorway limitations, settings-category routing, accessibility, and USER acceptance | Later proof intake after Package A and relevant FAM-003/FAM-001/FAM-002 context is settled; FAM/runtime approval required for new live proof | Yes | Likely for new tray/settings/failure proof | No initially; future enforcement waits | Yes | Keep current-PR scope; avoid runtime adoption mutation in Governance |
| Package D | Design tokens and shared UI rules | No-promotion packet generated; implementation/proof deferred | Token taxonomy, accepted values/ranges, code-to-visual trace, contrast proof, reusable primitive boundary, migration/rollback, adoption routing, and USER acceptance | Future design-token/shared-primitive implementation approval after visual references are promoted or explicitly accepted | Yes for acceptance | Maybe for visual parity proof | No unless validators later enforce token use | Yes | Wait until Package A/B/C visual reference lanes are clearer |
| Package E | Negative examples, bad fixtures, helper expectations, and validator expectations | No-code/no-fixture packet generated; enforcement implementation deferred | Executable bad fixtures, helper changes, validator changes, false-green regression coverage, fixture pass/fail proof, and USER approval | Future helper/validator/fixture implementation carrier after visual proof/reference rules are specific enough to avoid brittle automation | No for planning; yes for approving enforcement scope | No, unless fixtures need runtime surfaces | Yes | Yes unless reclassified later | Wait; do not automate against unpromoted references |
| Target-FAM adoption | FAM-003/FAM-006/FAM-007/future FAM consumption | Deferred out of this Governance PR | Each target FAM inventories created/touched surfaces after merge/rebaseline and compares them to promoted or binding standards | Target-FAM legal carrier after Governance merge/rebaseline | Maybe in target FAM review | Yes in target carriers only | Maybe in future target-FAM validators | No for this Governance PR unless overclaimed | Preserve as post-merge/rebaseline work |

| Candidate Next Package | Included Lanes | Why This Next | Legal Now? | Mutation Required? | PR Impact | Recommendation |
| --- | --- | --- | --- | --- | --- | --- |
| Package A - USER-provided proof intake and promotion-route packet | Golden window, AI Control Center seed, HUD comparison, golden control-cluster, close/minimize/maximize cluster | It has the strongest existing evidence, directly addresses the most disruptive UI drift, and can advance through USER-provided screenshot/video evidence without mutating FAM worktrees | Yes for planning and USER-provided evidence intake; no for promotion without later acceptance | No repo promotion or FAM mutation now; only packet/planning unless later approved | Advances current-PR completion while preserving blockers | Recommended next |
| Package B - Controls proof intake | Buttons, dropdowns, menus, lists, filters | Important for broad UI consistency, but reference quality depends on Package A window/control-class decisions | Yes for planning; proof may be incomplete | No if USER supplies evidence; otherwise later FAM/runtime proof | Useful but less foundational than Package A | Second priority |
| Package C - Surface/settings/doorway proof intake | Modal/dialog, status/failure/recovery, tray/menu, Global Settings surfaces | Important but likely touches FAM-003/FAM-001 runtime behavior and Windows tray constraints | Planning yes; proof likely requires later runtime/FAM approval | Likely later FAM/runtime proof | Keep scoped; avoid Governance runtime/adoption mutation | Third priority |
| Package D - Design token/shared rule implementation planning | Design tokens, shared UI rules, reusable primitives | Should follow accepted visual references to avoid codifying unstable visuals | Planning only yes; implementation no | Implementation requires separate approval | Too early for implementation | Wait |
| Package E - Helper/validator/fixture implementation planning | Negative fixtures, bad examples, helper/validator enforcement | Automation is valuable, but brittle if built before references/proof are accepted | Planning only yes; code/fixture mutation no | Helper/validator/fixture mutation requires separate approval | Too early for code enforcement | Wait until Package A and core references are clearer |

| Blocker | Current Status | Cleared By This Cycle? | Reason | Next Legal Action |
| --- | --- | --- | --- | --- |
| `Current Branch Template Work Incomplete` | Active | No | USER chose continued proof/promotion work for all Packages A-E; no lane was completed or reclassified | Approve Package A USER-provided proof intake / promotion-route packet or another named package route |
| `Golden Reference Promotion Blocked` | Active | No | No USER-approved promotion packet, visual acceptance, waiver, or catalog record exists | Collect proof, then request named USER visual acceptance/promotion |
| `Promoted Reference Count: 0` | Preserved / correct | No | Empty catalog remains required until promotion approval exists | Keep zero until exact promotion approval |
| Package A proof incomplete | Active | No | Existing proof is candidate-only and missing state/class/accessibility/USER acceptance coverage | Recommended next: Package A proof intake and promotion-route packet |
| Package B proof incomplete | Active | No | Controls/menu/list/filter evidence remains incomplete and should follow Package A baseline | Keep current-PR scope; run after Package A or upon USER priority |
| Package C proof incomplete | Active | No | Modal/status/tray/settings proof likely requires later FAM/runtime evidence | Keep current-PR scope; avoid target-FAM mutation |
| Package D implementation/proof incomplete | Active | No | Design-token/shared-rule implementation and proof are unapproved | Wait for promoted/accepted visual references or later implementation approval |
| Package E enforcement implementation incomplete | Active | No | Helper/validator/fixture code mutation remains unapproved and should wait until visual rules are concrete | Wait for later helper/validator/fixture implementation approval |
| Target-FAM adoption pending | Deferred out of Governance PR | Not applicable | Adoption belongs to target FAM legal gates after merge/rebaseline | Preserve as post-merge/rebaseline work |

Recommended Next Legal Package: `Package A - USER-provided proof intake and promotion-route packet for top-level window and window-control cluster`. This route best advances the current PR without target-FAM mutation because it can start by digesting USER-provided screenshot/video evidence and existing candidate evidence. It must still preserve `Promoted Reference Count: 0` until a later USER visual acceptance and promotion decision creates a catalog record.

## Template / Golden Reference Package A USER-Provided Proof Intake And Promotion-Route Packet Planning - 2026-06-17

Document Status: Non-Binding Proof-Intake / Promotion-Route Planning Receipt. Binding authority remains with `Docs/nexus_vision.md` for Project UI Vision and proof hierarchy, `Docs/family_visions/FAM-002_desktop_interface.md` for reusable Desktop Interface presentation grammar, `Docs/family_feature_visions/F2-FF01.md` for UI reference-system missing-proof rows and promotion boundaries, `Docs/ui_reference_catalog/` for promoted reference records only after explicit USER promotion approval, `Docs/phase_governance.md` for phase/blocker routing, and `Docs/user_test_summary_guidance.md` for USER proof interpretation.

Proof-Intake Result: `PACKET GENERATED - NO PROMOTION`. Governance inspected the current `C:\Nexus USER\Governance` packet, read-only FAM-006 and FAM-007 USER/evidence packets, and the empty UI reference catalog. No current Governance packet image or video evidence was found. FAM-007 AI Control Center evidence remains the strongest Package A seed, but the default and minimize-hover screenshots are duplicate proof by SHA256 for both focused and full-desktop files, so minimize-hover remains missing as independent proof. FAM-006 HUD/Recording/Log evidence includes USER-inspectable screenshots and a short video path, but the returned UTS packet explicitly keeps USER Gate State pending and Live Validation / UTS acceptance withheld. No reviewed proof item supplies USER visual acceptance, waiver, catalog promotion authority, or a complete Package A state/class/accessibility matrix.

Catalog Boundary: `Docs/ui_reference_catalog/index.md` remains `Promoted Reference Count: 0`; no promoted catalog records exist; no reference is promoted by this pass. Candidate screenshots, manifests, helper output, Live Validation evidence, or attractive visuals remain evidence only until a later USER-approved promotion packet records the required schema and final disposition.

| Candidate | Proof Item | Source Path | Proof Type | State Covered | Independent? | Sufficient? | Issue | Recommended Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HUD/FAM-006 surface reference | USER screenshot root, focused screenshots, short video pointer, and returned UTS packet | `C:\Users\anden\OneDrive\Pictures\Screenshots\Nexus Desktop AI\fam_006_monitoring_hud_live_validation\20260609_221334_192`; `C:\Nexus USER\FAM-006\Review Aids\LATEST_EVIDENCE_POINTERS.md`; `C:\Nexus USER\FAM-006\USER Review\RETURNED_UTS_LIVE_VALIDATION_FAILURE_REVIEW.md` | Screenshots, video pointer, manifests, USER review packet | HUD/Dashboard/Recording/Log candidate surfaces, focused elements, returned UTS repair proof | Partially | No | UTS acceptance remains pending; Live Validation acceptance is withheld; Package A still lacks isolated window-class matrix, large `CLOSE` disposition, complete state coverage, and USER visual acceptance | `INSUFFICIENT - preserve as comparison evidence; route missing proof to FAM-006 legal carrier, USER-provided proof packet, or named waiver/reclassification` |
| PR #269 AI Control Center surface reference | Default and minimize-hover focused screenshot hash comparison | `C:\Nexus USER\FAM-007\Review Aids\Inspectable Evidence\focused_element_screenshots\01_before_resize_focused_window.png`; `C:\Nexus USER\FAM-007\Review Aids\Inspectable Evidence\focused_element_screenshots\02_window_control_minimize_hover_focused_window.png` | PNG hash comparison | Default state versus minimize-hover claim | No | No | Both files have SHA256 `B40B5FCBC1EB85673809BAA57C9015BC4DB1FD16DB411BB706153F46910A8B03`; minimize-hover is not independent proof | `DUPLICATE - minimize-hover remains missing and must be recollected, supplied, waived, or scoped out before promotion` |
| PR #269 AI Control Center surface reference | Default and minimize-hover full-desktop screenshot hash comparison | `C:\Nexus USER\FAM-007\Review Aids\Inspectable Evidence\full_desktop_screenshots\01_before_resize_full_desktop.png`; `C:\Nexus USER\FAM-007\Review Aids\Inspectable Evidence\full_desktop_screenshots\02_window_control_minimize_hover_full_desktop.png` | PNG hash comparison | Full-desktop default versus minimize-hover claim | No | No | Both files have SHA256 `C4B997F2F5C3A9C90C4A22EF64C090C526ABDE019632F93330263E21A5998836`; hover state is not independently proven | `DUPLICATE - do not use as independent hover proof` |
| PR #269 AI Control Center surface reference | Close-hover focused and full-desktop screenshots | `C:\Nexus USER\FAM-007\Review Aids\Inspectable Evidence\focused_element_screenshots\04_window_control_close_hover_focused_window.png`; `C:\Nexus USER\FAM-007\Review Aids\Inspectable Evidence\full_desktop_screenshots\04_window_control_close_hover_full_desktop.png` | Screenshots | Close-hover visual state | Yes for close-hover image difference | No | Close-hover evidence is useful, but Package A still lacks full control-state matrix, focus/pressed/disabled/blocked states, hitbox/accessibility proof, class applicability, and USER visual acceptance | `INSUFFICIENT - preserve as candidate proof for later promotion packet` |
| PR #269 AI Control Center surface reference | Resize screenshots and runtime evidence digest | `C:\Nexus USER\FAM-007\Review Aids\Inspectable Evidence\focused_element_screenshots\05_after_corner_resize_focused_window.png`; `06_after_right_edge_resize_focused_window.png`; `07_after_bottom_edge_resize_focused_window.png`; `C:\Nexus USER\FAM-007\Review Aids\VISION_TO_PROOF_MATRIX.md`; `C:\Nexus USER\FAM-007\Review Aids\H4_TOOLTIP_HARDENING_DIGEST.md` | Screenshots, digest, manifest summary | Geometry/resize, tooltip suppression, compact cluster candidate behavior | Yes for resize images | No | Resize proof is useful but does not cover full top-level reference schema or complete control-state/accessibility/USER acceptance requirements | `INSUFFICIENT - preserve as strongest seed evidence; collect missing states or route waiver/reclassification` |
| Golden window reference | FAM-002/F2-FF01 source-truth schema plus HUD/AI Control Center candidate evidence | `Docs/family_visions/FAM-002_desktop_interface.md`; `Docs/family_feature_visions/F2-FF01.md`; candidate USER packets | Source truth plus candidate evidence | Top-level window reference class | No visual proof by itself | No | No promoted reference record, complete schema, class matrix, known limitations, multi-surface proof, or USER visual acceptance exists | `MISSING - build later promotion packet only after proof/waiver exists` |
| Golden control-cluster reference | FAM-002/F2-FF01 grammar plus AI Control Center compact cluster candidate | `Docs/family_visions/FAM-002_desktop_interface.md`; `Docs/family_feature_visions/F2-FF01.md`; FAM-007 candidate screenshots | Source truth plus candidate evidence | Close/minimize/maximize/restore cluster class | Partial | No | Compact cluster direction exists, but minimize-hover is duplicate, maximize/restore hidden-control matrix and focus/pressed/disabled/blocked/accessibility proof remain incomplete | `INSUFFICIENT - pair with golden window proof route; do not promote` |
| Close/minimize/maximize standard | FAM-002 top-level control grammar, AI Control Center cluster evidence, HUD large `CLOSE` comparison | `Docs/family_visions/FAM-002_desktop_interface.md`; FAM-007/FAM-006 candidate evidence | Source truth plus candidate comparison | Top-level compact cluster versus modal/child/content large `CLOSE` exception | Partial | No | Direction is durable planning grammar, not a promoted state-complete reference; class matrix and visual state proof remain missing | `INSUFFICIENT - keep as Package A route; require class matrix, state proof, and USER acceptance before catalog promotion` |

| Candidate | Current Status | Proof Gap | Next Route | Requires USER Evidence? | Requires FAM/Runtime Approval? | Requires USER Visual Acceptance? | Can Move To Promotion Packet? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HUD/FAM-006 surface reference | Candidate comparison evidence only | UTS acceptance pending, window-class isolation, large `CLOSE` disposition, state matrix, hover/focus/disabled/accessibility, and Package A schema gaps | Later FAM-006 runtime proof collection, USER-provided proof intake, or named waiver/reclassification | Yes | Yes if new runtime/live proof is collected | Yes unless explicitly waived/reclassified | No, not yet |
| PR #269 AI Control Center surface reference | Strongest seed, but incomplete | Duplicate minimize-hover proof, missing maximize/restore hidden-control matrix, focus/pressed/disabled/blocked/accessibility/hitbox proof, multi-surface comparison, USER acceptance | USER-provided proof intake for missing states, later FAM-007 runtime proof collection, or named waiver/reclassification | Yes | Yes if new runtime/live proof is collected | Yes unless explicitly waived/reclassified | Only after missing proof is supplied/waived and scope is narrowed |
| Golden window reference | No promoted top-level reference exists | Complete schema, eligible/non-eligible class matrix, geometry/reset expectations, platform exceptions, known limitations, multi-surface proof, USER acceptance | Governance/FAM-002 promotion packet after proof exists | Yes | Maybe if new runtime state proof is needed | Yes unless explicitly waived | No, proof missing |
| Golden control-cluster reference | No promoted control-cluster reference exists | Applicability matrix, hidden/blocked controls, hover/focus/pressed/disabled states, tooltip/accessibility names, hitboxes, keyboard/focus proof, child/modal distinction | Pair with top-level window proof route or later FAM/runtime proof collection | Yes | Maybe if new runtime state proof is needed | Yes unless explicitly waived | No, proof missing |
| Close/minimize/maximize standard | Planning direction only | Class matrix, default/hover/focus/pressed/disabled/blocked state proof, accessibility, known exceptions, USER acceptance | Fold into golden control-cluster promotion packet or explicitly narrow/waive | Yes | Maybe if new runtime state proof is needed | Yes unless explicitly waived | No, proof missing |

| Blocker | Current Status | Cleared By This Cycle? | Reason | Next Legal Action |
| --- | --- | --- | --- | --- |
| `Current Branch Template Work Incomplete` | Active | No | Package A proof-intake planning generated a route packet but did not complete, promote, waive, reject, or reclassify Package A-E authority lanes | USER must choose proof supply, FAM/runtime proof collection, waiver/promotion route, rejection/deferral/reclassification, or another named package route |
| `Golden Reference Promotion Blocked` | Active | No | No USER-approved promotion packet, visual acceptance, waiver, or catalog record exists | Collect or provide missing proof, then request named USER visual acceptance/promotion |
| `Promoted Reference Count: 0` | Preserved / correct | No | Empty catalog remains the correct source-truth posture; it also proves no golden reference has been promoted | Keep zero until exact USER promotion approval creates a catalog record |
| Package A proof incomplete | Active | No | Existing evidence is candidate-only and missing independent minimize-hover, state/class/accessibility, complete schema, and USER acceptance | Review this packet and select a Package A proof/promotion route |
| Package B proof incomplete | Active | No | Package B remains current-PR scope and is not cleared by Package A proof intake | Continue after Package A route is selected or upon USER priority |
| Package C proof incomplete | Active | No | Package C remains current-PR scope and is not cleared by Package A proof intake | Continue after Package A/B route selection or upon USER priority |
| Package D implementation/proof incomplete | Active | No | Design-token/shared-rule implementation and proof remain unapproved | Wait for visual reference lane clarity or later implementation approval |
| Package E enforcement implementation incomplete | Active | No | Helper/validator/fixture code mutation remains unapproved and should not automate unpromoted references | Wait for later helper/validator/fixture implementation approval |

Next Legal Use: USER reviews the Package A proof-intake packet and chooses one route: provide the missing Package A screenshot/video proof, approve later FAM/runtime proof collection in owning FAM carriers, approve a named USER visual waiver/promotion route, reject/defer/reclassify Package A, proceed to another named Package A-E route while Package A remains blocking, or keep PR Readiness blocked. This receipt does not authorize PR Readiness, PR creation, merge, release, FAM-003/FAM-006/FAM-007/main mutation, runtime proof generation, external-state mutation, catalog promotion, promoted-reference record creation, template creation, design-token/shared-primitive implementation, helper/validator/fixture mutation, issue mutation, cleanup, USER visual acceptance, or USER waiver.

## Template / Golden Reference Combined Packages B-E Proof-Route Decision And Evidence-Collection Admission - 2026-06-17

Document Status: Non-Binding Proof-Route / Evidence-Collection Admission Receipt. Binding authority remains with `Docs/nexus_vision.md` for Project UI Vision and proof hierarchy, `Docs/family_visions/FAM-002_desktop_interface.md` for reusable Desktop Interface presentation grammar, `Docs/family_feature_visions/F2-FF01.md` for UI reference-system missing-proof rows and promotion boundaries, `Docs/family_feature_visions/F3-FF01.md` for resident access/tray/settings dependency context, `Docs/ui_reference_catalog/` for promoted reference records only after explicit USER promotion approval, `Docs/phase_governance.md` for phase/blocker routing, `Docs/user_test_summary_guidance.md` for USER proof interpretation, and `Docs/validation_helper_registry.md` for future helper/validator guidance.

Proof-Route Result: `ROUTE DECISION RECORDED - NO PROMOTION`. Package A remains current-PR scope and blocked for proof. Packages B-E remain current-PR scope. This pass classifies proof and evidence routes only; it does not waive proof, promote references, create catalog records, create templates, implement design tokens, implement shared UI primitives, mutate helpers, mutate validators, mutate fixtures, mutate FAM worktrees, mutate external state, create issues, create a PR, merge, release, or authorize USER visual acceptance. `Docs/ui_reference_catalog/index.md` remains `Promoted Reference Count: 0`.

Repo / External-State Boundary: durable package proof-route decisions may be recorded here as planning receipts and in the standing branch authority record. Candidate screenshots, videos, hashes, helper outputs, current packet inventories, live runtime results, FAM adoption status, issue state, PR state, and current validation pass state remain evidence outside promoted catalog rows unless a later source-truth owner explicitly records a historical receipt. The UI reference catalog must remain empty until a USER-approved promotion packet creates a promoted reference record.

Packages B-E Proof-Route Table:

| Package | Lane | Current Status | Required Proof / Work | Next Legal Route | Requires USER Evidence? | Requires FAM/Runtime Approval? | Requires Helper/Validator/Fixture Approval? | Requires Design/Shared Primitive Approval? | Blocks PR Readiness? | Recommended Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B | Button standards | `REVISE - candidate comparison evidence only` | Primary/secondary/danger/default/hover/focus/pressed/disabled/blocked/loading/error states, text/icon alignment, spacing, contrast, keyboard activation, hitbox/accessibility, and USER acceptance | Package B USER-provided screenshot/video proof intake, or later owning-FAM runtime proof collection if USER evidence is unavailable | Yes | Maybe, if new runtime/live proof is needed | No for proof intake; yes only if later enforcement fixtures are admitted | No | Yes | Collect proof; do not promote |
| B | Dropdown standards | `DEFER - proof mostly missing` | Closed/open, selected, hover/focus/keyboard, disabled/empty/error/overflow, option grouping, labels, and USER acceptance | USER proof if existing evidence is available; otherwise later owning-FAM runtime proof | Yes | Likely | No for proof intake | No | Yes | Preserve missing-proof row and collect evidence when available |
| B | Menu standards | `DEFER - proof missing` | Open/closed, hover/focus/selected/disabled, separators/grouping/nested/overflow, keyboard, accessibility, dismissal behavior, and USER acceptance | USER proof if available; otherwise later FAM/runtime proof, especially for resident or tray menus | Yes | Likely | No for proof intake | No | Yes | Defer promotion until proof exists |
| B | List standards | `DEFER - proof incomplete` | Rows, selected/unselected, hover/focus, empty/loading/error, sort/filter, keyboard, accessibility, and USER acceptance | USER proof or later owning-FAM runtime proof | Yes | Likely | No for proof intake | No | Yes | Collect evidence; do not promote |
| B | Filter standards | `DEFER - proof missing` | Default/active/clear/invalid/no-result states, combined-filter behavior, reset behavior, keyboard/accessibility, and USER acceptance | USER proof or later owning-FAM runtime proof | Yes | Likely | No for proof intake | No | Yes | Collect evidence; do not promote |
| C | Modal/dialog standards | `REVISE - candidate comparison evidence only` | Modal taxonomy, open/close/dismiss/confirm/cancel/destructive states, focus trap, Escape behavior, keyboard, disabled/blocked state, platform exception classification, accessibility, and USER acceptance | USER proof or later owning-FAM runtime proof | Yes | Likely | No for proof intake | No | Yes | Proof intake only; no promotion |
| C | Status/failure/recovery panels | `DEFER - proof missing` | Success/warn/info/degraded/blocked/fatal/recovery states, retry/reset/report/support paths, runtime-truth mapping, safe wording, sequence proof, and USER acceptance | Later owning-FAM proof or USER-provided proof if available | Yes | Likely | No for proof intake | No | Yes | Preserve as missing proof and route later |
| C | Tray/menu doorway | `DEFER - proof mostly missing` | Real tray doorway proof, open/close/dismiss/menu states, compact menu budget, immutable/configurable entries, privacy/status visibility, Windows limitation, keyboard/accessibility, settings links, and USER acceptance | Later FAM-003/runtime proof is likely; USER proof may be accepted if complete | Yes | Yes | No for proof intake | No | Yes | Do not mutate FAM-003; keep as future proof route |
| D | Design-token standards | `REVISE - candidate extraction evidence only` | Token taxonomy, naming, owner location, inventory, code-to-visual trace, contrast, cross-surface comparison, adoption/rollback, and USER acceptance | Future implementation-planning carrier after visual references are accepted or explicitly scoped | Yes for acceptance | Maybe for parity proof | No initially | Yes | Yes | Do not implement before visual references are stable |
| D | Shared UI rules/primitives | `DEFER - implementation unapproved` | Owner/API/component boundary, reuse/migration/rollback plan, visual parity, compatibility, and adoption path | Future design/shared primitive implementation approval after reference clarity | Yes | Maybe | Maybe later | Yes | Yes | Wait; avoid codifying unstable visuals |
| E | Negative examples / bad fixtures | `Planning only` | Executable bad fixtures, positive/negative corpus, overclaim examples, and false-green regressions | Future fixture/helper/validator implementation approval after reference rules are concrete | Maybe for fixture acceptance | No unless runtime fixtures are admitted | Yes | No | Yes | Keep as planned enforcement work |
| E | Helper expectations | `Planning only` | Packet-stage checks, duplicate-hash checks, missing-proof row enforcement, catalog count checks, and false-green reporting | Future helper implementation carrier | No | No | Yes | No | Yes | Wait until accepted proof rules are precise |
| E | Validator expectations | `Planning only` | Catalog count/schema checks, no-promotion scans, no-FAM-mutation checks, PR-readiness blocker checks, and no-overclaim checks | Future validator implementation carrier | No | No | Yes | No | Yes | Wait until accepted proof rules are precise |

Package Priority Table:

| Candidate Next Package | Included Lanes | Why This Next | Legal Now? | Mutation Required? | PR Impact | Recommendation |
| --- | --- | --- | --- | --- | --- | --- |
| Package B USER-provided proof intake | Buttons, dropdowns, menus, lists, filters | Controls are foundational across FAM-002/FAM-003/FAM-006/FAM-007/FAM-008 consumers and can start with USER-provided screenshots/video without sibling worktree mutation | Yes, as proof intake / evidence classification only | No repo/FAM/runtime mutation if USER supplies evidence | Advances one current-PR blocker, but PR Readiness remains blocked until all current-PR lanes are completed, waived, promoted, rejected, deferred out of PR scope, or reclassified by USER | Recommended next |
| Combined Package B/C visual proof intake | Controls plus modal/dialog/status/failure/recovery/tray/menu classes | This groups adjacent visible-surface standards, but Package C likely needs FAM-003 or runtime proof for tray/menu/settings doorway behavior | Legal as planning/proof intake; runtime proof remains separately gated | No for existing/USER evidence; yes if new runtime proof is required | Higher review load, but can reduce packet churn if USER has enough visual evidence | Acceptable alternate if USER wants a wider evidence packet |
| Package C proof intake | Modal/dialog, status/failure/recovery, tray/menu doorway | Important for reliability and resident-access surfaces, but more likely to need later FAM/runtime evidence | Yes as proof intake | No for existing/USER evidence; likely yes later for runtime/tray proof | Advances C only; PR Readiness remains blocked | Second priority after Package B unless USER prioritizes tray/settings |
| Package D design-token/shared-rule implementation planning | Design tokens, shared UI rules, primitive ownership | Tokens and primitives should derive from accepted visual references; doing D too early risks codifying unstable candidate visuals | Planning is legal; implementation is not approved | Implementation approval required later | Could improve future enforcement but should not clear current visual-proof blockers | Wait until Package A/B/C proof posture is clearer |
| Package E helper/validator/fixture implementation planning | Negative examples, helpers, validators, fixtures | Enforcement needs precise accepted rules; automating before reference acceptance risks a false-green or false-red machine | Planning is legal; code/fixture mutation is not approved | Helper/validator/fixture approval required later | Reduces future drift only after rules stabilize | Wait until A/B/C/D rules are concrete |

Blocker Table:

| Blocker | Current Status | Cleared By This Cycle? | Reason | Next Legal Action |
| --- | --- | --- | --- | --- |
| `Current Branch Template Work Incomplete` | Active | No | This cycle records proof routes only; it does not complete, promote, waive, reject, or reclassify Package A-E lanes | Continue Package B proof intake next, provide Package A proof, or choose another explicit route |
| `Golden Reference Promotion Blocked` | Active | No | No USER-approved promotion packet, visual acceptance, waiver, or promoted catalog record exists | Collect proof and later request named USER visual acceptance/promotion |
| `Promoted Reference Count: 0` | Preserved / correct | No | Empty catalog is still required until explicit promotion approval exists | Keep count zero until a promotion packet creates a catalog record |
| Package A proof incomplete | Active | No | Existing Package A evidence remains candidate-only and still lacks full independent state/class/accessibility and USER acceptance proof | USER may provide missing Package A evidence, approve runtime proof collection, or choose a named waiver/reclassification route |
| Package B proof incomplete | Active | No | Package B lanes have route classifications but no complete proof or USER acceptance | Recommended next: Package B USER-provided proof intake |
| Package C proof incomplete | Active | No | Package C lanes likely need more runtime/USER proof, especially tray/menu and failure/recovery | Continue after B or choose C as alternate |
| Package D implementation/proof incomplete | Active | No | Design-token/shared-primitive implementation and proof remain unapproved and should wait for stable visual references | Defer until visual reference lanes are concrete |
| Package E enforcement implementation incomplete | Active | No | Helper/validator/fixture code mutation remains unapproved and should wait until visual rules are precise | Defer until reference rules are concrete |
| Target-FAM adoption pending | Deferred out of Governance PR | Not applicable | Target-FAM adoption belongs to target FAM legal gates after merge/rebaseline | Preserve as post-merge/rebaseline work |

Recommended Next Legal Package: `Package B - USER-provided proof intake and evidence-collection packet for buttons, dropdowns, menus, lists, and filters`. This is the best next route because it advances foundational UI controls without requiring sibling worktree mutation, avoids premature design-token/helper enforcement, and keeps Package A/C/D/E blockers visible. A combined Package B/C intake is acceptable only if USER wants a wider packet and has enough visual evidence to avoid another text-only proof gap.

Next Legal Use: USER may approve Package B proof intake, provide missing Package A proof, choose combined Package B/C proof intake, approve later FAM/runtime proof collection in owning carriers, approve a named visual waiver/promotion route, reject/defer/reclassify named lanes, or keep PR Readiness blocked. This receipt does not authorize PR Readiness, PR creation, merge, release, FAM-003/FAM-006/FAM-007/main mutation, runtime proof generation, external-state mutation, catalog promotion, promoted-reference record creation, template creation, design-token/shared-primitive implementation, helper/validator/fixture mutation, issue mutation, cleanup, USER visual acceptance, or USER waiver.

## Template / Golden Reference Package B USER-Provided Proof Intake And Evidence-Collection Packet - 2026-06-17

Document Status: Non-Binding Proof-Intake / Evidence-Collection Packet Receipt. Binding authority remains with `Docs/nexus_vision.md`, `Docs/family_visions/FAM-002_desktop_interface.md`, `Docs/family_feature_visions/F2-FF01.md`, `Docs/ui_reference_catalog/`, `Docs/phase_governance.md`, `Docs/user_test_summary_guidance.md`, and `Docs/validation_helper_registry.md`.

Package B Proof-Intake Result: `PACKET GENERATED - NO PROMOTION`. Governance cleanly regenerated `C:\Nexus USER\Governance` as a Package B proof-intake packet, copied representative read-only FAM-006 and FAM-007 candidate evidence into `Review Aids/Inspectable Evidence/`, copied source-truth context, and classified Package B proof without promoting references. The prior Governance packet and latest timestamped Governance ZIP contained no screenshot/video proof. FAM-006 supplied useful Dashboard button/control, selector, and short-video context, but UTS acceptance remains pending and the proof is not a complete Package B state matrix. FAM-007 supplied useful AI Control Center button/row/scrollbar comparison evidence, but not complete Package B proof. `Docs/ui_reference_catalog/index.md` remains `Promoted Reference Count: 0`.

| Candidate | Proof Item | Source Path | Proof Type | State Covered | Independent? | Sufficient? | Issue | Recommended Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Button standards | FAM-006 Dashboard Quick Access ready-state controls | `C:\Nexus USER\Governance\Review Aids\Inspectable Evidence\FAM-006\element_02_dashboard_quick_access_start_stop_ready_state.png` | Screenshot | Default/ready button-like controls | Yes | No | Lacks full state matrix, keyboard/accessibility, hitbox, async/error, and USER acceptance proof | `INSUFFICIENT - comparison evidence only` |
| Button standards | FAM-006 Dashboard Quick Access recording-active controls | `C:\Nexus USER\Governance\Review Aids\Inspectable Evidence\FAM-006\element_02_dashboard_quick_access_recording_active_state.png` | Screenshot | Active/recording context | Yes | No | Does not isolate each required button state | `INSUFFICIENT - comparison evidence only` |
| Dropdown standards | FAM-006 active Overlay Profile selector selected state | `C:\Nexus USER\Governance\Review Aids\Inspectable Evidence\FAM-006\element_02_hud_overlay_active_profile_selector_real_os_selected.png` | Screenshot | Closed selected selector state | Yes | No | Open/hover/focus/keyboard/disabled/empty/error/overflow state proof missing | `INSUFFICIENT - closed selected-state comparison only` |
| Button/list context | FAM-006 LV1 short video | `C:\Nexus USER\Governance\Review Aids\Inspectable Evidence\FAM-006\monitoring_hud_lv1_short_video.mp4` | Video | HUD/Dashboard interaction context | Yes | No | Context only; not a Package B state matrix and UTS acceptance remains pending | `NEEDS USER VISUAL JUDGMENT - context only` |
| Button standards | FAM-007 AI Control Center `RUN LOCAL CHECK` default state | `C:\Nexus USER\Governance\Review Aids\Inspectable Evidence\FAM-007\01_before_resize_focused_window.png` | Screenshot | One default action button and state rows | Yes | No | Covers one button state only; lacks state matrix, keyboard/accessibility, and USER acceptance | `REVISE - candidate comparison evidence only` |
| List/scrollbar context | FAM-007 custom scrollbar visual probe | `C:\Nexus USER\Governance\Review Aids\Inspectable Evidence\FAM-007\02_custom_scrollbar_visual_probe_focused_window.png` | Screenshot | Scrollable surface visual context | Yes | No | Not list/filter/dropdown/menu proof by itself | `INSUFFICIENT - comparison context only` |
| Dropdown standards | Open dropdown proof | Not found | Missing | Required Package B dropdown states | No | No | Required proof missing | `MISSING - requires USER proof or later FAM/runtime proof` |
| Menu standards | Open menu proof | Not found | Missing | Required Package B menu states | No | No | Required proof missing | `MISSING - requires USER proof or later FAM/runtime proof` |
| List standards | Dedicated list row proof | FAM-006/FAM-007 screenshots include rows/cards only | Screenshot context | Default rows only | Partial | No | Missing selected/unselected, hover/focus, empty/loading/error, sort/filter, keyboard, and accessibility proof | `INSUFFICIENT - row comparison only` |
| Filter standards | Filter proof | Not found | Missing | Required Package B filter states | No | No | Required proof missing | `MISSING - requires USER proof or later FAM/runtime proof` |

| Candidate | Current Status | Proof Gap | Next Route | Requires USER Evidence? | Requires FAM/Runtime Approval? | Requires USER Visual Acceptance? | Can Move To Promotion Packet? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Button standard | `REVISE - candidate comparison evidence only` | Full state matrix, keyboard/accessibility, hitbox, contrast, async/loading/error, and USER acceptance missing | USER-provided screenshot/video proof intake or later owning-FAM runtime proof | Yes | Maybe | Yes | No |
| Dropdown standard | `DEFER - proof mostly missing` | Open/closed/options/hover/focus/keyboard/disabled/empty/error/overflow proof missing | Later USER proof or FAM/runtime proof | Yes | Likely | Yes | No |
| Menu standard | `DEFER - proof missing` | Open/dismissed, item states, grouping/overflow, keyboard/accessibility proof missing | Later USER proof or FAM/runtime proof, likely tied to FAM-003/tray surfaces | Yes | Likely | Yes | No |
| List standard | `DEFER - proof insufficient` | Row-state matrix, empty/loading/error, sorting/filtering, keyboard/accessibility proof missing | Later USER proof or FAM/runtime proof | Yes | Likely | Yes | No |
| Filter standard | `DEFER - proof missing` | Default/active/cleared/invalid/no-result and keyboard/accessibility proof missing | Later USER proof or FAM/runtime proof | Yes | Likely | Yes | No |

| Blocker | Current Status | Cleared By This Cycle? | Reason | Next Legal Action |
| --- | --- | --- | --- | --- |
| `Current Branch Template Work Incomplete` | Active | No | Package B evidence was classified but not completed, promoted, waived, rejected, or reclassified out of current PR scope | Continue Package C proof intake, provide more Package B proof, or choose another explicit Package A-E route |
| `Golden Reference Promotion Blocked` | Active | No | No USER-approved promotion packet, visual acceptance, waiver, or catalog record exists | Collect complete proof, then request named USER visual acceptance/promotion |
| `Promoted Reference Count: 0` | Preserved / correct | No | Empty catalog remains required until exact promotion approval creates a record | Keep zero |
| Package A proof incomplete | Active | No | Package A remains current-PR scope and proof-blocked | Provide Package A proof, route later proof, or choose waiver/reclassification/reject/defer path |
| Package B proof incomplete | Active | No | Button evidence is partial; dropdown/menu/list/filter proof is missing or insufficient | Continue to Package C or provide more Package B proof |
| Package C proof incomplete | Active | No | Package C remains current-PR scope and is not cleared by Package B intake | Recommended next sequential route |
| Package D implementation/proof incomplete | Active | No | Design-token/shared-primitive implementation and proof remain unapproved | Defer until visual references are stable or USER approves implementation carrier |
| Package E enforcement implementation incomplete | Active | No | Helper/validator/fixture code mutation remains unapproved | Defer until reference rules are precise or USER approves enforcement implementation |

Package B Next Legal Use: USER may accept the Package B proof-intake packet as reviewable evidence only and approve Package C proof intake next; provide more Package B screenshot/video evidence; approve later FAM/runtime proof collection; approve a named visual waiver/promotion route; reject/defer/reclassify named Package B lanes; or keep PR Readiness blocked. This receipt does not authorize PR Readiness, PR creation, merge, release, FAM-003/FAM-006/FAM-007/main mutation, runtime proof generation, external-state mutation, catalog promotion, promoted-reference record creation, template creation, design-token/shared-primitive implementation, helper/validator/fixture mutation, issue mutation, cleanup, USER visual acceptance, or USER waiver.

## Template / Golden Reference Consolidated Package A-E Proof-Intake Corridor - 2026-06-17

Document Status: Non-Binding Consolidated Proof-Intake Corridor Receipt. Binding authority remains with `Docs/nexus_vision.md` for Project UI Vision and proof hierarchy, `Docs/family_visions/FAM-002_desktop_interface.md` for reusable Desktop Interface presentation grammar, `Docs/family_feature_visions/F2-FF01.md` for the UI reference-system feature-category vision, missing-proof rows, and deferred candidate preservation, `Docs/ui_reference_catalog/` for USER-promoted UI reference records only after explicit promotion approval, `Docs/phase_governance.md` for phase/blocker routing, `Docs/user_test_summary_guidance.md` for USER proof interpretation, and `Docs/validation_helper_registry.md` for future helper/validator guidance.

Corridor Result: `CONSOLIDATED PACKET GENERATED - NO PROMOTION`. Governance consolidated Packages A-E into one proof-intake review packet, classified existing FAM-006 and FAM-007 candidate evidence, preserved missing proof as blockers instead of stopping on each packet defect, and regenerated `C:\Nexus USER\Governance` plus a timestamped upload ZIP. `Docs/ui_reference_catalog/index.md` remains `Promoted Reference Count: 0`; no promoted catalog records exist. FAM-003, FAM-006, and FAM-007 remain consumer/context evidence only and are not mutation targets in this corridor.

| Package | Lane | Evidence Found | Proof Status | Missing Proof | Next Legal Route | Blocks PR Readiness? |
| --- | --- | --- | --- | --- | --- | --- |
| A | Top-level window reference | FAM-006 HUD/Recording/Log visual context and FAM-007 AI Control Center default/resize/window-control screenshots | `INSUFFICIENT` | Complete top-level window class matrix, geometry/reset proof, full control-state matrix, platform-exception classification, multi-surface comparison, and USER visual acceptance | USER-provided proof, later owning-FAM runtime proof, named waiver/reclassification, or promotion packet after proof | Yes |
| A | Window-control cluster | FAM-007 minimize/close hover and resize evidence plus FAM-002/F2-FF01 grammar | `INSUFFICIENT` | Maximize/restore/hidden-control applicability, blocked-control behavior, focus/pressed/disabled states, tooltip/accessibility/hitbox proof, child/modal distinction, and USER acceptance | Package A proof route or later promotion packet | Yes |
| B | Buttons | FAM-006 Dashboard quick-access controls and FAM-007 `RUN LOCAL CHECK` candidate evidence | `INSUFFICIENT` | Primary/secondary/danger/default/hover/focus/pressed/disabled/blocked/loading/error states, text/icon alignment, contrast, keyboard activation, hitbox/accessibility, and USER acceptance | USER-provided proof or later FAM/runtime proof | Yes |
| B | Dropdowns, menus, lists, filters | FAM-006 closed selected selector, FAM-006/FAM-007 row/card/scroll context | `MISSING / INSUFFICIENT` | Open dropdown/menu states, list row matrix, filter default/active/cleared/invalid/no-result states, keyboard/accessibility, empty/loading/error states, and USER acceptance | USER-provided proof, later FAM/runtime proof, or named reclassification | Yes |
| C | Modal/dialog surfaces | FAM-006 child/window/log/recording context and FAM-002/F2-FF01 grammar | `INSUFFICIENT` | Modal/dialog class matrix, focus trap, keyboard dismissal, confirm/cancel/destructive states, content hierarchy, and USER acceptance | Later Package C proof intake or owning-FAM runtime proof | Yes |
| C | Status/failure/recovery panels | FAM-006 returned UTS repair packet, FAM-007 provider/blocked/status context, FAM-001/FAM-002 carrydown | `INSUFFICIENT` | Runtime-truth mapping, fatal/degraded/blocked/retry/support states, recovery sequence, manual-validation route, and USER acceptance | Later Package C proof intake or FAM-001 or owning-FAM runtime proof | Yes |
| C | Tray/menu doorway and settings surfaces | F3-FF01 resident-access planning and FAM-003 context | `MISSING` | Actual tray/menu doorway visuals, Windows tray limitation handling, Global Settings/category proof, accessibility, and USER acceptance | Later FAM-003/FAM-runtime proof or USER-provided evidence | Yes |
| D | Design tokens and shared UI rules | FAM-002 grammar, F2-FF01 requirements, FAM-006/FAM-007 candidate visuals | `DEFERRED / INSUFFICIENT` | Token taxonomy, accepted values/ranges, code-to-visual trace, contrast proof, reusable primitive boundary, migration/rollback, adoption routing, and USER acceptance | Future implementation-planning carrier after visual references stabilize | Yes |
| E | Negative examples, bad fixtures, helper expectations, validator expectations | Package E planning expectations and anti-pattern classes | `DEFERRED / NO CODE MUTATION` | Executable fixtures, helper changes, validator changes, false-green regression coverage, fixture pass/fail proof, and USER approval | Future helper/validator/fixture implementation carrier after reference rules are specific | Yes unless USER reclassifies |

| Blocker | Status | Cleared By This Corridor? | Reason | Next Legal Route |
| --- | --- | --- | --- | --- |
| `Current Branch Template Work Incomplete` | Active | No | All Packages A-E remain current-PR scope and unresolved for promotion/implementation/enforcement | USER must choose proof collection, later FAM/runtime proof, waiver/reclassification, reject/defer, or keep blocked |
| `Golden Reference Promotion Blocked` | Active | No | No package has USER-approved visual acceptance, promotion packet final disposition, or catalog record | Collect proof and request a later named promotion decision |
| `Promoted Reference Count: 0` | Preserved / correct | No | Empty catalog is required because no candidate has promotion authority | Keep zero until explicit promotion approval |
| Package A proof incomplete | Active | No | Top-level window and control-cluster proof remains incomplete | Provide proof, route later proof, or reclassify/waive/reject |
| Package B proof incomplete | Active | No | Button/dropdown/menu/list/filter proof remains incomplete | Provide proof, route later proof, or reclassify/waive/reject |
| Package C proof incomplete | Active | No | Modal/dialog/status/failure/tray/settings proof remains incomplete | Provide proof, route later proof, or reclassify/waive/reject |
| Package D implementation/proof incomplete | Active | No | Design-token/shared-rule implementation and proof remain unapproved | Future implementation carrier or reclassification |
| Package E enforcement implementation incomplete | Active | No | Helper/validator/fixture code mutation remains unapproved | Future enforcement carrier or reclassification |

| Next Option | What It Would Approve | What It Would Not Approve | Legal Now? | Recommendation |
| --- | --- | --- | --- | --- |
| Accept consolidated proof-intake packet and run blocker-disposition digestion | Review one A-E table, choose proof/reclassification/defer/blocked path, and keep catalog count zero | PR Readiness, promotion, template creation, runtime proof generation, FAM mutation, helper/validator/fixture mutation, USER visual acceptance, or waiver | Yes | Recommended next true gate |
| Provide missing screenshot/video proof for named Package A-E lanes | USER-supplied evidence intake and classification without FAM mutation | Automatic promotion, catalog record creation, or USER acceptance by Codex | Yes if USER supplies evidence | Useful for A/B/C proof gaps |
| Approve later owning-FAM runtime proof collection | Future proof generation in the correct FAM/runtime carrier | Governance-side FAM mutation or runtime proof generation in this corridor | Requires later exact approval | Likely needed for tray/menu, recovery, and some control states |
| Reclassify named lanes out of current PR scope | Removes specific blockers from this PR only when USER names them | Silent deferral, deletion, or proof waiver by inference | Yes with exact USER wording | Valid if USER wants PR scope narrowed |
| Approve helper/validator/fixture implementation | Future enforcement implementation after rules are concrete | Visual proof, promotion, or current catalog population by itself | Not approved in this corridor | Wait until visual reference lanes are stable |

Next Legal Use: USER reviews the consolidated A-E proof-intake packet and chooses a blocker-disposition path. The recommended next decision is bounded blocker-disposition digestion for Packages A-E. PR Readiness remains blocked until all current-PR package lanes are completed, promoted, waived, rejected, deferred/reclassified by explicit USER decision, or otherwise legally removed from current PR scope. This receipt does not authorize PR Readiness, PR creation, merge, release, FAM-003/FAM-006/FAM-007/main mutation, runtime proof generation, external-state mutation, catalog promotion, promoted-reference record creation, template creation, design-token/shared-primitive implementation, helper/validator/fixture mutation, issue mutation, cleanup, USER visual acceptance, or USER waiver.

## Template / Golden Reference Consolidated Package A-E USER-Provided Proof Intake And Promotion-Route Packet - 2026-06-17

Document Status: Non-Binding Consolidated Proof-Intake / Promotion-Route Receipt. Binding authority remains with `Docs/nexus_vision.md`, `Docs/family_visions/FAM-002_desktop_interface.md`, `Docs/family_feature_visions/F2-FF01.md`, `Docs/ui_reference_catalog/`, `Docs/phase_governance.md`, `Docs/user_test_summary_guidance.md`, and `Docs/validation_helper_registry.md`.

Packet Result: `PACKET GENERATED - NO PROMOTION`. Governance regenerated `C:\Nexus USER\Governance` as a consolidated Package A-E USER-provided proof intake and promotion-route packet with required proof-item rows, promotion-route rows, blocker rows, copied evidence inventory, source-truth context, and exact next USER decision text. `Docs/ui_reference_catalog/index.md` remains `Promoted Reference Count: 0`; no promoted catalog records exist. FAM-003, FAM-006, and FAM-007 remain consumer/context evidence only and are not mutation targets.

| Package | Candidate | Current Proof Classification | Promotion-Route Result |
| --- | --- | --- | --- |
| A | AI Control Center / HUD top-level window reference | `INSUFFICIENT` | Strong future seed only; cannot promote until full state/class/accessibility and USER visual acceptance proof exists |
| A | Window-control cluster | `INSUFFICIENT / DUPLICATE` | FAM-007 default and minimize-hover screenshots are duplicate by SHA256; close-hover is useful but state matrix remains incomplete |
| B | Buttons | `INSUFFICIENT` | Existing FAM-006/FAM-007 button evidence is comparison proof only |
| B | Dropdowns, menus, lists, filters | `MISSING / INSUFFICIENT` | Closed selected selector and scrollbar context do not prove open menus, filters, list state matrix, or USER acceptance |
| C | Modal/dialog surfaces | `INSUFFICIENT / WRONG CANDIDATE FOR PROMOTION` | Child/window context does not prove modal/dialog taxonomy or focus/keyboard behavior |
| C | Status/failure/recovery panels | `INSUFFICIENT` | Returned UTS/FAM-007 status context is evidence, but acceptance and full recovery-state proof are missing |
| C | Tray/menu doorway and settings surfaces | `MISSING` | F3-FF01 is planning context only; real tray/menu/settings proof requires later FAM/runtime or USER evidence |
| D | Design tokens and shared UI rules | `DEFERRED / INSUFFICIENT` | Token/shared-primitive implementation and proof remain unapproved |
| E | Negative examples, bad fixtures, helper expectations, validator expectations | `DEFERRED / NO CODE MUTATION` | Executable fixtures and helper/validator changes remain unapproved |

Promotion-Route Determination: No named Package A-E candidate can move to promotion now. Package A top-level/window-control candidates are the strongest later promotion seeds, but only after missing proof and USER visual acceptance exist. Packages B and C require more USER evidence and likely later FAM/runtime proof for several lanes. Package D requires a later implementation-planning carrier. Package E requires later helper/validator/fixture mutation approval after reference rules are specific enough.

Blocker Result: `Current Branch Template Work Incomplete`, `Golden Reference Promotion Blocked`, Package A proof incomplete, Package B proof incomplete, Package C proof incomplete, Package D implementation/proof incomplete, Package E enforcement implementation incomplete, and PR Readiness blocked all remain active. This receipt does not authorize PR Readiness, PR creation, merge, release, FAM-003/FAM-006/FAM-007/main mutation, runtime proof generation, external-state mutation, catalog promotion, promoted-reference record creation, template creation, design-token/shared-primitive implementation, helper/validator/fixture mutation, issue mutation, cleanup, USER visual acceptance, or USER waiver.

Next Legal Use: USER reviews the consolidated Package A-E USER-provided proof intake and promotion-route packet and chooses a blocker-disposition path: continue proof collection, provide USER evidence, route later FAM/runtime proof, reclassify named lanes out of current PR scope, reject/defer named lanes, or keep the branch blocked.

## Template / Reference PR-Hold Posture Repair - 2026-06-16

Document Status: Non-Binding Planning Posture Repair. Binding authority remains with `Docs/phase_governance.md` for the dependency gate, `Docs/family_visions/FAM-002_desktop_interface.md` for current presentation law, and the future USER-approved template/reference carrier for any actual template, golden-reference, design-token, or shared UI primitive promotion.

Prerequisite Evidence: FAM-007 PR #262 merged, later Governance PRs #263 through #268 digested and hardened Family Feature Vision, UI, proof, and release-handoff lessons, PR #269 merged the FAM-007 AI Control Center boundary flow and H4 visual/resize/template-first evidence into `origin/main@7c26748bb6d04433a52b19d41dcacadebeb82c8e`, and USER approved bounded Governance continuation on 2026-06-16 to inspect the remaining Template/Reference dependency blocker and reconcile stale Governance external operational state records.

Disposition: `Template / Reference Plan Completed - Current Branch Completion Hold`. FAM-007 prerequisite evidence exists and the template/reference plan is complete as planning evidence, but USER clarified that all planned template/reference work belongs to the current branch/current PR. PR Readiness is blocked until that work is admitted, completed, and hardened on the current Governance branch, or USER explicitly removes/reclassifies it from the current PR scope. This repair does not create, promote, or imply a template, golden reference, design token, shared primitive, reusable component library, fixture, helper, validator, or product implementation by itself. Branches must continue to use current FAM-002 presentation grammar, phase gates, visual proof, and USER manual validation where required until a USER-approved template/reference promotion path exists.

## Template / Reference Plan Phase Entry - 2026-06-16

Document Status: Non-Binding Planning Entry. Binding authority remains with `Docs/phase_governance.md`, `Docs/family_visions/FAM-002_desktop_interface.md`, and any later USER-approved template/reference carrier. This section records prerequisite mapping only; it does not promote a template, golden reference, design token, shared primitive, fixture, helper, validator, runtime behavior, or product worktree mutation.

FAM-007 AI Control Center Evidence Digest:

- PR #269 merged at `origin/main@7c26748bb6d04433a52b19d41dcacadebeb82c8e` and is candidate evidence for future template/reference planning.
- The merged AI Control Center uses a HUD-derived WebEngine surface in `nexus_visual/ai_control_center.html`, consumes `nexus_visual/monitoring_hud.css`, records compact window-control cluster markers, keeps provider/model execution inactive, suppresses native tooltip drift, and has FAM-007-specific validation/live-resize proof.
- The H4 exhaustive inventory and visual proof remain evidence for evaluating candidate reusable references; they are not binding global template proof and cannot clear `Golden Template / Reference Promotion Blocked` without USER-approved promotion.
- The plan should evaluate AI Control Center alongside accepted HUD/FAM-006 surfaces, FAM-002 component grammar, and user-facing proof requirements before deciding whether any reference should become reusable.

Template / Reference Phase-Entry Item Map:

| Template / Reference Item | Current Owner | Current Status | Required Prerequisite | Blocker State | Can Plan Now? | Can Implement Now? | Can Promote Now? | USER Decision Needed | Recommended Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Golden window template | Future USER-approved FAM-002/template-reference carrier; FAM-002 owns presentation grammar | Candidate evidence exists from HUD/FAM-006 and PR #269 AI Control Center, but no promoted golden window exists | USER accepts planning completion and later approves promotion path after comparing candidate windows | `Golden Reference Promotion Blocked`; plan completed as evidence | Yes, as planning/evaluation only | No | No | Approve future promotion | Use the completed comparison plan as input for any later promotion decision |
| Golden control-cluster reference | FAM-002 presentation law; phase governance control grammar | AI Control Center includes compact minimize/hidden-maximize/close cluster evidence; global reference not promoted | USER promotion approval plus applicability rules for close/minimize/maximize/restore by window class | `Golden Reference Promotion Blocked` | Yes | No | No | Approve promotion after review | Treat AI Control Center cluster as candidate reference evidence, not as current law beyond existing FAM-002 grammar |
| Golden button set | FAM-002 component grammar | Current grammar covers button states; no reusable golden set promoted | USER review of button anatomy, state coverage, proof expectations | `Template Treated As Existing Proof` if inferred | Yes | No | No | Later promotion approval | Plan primary/secondary/danger/disabled/hover/focus/pressed examples and bad examples |
| Golden dialog template | FAM-002 plus consuming FAM behavior owner | Not promoted; modal/child/platform exceptions require classification | USER-approved dialog/reference planning and exception taxonomy | `Golden Reference Promotion Blocked` | Yes | No | No | Later promotion approval | Plan separate top-level, child/modal, confirmation, failure/recovery, and platform-native exception references |
| Golden status/failure panel template | FAM-001 owns fatal/recovery meaning; FAM-002 owns presentation; consuming FAM owns feature failure behavior | Durable carrydown exists; no visual reference promoted | USER-approved reference plan and failure/recovery proof classes | `Golden Reference Promotion Blocked` | Yes | No | No | Later promotion approval | Compare AI inactive/provider blocked panels, HUD state panels, and future FAM-001 recovery needs |
| Golden tray menu template | FAM-003 owns resident doorway behavior; FAM-002 presentation grammar; FAM-008 setup/education where relevant | No promoted tray/menu reference; OS tray limits remain platform reality | USER approves tray/resident template plan and Windows notification-area constraints | `Golden Reference Promotion Blocked` | Yes | No | No | Later promotion approval | Plan tray as doorway, not control room; include AI/privacy transparency and quick-access slot rules |
| FAM-002 component anatomy | `Docs/family_visions/FAM-002_desktop_interface.md` | Binding now as presentation law | None for manual enforcement; templates improve later proof | Not blocked for manual use; blocked for promoted reference claim | Yes | No new implementation here | Already binding as grammar, not as golden assets | Promotion only if turning examples into references | Continue enforcing anatomy manually with focused visual evidence |
| Reference surface library | Future USER-approved template/reference carrier | Not created/promoted; candidate sources exist and owner/location/schema recommendations are recorded below | USER approves source-truth/file creation and promotion criteria if a catalog is needed | Plan completed as evidence; catalog creation blocked | Yes | No | No | Approve source-truth/file creation if needed | Design library ownership without active-state rows or repo live proof ledgers |
| Design tokens | Future UI implementation/template carrier | Not implemented/promoted | USER approves token implementation and ownership | `Shared Primitive Promotion Blocked` | Yes, conceptually | No | No | Later implementation approval | Plan naming, scope, and validation expectations only |
| Shared UI primitives | Future UI implementation/template carrier | Not implemented/promoted | USER approves code/runtime/shared primitive work | `Shared Primitive Promotion Blocked` | Yes, conceptually | No | No | Later implementation approval | Keep future; do not create component code in this planning pass |
| Negative fixtures / bad examples | Future helper/validator cycle | Guidance exists; fixture mutation excluded now | USER approves fixture mutation | Future Helper/Validator Enforcement | Yes, as requirements | No | No | Later fixture/helper approval | Plan failures for default Windows chrome, generic dialogs, mismatched button states, unproven template claims |
| Helper/validator enforcement | `Docs/validation_helper_registry.md` for guidance; future code owner | Guidance exists; no new code approved here | USER approves helper/validator mutation | Future Helper/Validator Enforcement | Yes | No | No | Later code approval | Keep as future enforcement after template/reference plan decisions |

Phase-Entry Result: This section admitted the template/reference planning phase. The later `Template / Reference Planning Completion` section completes the plan as planning evidence and keeps actual template/reference promotion as a separate later approval.

## Template / Reference Planning Packet And PR #269 Release Target Evaluation - 2026-06-16

Document Status: Non-Binding Planning / Evaluation Receipt. Binding authority remains with `Docs/phase_governance.md` for release-floor, Release Readiness, and phase-gate law; `Docs/family_visions/FAM-002_desktop_interface.md` for current presentation grammar; `Docs/nexus_vision.md` for Project UI Vision and proof hierarchy; `Docs/family_visions/FAM-007_ai_edition_capability_trust_boundary_release_plan.md` and `Docs/family_feature_visions/FAM-007_assisted_desktop_ai_function_slice.md` for FAM-007 v1.8.0 / public-safe AI boundary intent; and any later USER-approved template/reference carrier for actual golden-reference, design-token, shared-primitive, helper, validator, or fixture promotion.

USER Versioning Clarification: The `v1.8.0-prebeta` blocker exists to keep later functional AI work separated from public-safe AI scaffolding and to prevent Codex from treating an AI-looking surface as functional AI. `v1.8.0-prebeta` should represent a real functional AI milestone, with approved provider/model/prompt execution or another USER-approved local AI execution path, edition-boundary validation, truthful provider-visible-data behavior, and any learning, memory, personalization, cache, or Owner-agent behavior handled only through the separate consent and privacy gates that source truth requires. The blocker must not force memory or learning early; it blocks public version movement until functional AI behavior is actually admitted, implemented, proven, and USER-approved.

PR #269 Evidence Summary:

- PR #269 merged FAM-007 AI Control Center boundary flow into `origin/main@7c26748bb6d04433a52b19d41dcacadebeb82c8e`.
- The merged scope added a public-safe AI Control Center surface, truthful ORIN / AI inactive status, provider-visible data `none`, deterministic no-provider local assist result flow, capability-pack eligibility with blocked install intent, public/developer/owner boundary copy, provider-state validation, public-leak prevention, compact window-control candidate evidence, tooltip suppression, and live resize proof.
- The merged scope did not approve or implement provider/model execution, prompt acceptance, prompt send, model downloads, capability-pack download/install/execution, runtime cache behavior, memory, learning, personalization, private Developer or Owner setup, Owner agents, shortcut/installer/packaging execution, or `v1.8.0` execution.

Template / Reference Evaluation Table:

| Candidate / Template Item | Evidence Source | Current Status | Required Comparison | USER Review Needed? | Can Plan Now? | Can Promote Now? | Blocker | Later Approval Needed | Recommended Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HUD Dashboard window grammar | FAM-006 family vision, HUD/Dashboard proof evidence, FAM-002 presentation grammar | Candidate reference evidence only | Compare window chrome, cards, spacing, typography, controls, proof artifacts, and USER-accepted visual behavior against Project UI Vision and FAM-002 grammar | Yes before promotion | Yes | No | `Golden Reference Promotion Blocked` | USER-approved template/reference promotion | Use as a comparison baseline, not as a promoted template |
| HUD/FAM-006 card and control references | FAM-006 HUD/Dashboard surfaces | Candidate reference evidence only | Compare card chrome, badges, state rows, dividers, buttons, hover/focus/disabled states, and density | Yes | Yes | No | `Golden Reference Promotion Blocked` | USER-approved reference selection | Include in future card/button reference review |
| AI Control Center H4 window surface | PR #269 files and FAM-007 H4 proof evidence | Candidate reference evidence only | Compare against HUD/FAM-006, FAM-002 grammar, Project UI Vision, Vision-To-Proof Matrix, focused screenshot/video proof, and USER feedback | Yes | Yes | No | `Template Treated As Existing Proof` if promoted by inference | USER-approved promotion after review | Treat as strong candidate input, not a golden reference |
| AI Control Center compact control cluster | PR #269 AI Control Center window-control cluster | Candidate control-cluster evidence | Compare close/minimize/maximize/restore applicability, hitbox, hover/focus/pressed states, accessibility, top-level window role, and exception rules | Yes | Yes | No | `Golden Reference Promotion Blocked` | USER-approved control-cluster reference | Evaluate as likely top-level control reference candidate after visual review |
| Close/minimize/maximize control cluster | FAM-002 top-level window-control grammar and PR #269 candidate evidence | Binding grammar exists; promoted visual reference does not | Compare all button states and blocked/hidden control rules by window class | Yes | Yes | No | `Template Treated As Existing Proof` | USER-approved reference/template promotion | Plan standard cluster taxonomy before implementation |
| WebEngine surface grammar | AI Control Center WebEngine surface and current HUD WebEngine reuse | Candidate implementation pattern | Compare offline/local behavior, styling inheritance, backend truth mapping, frame/window ownership, and proof route | Yes | Yes | No | `Shared Primitive Promotion Blocked` | Later implementation/reference approval | Keep as candidate; do not infer WebEngine as mandatory global window tech |
| `monitoring_hud.css` reuse | PR #269 reused HUD CSS plus AI-specific additions | Candidate shared-style evidence | Compare whether reuse is stable, intentional, non-leaky, and compatible with future FAM-006/FAM-007 surfaces | Yes | Yes | No | `Shared Primitive Promotion Blocked` | Later design-token/shared-style approval | Evaluate for token extraction, not direct promotion |
| Button grammar | FAM-002 component anatomy plus HUD/FAM-006 and AI Control Center examples | Binding current grammar; no golden button set | Compare label, size, border, glow, icon/text, hover/focus/pressed/disabled, destructive/secondary role, and proof states | Yes | Yes | No | `Golden Template / Reference Promotion Blocked` | USER-approved button reference | Plan button-state matrix and bad examples |
| Dropdown/menu grammar | FAM-002 grammar plus current FAM-006/FAM-007 surfaces where available | No promoted reference yet | Compare trigger, menu body, checkbox/state rows, filters, keyboard/focus, clipping, scroll, and disabled states | Yes | Yes | No | `Golden Reference Promotion Blocked` | USER-approved dropdown/menu reference | Include dropdowns and menus in template plan, not only windows/buttons |
| Modal/dialog grammar | FAM-002 grammar and existing dialog/child-window behavior | Not promoted | Compare modal versus child versus top-level window role, footer actions, close semantics, platform-native exceptions, and proof route | Yes | Yes | No | `Golden Reference Promotion Blocked` | USER-approved dialog reference | Keep top-level controls separate from content/modal actions |
| Status/failure panel grammar | FAM-001 diagnostics/recovery direction, FAM-002 presentation grammar, AI Control Center blocked-state panels, HUD status panels | Candidate evidence only | Compare error/failure wording, recovery route, truthfulness, severity, local/privacy boundaries, and USER proof needs | Yes | Yes | No | `Golden Reference Promotion Blocked` | USER-approved status/failure reference | Plan status/failure panel reference with recovery and fallback classes |
| Tray/menu doorway grammar | FAM-003 resident access vision, FAM-002 presentation grammar, AI/privacy visibility vision | Future candidate; no golden tray reference | Compare doorway model, quick-access limits, privacy/status surfaces, Windows tray constraints, and settings/global doorway boundaries | Yes | Yes | No | `Golden Reference Promotion Blocked` | USER-approved tray/menu reference | Keep tray as doorway; avoid turning it into the full control room |
| Design-token candidates | FAM-002 grammar, HUD/FAM-006, AI Control Center CSS | Conceptual only | Compare color, spacing, radii, typography, glow, borders, density, component-state tokens, and source ownership | Yes | Yes | No | `Shared Primitive Promotion Blocked` | USER-approved token implementation | Plan tokens after reference surfaces are selected |
| Shared UI primitive candidates | Future UI implementation/template carrier | Not admitted for implementation | Compare ownership, reuse boundaries, API shape, backend-state mapping, and proof obligations | Yes | Yes | No | `Shared Primitive Promotion Blocked` | USER-approved implementation | Do not create shared primitives in this docs-only pass |
| Negative fixture candidates | Future helper/validator fixture cycle | Requirements only | Compare bad examples for OS chrome, mismatched button states, template-shell proof, missing screenshots, circular validation, and unproven reference claims | Yes for fixture set selection | Yes | No | Future Helper/Validator Enforcement | USER-approved fixture mutation | Preserve as future hardening after reference decisions |
| Helper/validator future enforcement candidates | `Docs/validation_helper_registry.md` | Guidance only | Compare against current binding rules and future machine-checkable possibilities | No for planning; yes for code mutation | Yes | No | Future Helper/Validator Enforcement | USER-approved helper/validator mutation | Keep current pass docs-only; future validators can enforce selected templates |

PR #269 Release Target Evaluation Table:

| Release Option | Required Evidence | PR #269 Evidence Found | Gate Satisfied? | Version Rationale Status | USER Decision Needed? | Recommendation |
| --- | --- | --- | --- | --- | --- | --- |
| `v1.7.x patch prerelease` | Latest public prerelease plus release-bearing patch-floor rationale showing work remains below the `v1.8.0` functional AI gate | Latest public prerelease is `v1.7.33-prebeta`; PR #269 delivers public-safe AI boundary UI/status/no-provider behavior and keeps provider/model/prompt/download/cache/memory/private setup blocked | Yes, if release target fields are recorded before Release Readiness | Missing from merged PR #269 source truth; suitable rationale can be stated deterministically | USER must approve the legal repair carrier for missing release-target contract and any release execution separately | Recommended target posture if release proceeds now: `Release Floor: patch prerelease`, likely next public prerelease `v1.7.34-prebeta`, because PR #269 is below the functional AI milestone |
| Minor prerelease | New executable/runtime/operator-facing/user-facing or materially expanded product capability lane, with no conflicting milestone gate | PR #269 is user-facing/runtime UI, but the next minor from `v1.7.33-prebeta` is `v1.8.0-prebeta`, and FAM-007 source truth reserves that for functional AI plus edition-boundary validation | No under current FAM-007 gate | Weak/blocked because minor movement would collide with the `v1.8.0` functional AI threshold | USER could later reclassify the release strategy, but current source truth does not support it | Do not use minor movement for PR #269 unless USER explicitly changes the public versioning strategy and source truth |
| Aggregation hold | Evidence that the branch is release-bearing but should wait for a larger USER-approved family release or future aggregation target | PR #269 could be treated as merged-unreleased aggregation evidence while release target fields were missing | Partially; it explained hold posture, but it did not clear `Release Target Undefined` by itself | Pre-repair durable release target/floor/scope/artifact fields were the blocker | USER decision required if deferring release rather than publishing next patch prerelease | Valid as a temporary blocked posture; not a substitute for release-target markers |
| `v1.8.0-prebeta` | Functional public AI execution or another USER-approved functional AI path; provider setup/consent truth; provider-visible-data boundary; `canAcceptPrompts` approved/validated; prompt/model execution proof; network/download/cache/memory gates explicit; public notes do not imply private Owner/Developer capability | PR #269 proves the opposite boundary: no provider/model execution, no prompt acceptance/send, no downloads, no runtime cache, no memory/learning/personalization, no private setup, provider-visible data none | No | Blocked by FAM-007 vision and FFV explicit non-goals | Would require later USER-approved FAM-007 functional-AI work and Release Readiness approval | Reject for PR #269 |
| Blocked pending Version Rationale / USER decision | Required release-target fields absent or semantically unresolved | The prior Release Readiness digest reported missing `Release Target:`, `Release Floor:`, `Version Rationale:`, `Release Scope:`, `Release Artifacts:`, and `Post-Release Truth:` | Pre-repair only; the legal repair carrier later recorded the missing fields | Missing in the merged PR #269 release-bearing truth before the repair closure | USER decision required for the legal repair carrier and separate release execution | Pre-repair posture was `Release Target Undefined`; recommended rationale was patch-floor / v1.7.x, not v1.8.0 |

Release-Target Recommendation:

- PR #269 should not be treated as `v1.8.0-prebeta` because it did not implement functional public AI, provider/model execution, prompt send/acceptance, downloads, runtime cache, memory, learning, personalization, or private Developer/Owner setup.
- PR #269 is release-bearing public-safe product work, but its deterministic release-floor recommendation is `patch prerelease` on the `v1.7.x-prebeta` line unless USER explicitly changes the public versioning strategy.
- Before the repair closure below, the missing release-target contract was a real blocker: Release Readiness could not green until a legal carrier recorded `Release Target:`, `Release Floor:`, `Version Rationale:`, `Release Scope:`, `Release Artifacts:`, and `Post-Release Truth:` or USER selected a lawful hold/repair route.
- Proposed Version Rationale text for the legal repair carrier: `PR #269 delivers public-safe FAM-007 AI Control Center boundary UI/status and deterministic no-provider assist behavior while preserving provider/model execution, prompt send/acceptance, downloads, runtime cache, memory/learning/personalization, private setup, packaging, and v1.8.0 as future-gated. Because the FAM-007 v1.8.0 Functional AI Gate is not satisfied, the release floor is patch prerelease on the v1.7.x public prebeta line.`

Planning Result: The Template / Reference plan is completed as non-binding planning/evaluation evidence for the current Governance path. The plan classified candidate evidence, compared the accepted HUD/FAM-006 and PR #269 AI Control Center evidence against Project UI Vision and FAM-002 presentation grammar, defined future promotion criteria, and recorded owner/location/schema recommendations. It cannot promote a golden reference, template, design token, shared primitive, helper, validator, fixture, or active product implementation by itself. USER later clarified that all planned template/reference work belongs to the current branch/current PR, so PR Readiness remains blocked until that work is admitted, completed, and hardened on this branch, or USER explicitly removes/reclassifies it from current scope. Codex must not imply that a template, golden reference, design token, shared primitive, helper, validator, fixture, or product-worktree adoption is already promoted. Separately, PR #269 release-target repair was necessary before Release Readiness could green for that merged release-bearing scope; the repair closure below records the durable contract location.

### Template / Reference Planning Completion - 2026-06-16

Completion Status: `Template / Reference Plan Completed - Current Branch Completion Hold`.

This completion closes the plan-completion portion of the PR-hold blocker only. It does not close `Golden Reference Promotion Blocked`, `Shared Primitive Promotion Blocked`, `Future Helper/Validator Enforcement`, or active FAM adoption requirements. USER later clarified that those planned work areas should not be deferred beyond the current branch/current PR by default; they must be admitted and completed here or explicitly removed/reclassified by USER before PR Readiness.

### Current Branch Full Work Completion Hold - 2026-06-16

USER Direction: `All work that is planned for the Governance reliability / vision / proof / template-reference track must be digested, planned, admitted, and completed for the current Governance branch and intended current PR before PR Readiness. Do not proceed to PR until all admitted planned work is done.`

Current Branch Disposition: `Template / Reference Plan Completed - Current Branch Completion Hold`.

Current Branch Required Next Work:

- Admit a bounded Template / Golden Reference Promotion cycle on this Governance branch.
- Decide and create the durable owner surface for template/reference truth only if current source truth and USER approval permit it.
- Promote only USER-reviewed references/templates; candidate evidence from HUD/FAM-006 and PR #269 AI Control Center remains non-binding until promotion.
- Decide whether design tokens, shared primitives, helper/validator code, fixtures, and product-worktree adoption are admitted into this current branch or explicitly deferred/reclassified by USER before PR Readiness.
- Run final integration hardening after the admitted template/reference work is complete.

PR Hold Rule: `PR Readiness Stage 1 is blocked while Current Branch Template Work Incomplete remains active. Plan completion alone is not a PR-readiness gateway for this branch.`

Allowed Exit From This Hold:

- `Completed On Current Branch`: USER approves the remaining template/reference cycle or cycles, the work is implemented or source-truth-promoted as approved, final integration hardening is green, and PR Readiness is separately approved.
- `Explicit USER Reclassification`: USER explicitly removes or defers a planned item from current PR scope with reason, preserving it as future work without ambiguity.
- `Explicit Limited PR Path`: USER explicitly approves a limited PR path despite incomplete planned work. This is not the current default.

Candidate Evidence Classification:

| Candidate Evidence | Planning Classification | Strong Future Use | Invalid Use |
| --- | --- | --- | --- |
| HUD/FAM-006 Dashboard and monitoring surfaces | Candidate visual reference evidence | Compare dashboard framing, cards, rows, status language, density, visual proof, and USER-accepted behavior | Treat as a promoted global template without USER promotion |
| HUD/FAM-006 card/control behavior | Candidate component evidence | Compare card anatomy, buttons, badges, status rows, dividers, scroll behavior, and disabled/degraded states | Treat as complete button/card template coverage |
| PR #269 AI Control Center H4 surface | Candidate top-level AI/control-surface evidence | Compare compact window chrome, AI inactive/provider-blocked state, no-provider flow, WebEngine styling, and resize proof | Treat as functional AI, v1.8.0 proof, or global UI proof |
| PR #269 compact control cluster | Strong candidate control-cluster evidence | Evaluate as likely close/minimize/hidden-maximize top-level window-control reference with per-window applicability | Apply blindly to child/modals or treat as universal without exception rules |
| FAM-002 component grammar | Binding presentation grammar now | Govern visual law for Nexus-owned UI while references remain unpromoted | Treat prose grammar as a promoted screenshot/template artifact |
| Project UI Vision | Binding project-wide UI/UX principle now | Govern deterministic, intuitive, immersive, predictable, evidence-backed UI expectations | Treat as a component-library implementation |

Recommended Future Owner / Location Model:

- Binding presentation law remains in `Docs/family_visions/FAM-002_desktop_interface.md` and Project-wide UI principles remain in `Docs/nexus_vision.md`.
- If USER wants a durable feature-category carrier before implementation, create a future FAM-002 Family Feature Vision such as `F2-FF01 Nexus UI Reference System` under `Docs/family_feature_visions/` after explicit approval. That FFV would own reference-system vision, element-group categories, deferred reference items, and promotion criteria.
- If USER later approves durable promoted reference artifacts, create a future reference catalog owner such as `Docs/ui_reference_catalog/` only for promoted references. That catalog must store durable reference contracts and accepted proof pointers, not active branch status, live evidence rows, current defect ledgers, or temporary LV artifacts.
- Code templates, design tokens, shared UI primitives, fixture files, helper code, and validator code require later implementation authority in the owning carrier. This planning completion does not create or mutate them.

Promotion Packet Schema:

Any future template/reference promotion packet should include: `Reference ID`, `Reference Name`, `Reference Class`, `Owner`, `Source Evidence`, `Accepted Visual Baseline`, `Applicable Surface Classes`, `Non-Applicable Classes`, `Required Element Groups`, `Required States`, `Geometry / Resize / Accessibility Expectations`, `Proof Artifacts`, `USER Acceptance Receipt`, `Known Limitations`, `Adoption Rule`, `Validator Guidance`, `Promotion Result`, and `Final Disposition`.

Future Promotion Criteria:

- The candidate has focused screenshot/video or frame-sequence proof for the relevant USER-visible states.
- The candidate is compared against Project UI Vision, FAM-002 grammar, and at least one accepted surface of the same class.
- The promotion packet names where the reference applies, where it does not apply, and how child/modal/top-level/diagnostic/platform-native exceptions work.
- The promotion packet proves element-group anatomy and state behavior, including hover, focus, pressed, disabled, blocked, degraded, empty, error, resize, and recovery states where applicable.
- USER explicitly accepts the promoted reference, waives a gap, or requests revision before the reference becomes durable proof authority.
- Helper/validator enforcement remains future until USER approves code/fixture mutation and the selected references are machine-checkable.

Blocker Disposition:

| Blocker | Planning Completion Disposition |
| --- | --- |
| `Template / Reference Plan Blocked` | Closed as planning-only when USER accepts this completion receipt |
| `Template Dependency Unresolved` | Closed only for plan routing; remains active for any claim that a template already exists |
| `Golden Reference Promotion Blocked` | Still active until USER approves and accepts reference promotion |
| `Shared Primitive Promotion Blocked` | Still active until USER approves implementation |
| `Template Treated As Existing Proof` | Preventive blocker remains active |
| `Future Helper/Validator Enforcement` | Still future-gated until USER approves helper/validator/fixture mutation |

Next Legal Decision:

USER's current selected path is to keep the Governance branch open and perform the planned template/reference work before PR Readiness. The next legal decision is not PR Readiness; it is whether to admit the bounded Template / Golden Reference Promotion cycle on this current Governance branch, including the exact owner files, artifact/reference locations, schema, USER review packet, validation, and non-includes. This does not authorize release, PR creation, merge, FAM worktree mutation, external-state mutation, issue mutation, helper/validator code, fixture mutation, design-token/shared-primitive implementation, or runtime/provider/private/cache/memory work without separate approval.

### Template / Golden Reference Promotion Admission Cycle - 2026-06-16

Admission Status: `Admission Packet Completed - Implementation Approval Required`.

This admission cycle classifies the remaining current-branch template/reference work. It does not create templates, promote golden references, implement design tokens, implement shared UI primitives, mutate helpers, mutate validators, mutate fixtures, mutate FAM worktrees, mutate external state, create issues, create a PR, merge, release, or clear `Current Branch Template Work Incomplete` by itself.

Current Branch Template Work Incomplete Result: `Still Active`. The blocker can clear only after USER approves and the branch completes the admitted current-branch template/reference work with final hardening, or USER explicitly removes/reclassifies the work from the current PR scope.

Required Admission Table:

| Work Item | Current Owner | Evidence Source | Current Status | Admission Decision | Can USER Review Now? | Can Implement Now? | Can Promote Now? | Blocker | Required Next Approval | Recommended Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Golden window template | Future USER-approved FAM-002/template-reference carrier; FAM-002 owns presentation grammar | HUD/FAM-006 surfaces, PR #269 AI Control Center, Project UI Vision, FAM-002 grammar | Candidate evidence only; no promoted golden window exists | Advance to USER visual review first | Yes | No | No | `Golden Reference Promotion Blocked` | USER approval for reference-review packet, then promotion implementation | Compare candidate window classes and decide whether to promote a top-level window reference |
| Golden control-cluster reference | FAM-002 presentation law and phase governance control grammar | PR #269 compact close/minimize/hidden-maximize evidence; FAM-002 top-level control grammar | Strong candidate evidence; no global reference promoted | Advance to USER visual review first | Yes | No | No | `Golden Reference Promotion Blocked` | USER approval for control-cluster reference review and promotion | Evaluate close/minimize/maximize/restore applicability by window class before promotion |
| Close/minimize/maximize control cluster | FAM-002 top-level window-control grammar | PR #269 AI Control Center compact cluster and FAM-002 grammar | Binding grammar exists; visual reference not promoted | Admit for later promotion packet after USER visual review | Yes | No | No | `Template Treated As Existing Proof` if inferred | USER approval for promotion implementation | Treat as likely first control-cluster reference, not universal law until accepted |
| Golden button set | FAM-002 component anatomy | FAM-002 grammar, HUD/FAM-006 buttons, AI Control Center buttons | Binding grammar exists; no golden button set | Advance to USER visual review first | Yes | No | No | `Golden Template / Reference Promotion Blocked` | USER approval for button reference selection and promotion | Define primary, secondary, danger, disabled, hover, focus, pressed, loading, and blocked states |
| Golden dropdown/menu reference | FAM-002 component grammar; consuming FAM owns feature behavior | FAM-006 dropdown/menu evidence, current FAM-002 grammar, USER concern about dropdown coverage | Candidate class identified; no promoted reference | Advance to USER visual review first | Yes | No | No | `Golden Reference Promotion Blocked` | USER approval for dropdown/menu reference review and promotion | Include dropdown triggers, checkbox rows, filters, scroll/clipping, keyboard/focus, and disabled states |
| Modal/dialog template | FAM-002 presentation grammar; consuming FAM owns dialog behavior | Existing FAM-002 modal/child/platform exception rules | Not promoted | Advance to USER visual review first | Yes | No | No | `Golden Reference Promotion Blocked` | USER approval for dialog taxonomy and promotion | Separate top-level windows, child windows, modal confirmations, footer/content close actions, and platform-native exceptions |
| Status/failure panel template | FAM-001 owns fatal/recovery meaning; FAM-002 owns presentation; consuming FAM owns feature behavior | FAM-001/FAM-002 carrydown, HUD status panels, AI Control Center blocked-state panels | Candidate evidence only | Advance to USER visual review first | Yes | No | No | `Golden Reference Promotion Blocked` | USER approval for status/failure reference review | Promote only with clear recovery route, severity, privacy, fallback, and proof-class expectations |
| Tray/menu doorway template | FAM-003 owns resident doorway behavior; FAM-002 owns presentation; FAM-008 owns setup education where applicable | Project tray/privacy vision, F3-FF01, FAM-002 grammar | Candidate future template; no promoted tray/menu reference | Advance to USER visual review first | Yes | No | No | `Golden Reference Promotion Blocked` | USER approval for tray/menu doorway reference review | Keep tray as a doorway with quick-access limits and privacy/status routing, not a deep control room |
| HUD/FAM-006 surface reference | FAM-006 owns monitoring/HUD behavior; FAM-002 owns reusable presentation law | FAM-006 family vision, Dashboard/HUD evidence, visual-system inheritance rules | Candidate comparison baseline only | Advance to USER visual review first | Yes | No | No | `Template Treated As Existing Proof` if promoted by inference | USER approval before any FAM-006 surface becomes a reference | Use as comparison evidence for windows, cards, rows, buttons, status language, density, and proof expectations |
| PR #269 AI Control Center surface reference | FAM-007 owns AI Control Center behavior; FAM-002 owns reusable presentation law | PR #269 merged AI Control Center, H4 visual/resize/template-first proof, F7-FF01 | Strong candidate evidence only | Advance to USER visual review first | Yes | No | No | `Template Treated As Existing Proof` if promoted by inference | USER approval before using as a golden reference | Compare against HUD/FAM-006 and FAM-002 before selecting any reusable pieces |
| FAM-002 component anatomy | `Docs/family_visions/FAM-002_desktop_interface.md` | Current source truth | Binding presentation grammar already exists | Keep binding now; no promotion needed unless turning examples into references | Yes | No new implementation in this pass | Already binding as grammar, not as assets | `Current Branch Template Work Incomplete` for reference promotion, not manual grammar use | USER approval only if promoting examples/assets | Continue enforcing manually in BP/H/Live Validation while references are unpromoted |
| Reference surface library | Future USER-approved template/reference carrier | Current owner/location/schema recommendation | Not created | Admit for later implementation packet only | Yes, as proposed schema | No | No | `Golden Reference Promotion Blocked` | USER approval to create the durable carrier and initial catalog | Recommended future path: FAM-002 FFV plus optional `Docs/ui_reference_catalog/` for promoted references only |
| Design-token candidates | Future UI implementation/template carrier; FAM-002 governs intent | HUD/FAM-006 CSS, AI Control Center CSS, FAM-002 grammar | Candidate analysis only | Reclassify as future blocked lane unless USER explicitly admits implementation | Yes, conceptually | No | No | `Shared Primitive Promotion Blocked` | USER approval for implementation after references are selected | Do not admit into current branch by default; extract after promoted references exist |
| Shared UI primitive candidates | Future UI implementation/template carrier | FAM-002 grammar, candidate windows, current product UI code | Not admitted | Reclassify as future blocked lane unless USER explicitly admits implementation | Yes, conceptually | No | No | `Shared Primitive Promotion Blocked` | USER approval for code/runtime implementation | Keep out of current docs-only admission; do not create component code here |
| Negative fixtures / bad examples | `Docs/validation_helper_registry.md` for future helper/validator guidance | Current governance guidance and known failure classes | Guidance only; fixtures not created | Reclassify as future helper/validator lane unless USER explicitly admits fixture work | Yes, as scenario list | No | No | `Future Helper/Validator Enforcement` | USER approval for fixture mutation | Preserve examples for later validator hardening; do not mutate fixture files here |
| Helper/validator enforcement | `Docs/validation_helper_registry.md` plus future code owners | Current helper guidance; existing validators | Future guidance only for new template references | Reclassify as future blocked lane unless USER explicitly admits code changes | Yes, as enforcement plan | No | No | `Future Helper/Validator Enforcement` | USER approval for helper/validator mutation | Current Codex must enforce binding rules manually; code enforcement waits for selected references |
| FAM-006/FAM-007 adoption | Affected FAM worktrees at their next legal gate | Merged source truth, Merged Vision / Proof Standard Adoption Gate | Future next-gate requirement; no sibling mutation | Reclassify as next-legal-gate adoption outside this Governance branch | Yes, as requirement | No | No | `FAM Worktree Mutation Approval Missing` if attempted here | USER approval inside each FAM lane at next gate | FAM branches must inventory current branch output against merged UI/proof/template standards after rebaseline |
| PR #269 release-target contract | FAM-007 branch record plus phase release-floor rules | `Docs/branch_records/feature_fam_007_three_ndai_assisted_ai_function_slice.md` repair receipt | Repaired as source-truth contract; release execution still gated | Treat as separate PR-readiness risk to re-verify, not a template blocker | Yes, as risk review | No | No | Release execution approval missing; not current template blocker | Later Release Readiness / release execution approval if USER chooses | Re-verify during PR/RR packets; do not edit in this admission cycle |

Owner / Location / Schema Recommendation:

- Keep binding UI law in `Docs/nexus_vision.md` and `Docs/family_visions/FAM-002_desktop_interface.md`.
- If USER approves durable reference-system vision, create a future FAM-002 Family Feature Vision such as `F2-FF01 Nexus UI Reference System` under `Docs/family_feature_visions/`.
- If USER approves promoted reference artifacts, create a future reference catalog such as `Docs/ui_reference_catalog/` for promoted references only. That catalog must store durable reference contracts, accepted proof pointers, surface applicability, non-applicability, state coverage, USER acceptance receipts, known limitations, adoption rules, and validator guidance.
- Do not store active proof ledgers, current UI defect rows, live validation artifacts, PR state, issue state, or current adoption state in the catalog. Those remain in active external branch plans, USER packets, helper output, validator output, evidence roots, Codex digests, Git, GitHub, or `C:\Nexus Governance State` as routed by source truth.

Candidate References Advancing To USER Review: golden window template, golden control-cluster reference, close/minimize/maximize control cluster, golden button set, golden dropdown/menu reference, modal/dialog template, status/failure panel template, tray/menu doorway template, HUD/FAM-006 surface reference, PR #269 AI Control Center surface reference, FAM-002 component anatomy, and reference surface library schema.

Explicitly Deferred Or Reclassified Unless USER Admits Them Now: design-token implementation, shared UI primitive implementation, negative fixture mutation, helper/validator code mutation, and active FAM-006/FAM-007 adoption worktree mutation.

USER Review Requirements Before Promotion:

- USER-facing visual review packet comparing candidate references against Project UI Vision, FAM-002 presentation grammar, accepted HUD/FAM-006 surfaces, PR #269 AI Control Center evidence, Vision-To-Proof Matrix requirements, Scope Coverage Manifest expectations, and USER proof hierarchy.
- Per-reference decision rows: accept, revise, reject, waive gap, or defer.
- For each accepted reference: applicable surface classes, non-applicable classes, required element groups, required states, proof artifacts, known limitations, adoption rule, and final disposition.

Admission Result: This cycle can produce the next implementation approval packet. It cannot clear `Current Branch Template Work Incomplete` by itself because actual reference promotion, catalog creation, design tokens, shared primitives, helpers, validators, fixtures, and product-worktree adoption remain unapproved or explicitly reclassified.

### Template / Golden Reference USER Visual Review Packet - 2026-06-16

Packet Status: `Repaired - USER Candidate Decision Packet Only`.

Packet Location: `C:\Nexus USER\Governance`.

Packet Purpose: The local USER review packet compares the admitted candidate references against Project UI Vision, FAM-002 presentation grammar, accepted HUD/FAM-006 evidence, PR #269 AI Control Center evidence, Vision-To-Proof Matrix expectations, Scope Coverage Manifest expectations, and USER proof hierarchy. It records USER decision rows for accept, revise, reject, waive gap, or defer.

Packet Boundary: The packet is review evidence only. It does not create a FAM-002 FFV, create `Docs/ui_reference_catalog/`, promote a golden reference, create a template, implement design tokens, implement shared primitives, mutate helpers, mutate validators, mutate fixtures, mutate FAM worktrees, mutate external state, create issues, create a PR, merge, release, move/delete/archive files, or clear `Current Branch Template Work Incomplete`.

Visual-Evidence Repair: USER/ChatGPT review found that the initial packet was text-only and therefore not valid as a visual-review packet. Governance repaired the packet by including selected visual artifacts for FAM-007 H4 AI Control Center and FAM-006 HUD/Dashboard candidate evidence, adding explicit proof pointers, adding a missing-proof list, and reclassifying the packet as a candidate decision packet rather than a completed visual acceptance packet.

Candidate Disposition: Visual-dependent candidate rows must remain `REVISE` or `DEFER` until the selected candidate has focused screenshot, video, ordered frame-sequence, or USER-validated proof that covers the relevant element groups, states, applicability, non-applicability, and exception rules. FAM-002 component anatomy remains binding presentation grammar, but candidate screenshots do not become promoted templates or golden references without a later USER-approved promotion carrier.

Next Legal Use: USER/ChatGPT review should decide which candidate references, if any, advance to the next bounded digestion and promotion-planning packet. Any accepted candidate still requires a later USER-approved implementation carrier before durable reference files, catalog records, templates, helper enforcement, validator enforcement, fixtures, or product-worktree adoption can be created. PR Readiness remains blocked while `Current Branch Template Work Incomplete` is active.

### Template / Golden Reference Candidate Decision Digestion - 2026-06-16

Document Status: Non-Binding Candidate-Decision Receipt. Binding authority remains with the named owner files: `Docs/nexus_vision.md` for Project UI Vision, `Docs/family_visions/FAM-002_desktop_interface.md` for current presentation grammar, phase/branch-planning owners for proof gates, `Docs/validation_helper_registry.md` and `dev/orin_user_review_bundle.py` for USER review packet helper expectations, and any later USER-approved FAM-002 FFV or reference catalog for future promoted references.

Reviewed Packet:

- Packet path: `C:\Nexus USER\Governance`
- Reviewed ZIP: `C:\Nexus USER\Governance-20260616-122646.zip`
- Reviewed ZIP SHA256: `4EFBD274552803A1F8E505FCBC0B0D1CA3BD62878F563ED10A006E9EBAF26BD8`
- File count: `26`
- Packet disposition: `USER Candidate Decision Packet Only`

Applied USER Decisions:

| Candidate / Work Item | USER Decision | Recorded Disposition | Missing Proof / Requirement | Current Blocker Result |
| --- | --- | --- | --- | --- |
| FAM-002 component anatomy | Accept as binding grammar only | `Accepted As Binding Grammar - Not Promoted Visual Proof` | None for grammar; future visual references still need proof and USER promotion | Does not clear template/reference blockers |
| HUD/FAM-006 surface reference | Advance to promotion planning with REVISE requirements | `Advance To Promotion Planning - REVISE` | USER side-by-side adjudication, exact accepted surface list, state coverage, known limitations, and class applicability | `Golden Reference Promotion Blocked` remains active |
| PR #269 AI Control Center surface reference | Advance to promotion planning with REVISE requirements | `Advance To Promotion Planning - REVISE` | USER visual adjudication against Project UI Vision/FAM-002, side-by-side with FAM-006, accepted pieces, state coverage, known limitations | `Golden Reference Promotion Blocked` remains active |
| Golden window reference | Advance to promotion planning with REVISE requirements | `Advance To Promotion Planning - REVISE` | Top-level, child, modal, tray-opened, status/failure, platform-exception, geometry, resize, and visual-inheritance comparison | `Golden Reference Promotion Blocked` remains active |
| Golden control-cluster reference | Advance to promotion planning with REVISE requirements | `Advance To Promotion Planning - REVISE` | Close/minimize/maximize/restore applicability by window class, hidden/disabled/focus/keyboard/tooltip/hitbox states, child/modal exceptions | `Golden Reference Promotion Blocked` remains active |
| Close/minimize/maximize cluster reference | Advance to promotion planning with REVISE requirements | `Advance To Promotion Planning - REVISE` | Maximize/restore proof, disabled states, child/modal/platform exceptions, accessibility/focus states, and class-by-class applicability | `Golden Reference Promotion Blocked` remains active |
| Full golden button set | Defer until full proof exists | `Deferred - Missing Button-State Proof` | Primary, secondary, danger, disabled, hover, focus, pressed, loading, blocked/future-gated, compact/default states across surfaces | Future proof/promotion required |
| Dropdown/menu reference | Defer until full proof exists | `Deferred - Missing Dropdown/Menu Proof` | Trigger, open, hover, selected, disabled, scrolling, clipping, keyboard/mouse, close/reopen, stale-highlight, checkbox/filter rows | Future proof/promotion required |
| Modal/dialog template | Defer until visual proof exists | `Deferred - Missing Modal/Dialog Proof` | Modal, child window, confirmation, footer/content close, platform exception screenshots and proof | Future proof/promotion required |
| Status/failure panel template | Defer until taxonomy proof exists | `Deferred - Missing Status/Failure Taxonomy Proof` | Failure, degraded, blocked, unavailable, disabled, recovery, privacy, support/log/bundle, and severity examples | Future proof/promotion required |
| Tray/menu doorway template | Defer until FAM-003/FAM-008 proof exists | `Deferred - Missing Tray/Menu Doorway Proof` | Actual tray/menu doorway screenshots, quick-access layout, privacy/status routes, settings/AI/HUD doorway examples | Future proof/promotion required |
| Design-token implementation | Defer | `Deferred - Implementation Not Admitted` | USER-approved implementation carrier after accepted references | `Shared Primitive Promotion Blocked` remains active |
| Shared UI primitive implementation | Defer | `Deferred - Implementation Not Admitted` | USER-approved implementation carrier after accepted references | `Shared Primitive Promotion Blocked` remains active |
| Negative fixtures / bad examples | Defer | `Deferred - Fixture Mutation Not Admitted` | USER-approved fixture/helper/validator hardening carrier | `Future Helper/Validator Enforcement` remains active |
| Helper/validator enforcement | Defer | `Deferred - Code Mutation Not Admitted` | USER-approved helper/validator mutation after references are selected | `Future Helper/Validator Enforcement` remains active |
| FAM-006/FAM-007 adoption mutation | Defer | `Deferred - Active FAM Mutation Not Admitted` | Each FAM worktree evaluates merged standards at its next legal gate after rebaseline | FAM mutation remains blocked |

Packet-Generation Governance Drift Review:

- Current source truth already requires local USER packets to be regenerated from a clean worktree-labeled folder under `C:\Nexus USER\<label>`.
- Current source truth already requires `START_HERE.md`, exactly one primary current-gate file under `USER Review`, supporting review aids under `Review Aids`, copied repo context under `Source Truth Context`, and no stale folder contents.
- Current source truth already requires a mandatory timestamped upload ZIP shaped `C:\Nexus USER\<label>-YYYYMMDD-HHMMSS.zip`, plus removal of legacy same-name `C:\Nexus USER\<label>.zip` and previous same-label timestamped zips.
- Packet drift correction: the stable `C:\Nexus USER\Governance.zip` artifact was drift because source truth already requires timestamped upload zips. It was removed as a legacy same-name artifact and replaced with `C:\Nexus USER\Governance-20260616-122646.zip`.
- Next generated USER packets for this branch must use the helper-shaped packet and timestamped ZIP contract or explicitly record a USER waiver. Any future stable `Governance.zip` upload must be treated as stale/legacy unless USER explicitly approves a one-off waiver before packet generation.

Future Carrier Recommendation:

- Recommended next carrier model: `Both, staged`.
- A future FAM-002 Family Feature Vision, likely `F2-FF01 Nexus UI Reference System`, should own durable feature-category vision for the UI reference system, element-group classes, missing-proof requirements, candidate grouping, deferred reference items, and promotion criteria.
- A future `Docs/ui_reference_catalog/` surface should exist only if USER approves durable promoted reference contracts. It should store accepted reference IDs, applicability, non-applicability, accepted visual baseline pointers, proof artifacts, USER acceptance receipts, known limitations, adoption rules, and validator guidance.
- The future catalog must not store active proof ledgers, current defect rows, live branch status, current adoption status, PR status, release-window state, temporary LV artifacts, or mutable screenshot inventories. Those remain in USER packets, helper output, validator output, Codex digests, evidence roots, Git/GitHub, or external operational state.
- Do not create the FAM-002 FFV or `Docs/ui_reference_catalog/` in this digestion pass. Creation requires the next exact USER approval.

Blocker Status After USER Decisions:

- `Current Branch Template Work Incomplete`: still active.
- `Golden Reference Promotion Blocked`: still active.
- `Shared Primitive Promotion Blocked`: still active.
- `Future Helper/Validator Enforcement`: still active.
- PR Readiness remains blocked.

### Template / Golden Reference Missing-Proof / Promotion-Planning Packet Repair - 2026-06-16

Document Status: Non-Binding Packet-Stage Repair Receipt. Binding authority remains with `Docs/development_rules.md`, `Docs/phase_governance.md`, and `Docs/validation_helper_registry.md` for clean USER packet regeneration and timestamped upload ZIP rules; `Docs/nexus_vision.md` and `Docs/family_visions/FAM-002_desktop_interface.md` for current UI vision and presentation law; and any later USER-approved FAM-002 Family Feature Vision or reference catalog for promoted template/reference truth.

Repair Finding: The timestamped upload ZIP `C:\Nexus USER\Governance-20260616-122646.zip` used a valid timestamped name but contained the older `USER Candidate Decision Packet Only` content from the visual-evidence repair. That packet was valid for candidate-decision digestion, but it was stale for the next missing-proof / promotion-planning approval surface after the accepted candidate decisions were recorded.

Required Corrected Packet: The local USER hub must be purged and rebuilt as a `Missing-Proof / Promotion-Planning Approval Packet`, not reused as a candidate-decision packet. It must include a decision summary, source-truth loaded list, missing-proof matrix, carrier recommendation, future owner/location/schema recommendation, blocker table, exact next USER decision text, packet digest, and timestamped ZIP proof reported outside USER-facing packet content.

Packet Boundary: This repair creates USER/ChatGPT review evidence only. It does not create a FAM-002 Family Feature Vision, create `Docs/ui_reference_catalog/`, promote a golden reference, create a template, implement design tokens, implement shared primitives, mutate helpers, mutate validators, mutate fixtures, mutate external state, mutate FAM worktrees, create issues, create a PR, merge, release, move/delete/archive source files, or clear `Current Branch Template Work Incomplete`.

Next Legal Use: USER/ChatGPT should review the corrected packet and decide whether to approve the next bounded template/reference carrier. The recommended next carrier remains staged: first a future FAM-002 Family Feature Vision such as `F2-FF01 Nexus UI Reference System` for durable UI reference-system vision and missing-proof planning, then an optional future `Docs/ui_reference_catalog/` only for USER-promoted reference contracts. PR Readiness remains blocked while `Current Branch Template Work Incomplete` is active unless USER explicitly reclassifies or removes the remaining work from current PR scope.

### PR #269 Release-Target Repair Closure - 2026-06-16

Repair Closure: `USER approved the bounded Governance intake repair for the PR #269 missing release-target contract. The binding repair lives in Docs/branch_records/feature_fam_007_three_ndai_assisted_ai_function_slice.md as the Merged PR #269 Release Target Contract. That receipt records Release Target v1.7.34-prebeta, Release Floor patch prerelease, Version Rationale, Release Scope, Release Artifacts, and Post-Release Truth. The evaluation rows above remain historical planning evidence; Release Target Undefined is no longer the current PR #269 source-truth-contract blocker after this repair. Release execution remains separately USER-gated.`

## Binding-Now / Future-Enforcement / Template-Blocked Classification - 2026-06-15

Document Status: Non-Binding Planning Classification. Binding authority remains with each owner named in the `Current Owner` column. This table prevents future Codex passes from treating future helper/validator guidance, template work, active FAM adoption, or FAM-007 lesson digestion as already complete.

Classification Values:

- `Binding Now`: the requirement is already durable source truth and must be manually enforced by Codex at the applicable phase even if helper coverage is future.
- `Binding At Next Legal Gate`: the requirement applies when an active/re-entering worktree reaches the phase or gate that source truth names.
- `Future Helper/Validator Enforcement`: the durable rule exists, but machine-checkable helper/validator enforcement remains a later USER decision unless already implemented.
- `Future Template/Golden Reference Work`: the durable rule points toward templates, references, design tokens, or shared primitives, but creation/promotion is not approved here.
- `Blocked By FAM-007 PR/Merge/Rebaseline/Lessons Dependency`: work waits until FAM-007 pushes/merges, worktrees rebaseline/reconcile, lessons are digested, and USER approves promotion.
- `Template / Reference Plan Completed - Current Branch Completion Hold`: FAM-007 prerequisite proof exists and the template/reference plan classifies candidates, future owners, schema, and promotion criteria, but PR Readiness remains blocked until planned current-branch template/reference work is admitted and completed or explicitly reclassified by USER.
- `PR-Hold Blocker`: the current integrated Governance PR path remains held until this item is completed or USER records an explicit limited PR path.
- `Not PR-Blocking`: the item is intentionally future-gated or applies to active FAM branches at their own next legal gate.
- `USER Decision Required`: no mutation may proceed until USER grants the named later authority.

| Requirement / Reform Item | Current Owner | Current Coverage | Binding Status | PR-Hold Status | Future Enforcement Type | Dependency / Blocker | Recommended Action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Scope Coverage Manifest Gate | `Docs/phase_governance.md`; `Docs/branch_plans/README.md`; `Docs/family_visions/FAM-002_desktop_interface.md` for UI anatomy; `Docs/validation_helper_registry.md` for helper guidance | Binding rule and required manifest fields exist; helpers are future guidance | Binding Now for broad/full-scope success claims; Binding At Next Legal Gate for active branches | Not PR-Blocking by itself after classification | Future Helper/Validator Enforcement | None beyond phase applicability | Enforce manually in Codex digests and packets until helper coverage is admitted |
| Broad/multi-issue defect decomposition | `Docs/phase_governance.md`; `Docs/incident_patterns.md`; `Docs/user_test_summary_guidance.md` | Binding broad-claim decomposition and incident pattern exist | Binding Now | Not PR-Blocking | Future Helper/Validator Enforcement | None | Require atomic target ledger or complete-class scan before any `all fixed` / `green` claim |
| Quantity-insensitive repair reliability | `Docs/phase_governance.md`; `Docs/incident_patterns.md` | Binding coverage disposition language exists | Binding Now | Not PR-Blocking | Future Helper/Validator Enforcement | None | Treat numbered or broad USER defects as coverage-expanding until every target has disposition |
| Element-group UI acceptance | `Docs/phase_governance.md`; `Docs/family_visions/FAM-002_desktop_interface.md`; `Docs/user_test_summary_guidance.md` | Binding element-group acceptance and visual adjudication language exists | Binding Now for UI/LV claims | Not PR-Blocking | Future Helper/Validator Enforcement; Future Template/Golden Reference Work for reference surfaces | Golden references not yet promoted | Enforce with focused screenshots/video or USER manual validation; do not wait for templates to enforce obvious UI failures |
| No-vague-final-acceptance | `Docs/phase_governance.md`; `Docs/user_test_summary_guidance.md`; `Docs/incident_patterns.md` | Binding anti-`looks good` / anti-`validator passed` language exists | Binding Now | Not PR-Blocking | Future Helper/Validator Enforcement | None | Require mapped evidence, accepted requirement, proof artifact, known limitation, and disposition |
| LV evidence table / element-group proof table | `Docs/phase_governance.md`; `Docs/user_test_summary_guidance.md`; active external branch plan or USER packet for active rows | Required by LV proof/manifest rules but active rows stay outside repo docs | Binding At Next Legal Gate | Not PR-Blocking | Future Helper/Validator Enforcement | Active branch proof rows belong outside repo docs | Require in LV/UTS handoff for active user-facing branches; do not add live rows to repo docs |
| Visual Inheritance Matrix | `Docs/phase_governance.md`; `Docs/family_feature_visions/README.md`; `Docs/family_visions/FAM-002_desktop_interface.md` | Binding matrix gate and UI inheritance fields exist | Binding At Next Legal Gate before Workstream for visible UI | Not PR-Blocking | Future Helper/Validator Enforcement; Future Template/Golden Reference Work for reference samples | Golden/reference samples improve proof later | Require branch packets to name inherited surface, FAM-002 grammar, exception, proof artifact, and verdict |
| Vision-To-Proof Matrix | `Docs/phase_governance.md`; `Docs/branch_plans/README.md`; `Docs/user_test_summary_guidance.md` | Binding matrix and proof-strength fields exist | Binding Now for material claims before LV green / UTS handoff | Not PR-Blocking | Future Helper/Validator Enforcement | None | Enforce manually in Hardening/LV/UTS packets until helper coverage expands |
| Claim Class / Proof Strength model | `Docs/phase_governance.md`; `Docs/user_test_summary_guidance.md`; `Docs/ai_runtime_and_trust_architecture.md` | Binding claim classes and evidence-independence rules exist | Binding Now | Not PR-Blocking | Future Helper/Validator Enforcement | None | Require claim class, minimum proof, evidence class, limitation, and USER validation route for material claims |
| Hardening / Live Validation repair loop | `Docs/phase_governance.md`; `Docs/branch_plans/README.md`; `Docs/user_test_summary_guidance.md` | Binding loop language exists; validators future | Binding Now when LV finds defects after Hardening | Not PR-Blocking | Future Helper/Validator Enforcement | None | Repair LV blockers first, rerun Hardening after branch changes, then reconfirm LV before PR Readiness |
| Top-level window geometry reset route | `Docs/phase_governance.md`; `Docs/branch_plans/README.md`; `Docs/family_visions/FAM-002_desktop_interface.md`; `Docs/family_visions/FAM-003_interaction_and_actions.md`; `Docs/family_feature_visions/F3-FF01.md`; `Docs/family_visions/FAM-008_packaging_and_install_experience.md` | Binding classification and dependency route exist; runtime reset action not implemented here | Binding At Next Legal Gate for branches touching eligible windows | Not PR-Blocking | Future Helper/Validator Enforcement; future product implementation by owning FAM | Runtime implementation remains separate; no repo live window-state tracking | Classify window/reset applicability in BP1/BP2/BP3; route FAM-003 dependency without mutating FAM-003 here |
| Top-level window-control grammar | `Docs/phase_governance.md`; `Docs/branch_plans/README.md`; `Docs/family_visions/FAM-002_desktop_interface.md` | Binding grammar and blocker names exist | Binding At Next Legal Gate for top-level Nexus windows | Not PR-Blocking | Future Helper/Validator Enforcement; Future Template/Golden Reference Work | Golden reference control cluster not yet promoted | Require compact NDAI control cluster or recorded exception before accepting a top-level product window |
| FAM-002 component anatomy | `Docs/family_visions/FAM-002_desktop_interface.md`; `Docs/phase_governance.md` | Binding component anatomy and element-group acceptance language exists | Binding Now as reusable presentation law | Current Branch Template Work Incomplete until promotion/reclassification is resolved | Future Template/Golden Reference Work; Future Helper/Validator Enforcement | FAM-007 prerequisite evidence exists; template/reference plan completed as evidence; actual promotion remains USER-gated | Use current grammar now; admit template/reference promotion next or explicitly reclassify |
| Backend Predictability / Reliability Contract | `Docs/phase_governance.md`; `Docs/branch_plans/README.md`; `Docs/development_rules.md`; `Docs/architecture.md`; AI-specific runtime boundaries in `Docs/ai_runtime_and_trust_architecture.md` | Binding backend/runtime contract language exists after the template/backend repair; future helpers remain guidance | Binding At Next Legal Gate for runtime/backend-affecting branches | Not PR-Blocking by itself after classification | Future Helper/Validator Enforcement | None beyond phase applicability | Require state owner, deterministic inputs/outputs, lifecycle/state machine, config/schema compatibility, failure/fallback/recovery, observability, rollback, and UI status/error mapping |
| Frontend / Backend Contract Consistency | `Docs/phase_governance.md`; `Docs/branch_plans/README.md`; `Docs/development_rules.md` | Binding UI-runtime truth mapping exists after the template/backend repair | Binding At Next Legal Gate for branches exposing runtime/backend state through UI | Not PR-Blocking by itself after classification | Future Helper/Validator Enforcement | None | Reject UI green/disabled/blocked/recovered states that do not map to runtime truth, policy truth, or USER-approved exception |
| FFV adoption checks for active branches | `Docs/phase_governance.md`; `Docs/family_visions/README.md`; `Docs/family_feature_visions/README.md`; `Docs/validation_helper_registry.md` | Binding FFV sufficiency and pointer rules exist; active branch adoption is future gate-specific | Binding At Next Legal Gate | Not PR-Blocking for Governance PR | Future Helper/Validator Enforcement | Active FAM worktree mutation excluded | FAM branches must run adoption review after rebaseline; Governance records rule only |
| FAM-006 adoption at next legal gate | `Docs/phase_governance.md`; active FAM-006 branch/worktree when resumed | Governance records next-gate adoption requirement; no FAM-006 mutation here | Binding At Next Legal Gate | Not PR-Blocking for Governance PR | Future Helper/Validator Enforcement | FAM-006 mutation excluded | FAM-006 must evaluate merged standards against its branch output at its next legal gate |
| FAM-007 adoption at next legal gate | `Docs/phase_governance.md`; active FAM-007 branch/worktree when resumed | Governance records next-gate adoption requirement; no FAM-007 mutation here | Binding At Next Legal Gate | Not PR-Blocking for Governance PR | Future Helper/Validator Enforcement | FAM-007 mutation excluded | FAM-007 must evaluate merged standards after rebaseline and before continuing branch gates |
| Rebaseline current-branch / previous-output implementation conformance scan | `Docs/phase_governance.md`; `Docs/branch_plans/README.md`; active external branch plan, USER packet, or Codex digest for active rows | Binding adoption review fields require current branch implementation inventory, implemented/touched UI-UX surfaces, implemented/touched runtime-backend surfaces, merged standard comparison, current violation findings, issue-candidate disposition, and no repo live-state tracking | Binding At Next Legal Gate | Not PR-Blocking for Governance PR | Future Helper/Validator Enforcement | Active FAM worktree mutation, live-state tracking, and GitHub issue mutation excluded | Rebaselining FAM branches must identify what they already implemented and whether current or previous output violates merged standards; out-of-scope defects become USER-reviewed issue candidates, not automatic fixes/issues |
| FAM-007 lessons digest | FAM-007 branch closeout / USER-reviewed evidence; Governance consumes only after merge/rebaseline | FAM-007 prerequisite evidence exists through merged PR #262, Governance PRs #263 through #268 lesson digestion, and merged PR #269 AI Control Center H4/template-first candidate evidence; no active FAM mutation here | Template / Reference Plan Completed - Current Branch Completion Hold | Current Branch Template Work Incomplete until promotion/reclassification is resolved | USER Decision Required for template/reference promotion | Actual template/reference promotion still requires USER approval | Do not infer active FAM packet state or golden-reference authority; use PR #269 evidence only as candidate template/reference input |
| Golden templates/reference surfaces | Future USER-approved FAM-002 / template-reference carrier; `Docs/family_visions/FAM-002_desktop_interface.md` owns presentation law | Ownership exists and the planning packet recommends future owner/location/schema; actual golden references are not promoted | Future Template/Golden Reference Work | Current Branch Template Work Incomplete until promotion/reclassification is resolved | USER Decision Required; future helper/validator evidence | Actual template/reference promotion remains unapproved | Admit the template/reference promotion cycle next or explicitly reclassify from current PR scope |
| Design tokens/shared primitives | Future UI implementation/template carrier; FAM-002 presentation law governs intent | Not admitted for implementation in this branch | Future Template/Golden Reference Work | Current branch must decide admission or explicit deferral before PR Readiness | USER Decision Required | Requires future implementation authority | Decide whether to admit implementation now or record explicit USER deferral/reclassification |
| Negative fixtures / bad example tests | `Docs/validation_helper_registry.md`; future helper/validator cycle | Guidance exists; fixture mutation excluded here | Future Helper/Validator Enforcement | Not PR-Blocking unless USER admits fixture implementation before PR | USER Decision Required | Fixture mutation excluded | Preserve as future enforcement; do not mutate fixtures in this classification cycle |
| Helper/validator future enforcement | `Docs/validation_helper_registry.md` | Multiple future guidance entries exist | Future Helper/Validator Enforcement | Not PR-Blocking unless USER admits code enforcement before PR | USER Decision Required | Helper/validator mutation excluded | Track as implementation backlog; current binding rules still apply manually |
| Codex User Guide compaction | `Docs/codex_user_guide.md`; `dev/orin_branch_governance_validation.py`; `dev/orin_governance_efficiency_validation.py` | USER-approved guide cleanup moved binding governance mirror expectations out of the operator guide and reduced the guide to prompt examples, workflow wording, and glossary support | Current repair completed; future helper coverage may improve guide-specific linting if drift returns | Not PR-blocking after current validation is green | No USER decision needed for current repair; future enforcement expansion remains USER-gated | Current validators now treat the guide as operator guidance, not a core governance mirror | Binding phase/source-truth/checklist language belongs in owner docs and prompt templates, while `Docs/codex_user_guide.md` stays subordinate to Main-routed source truth |
| Active ledger placement boundary | `Docs/governance_efficiency_operating_model.md`; `Docs/external_operational_state_store_reform_plan.md`; `Docs/phase_governance.md`; `Docs/worktree_slots.md` | Binding repo/external split exists | Binding Now | Not PR-Blocking | Future Helper/Validator Enforcement for new leakage classes | None | Keep active rows, branch proof, visual ledgers, and current adoption state outside repo docs |
| One integrated PR plan | This planning file plus `Docs/branch_records/feature_release_readiness_source_truth_intake.md` | USER preference recorded; template/reference prerequisite evidence exists and the plan is completed as planning evidence | Binding Now for current Governance branch posture | Current Branch Template Work Incomplete blocks PR Readiness | USER Decision Required for template/reference admission, later PR Readiness, PR creation, merge, release, and any reclassification | PR creation/merge/release remain separate USER decisions | Stop before PR Readiness and admit the remaining template/reference work on this current branch unless USER explicitly reclassifies it |

Closed PR-Hold Blockers:

- `FAM-007 Lessons Digest Missing For Template Promotion`: closed only as missing-prerequisite evidence by merged FAM-007 PR #262, Governance PRs #263 through #268 lesson digestion, and merged PR #269 AI Control Center candidate evidence; active FAM packets and chat remain non-authoritative.

Current PR-Hold Blocker List:

- `Golden Template / Reference Promotion Blocked`: actual template/reference/golden-reference/design-token/shared-primitive promotion remains future USER-approved work and must not be inferred from prerequisite evidence.
- `Current Branch Template Work Incomplete`: USER direction keeps the current Governance branch open until planned template/reference work is completed or explicitly reclassified.
- `Limited PR Path USER Approval Missing`: if USER later wants PR Readiness without completing the planned work, USER must explicitly approve that limited PR path or reclassify the blocker.

Not-PR-Blocking Future List:

- Future helper/validator enforcement for rules already binding in source truth.
- Future negative fixtures and bad-example tests unless USER separately admits fixture mutation before PR.
- Future GitHub issue creation, labeling, commenting, closing, reopening, or auto-close wording for any issue candidates; issue mutation remains USER-gated and is not a PR blocker by itself unless a current phase explicitly admits and blocks on it.
- Active FAM-006/FAM-007 adoption checks, which apply at each active worktree's next legal gate after rebaseline.
- Rebaseline current-branch implementation and UI/UX conformance scans, which apply inside the active branch plan, USER packet, phase digest, or external operational state of the affected worktree rather than this Governance plan file.
- Design-token and shared UI primitive implementation unless USER separately admits that implementation into this integrated PR.
- Active LV evidence rows, defect ledgers, proof manifests, and element-group proof tables, which belong in active external branch plans, USER packets, helper output, validator output, evidence roots, or Codex digests rather than repo docs.

FAM-007 Template Dependency Result:

FAM-007 prerequisite evidence is present for template/reference planning, including merged PR #269 AI Control Center H4/template-first evidence. The current Governance path now records `Template / Reference Plan Completed - Current Branch Completion Hold`. This posture does not make future helper/validator implementation, active FAM worktree mutation, design-token implementation, shared UI primitive implementation, or template/golden-reference promotion legal by itself.

One Integrated PR Plan Result:

The default path remains one integrated Governance PR after all admitted blockers are resolved. After the 2026-06-16 current-branch completion clarification, Codex must not recommend PR Readiness Stage 1 while `Current Branch Template Work Incomplete` remains active. Codex must not create a PR, merge, release, promote templates/references, mutate FAM worktrees, or create/mutate GitHub issues without the next exact USER approval.

## Purpose

This planning reference preserves candidate improvements for repo-wide governance, source truth, efficiency, reliability, error checking, drift prevention, and future Main / Dev / Owner repo separation.

This file is intentionally non-binding. It does not create new governance law, validators, helper requirements, source-truth owners, branch scope, external state records, repo split execution, private repos, file moves, or migration authority. Future implementation requires a separate USER-approved source-truth patch that names the owner files and exact write set.

## Source-Truth Boundary

Current repo truth already provides the first-order rules that control these recommendations:

- `Docs/Main.md` is the first loader and source-truth router.
- `Docs/phase_governance.md` owns phase law.
- `Docs/governance_efficiency_operating_model.md` owns the repo-docs-as-index/context model and external operational state contract.
- `Docs/feature_backlog.md` owns backlog identity and taxonomy.
- `Docs/ai_runtime_and_trust_architecture.md` already owns AI-native architecture and cross-family AI trust/cache/provider/capability direction.
- `Docs/validation_helper_registry.md` owns validator/helper interpretation and reuse.
- `Docs/external_operational_state_store_reform_plan.md` preserves the completed External Operational State Store transition and future cleanup boundaries.

Because source truth says to run `Source-Truth Placement Preflight` and extend existing owners first, this file treats every proposed new file or registry as a candidate only. A later implementation pass must prove `No Existing Owner Fits` before creating new durable owners.

## Current Branch Scope Correction - 2026-05-28

Scope Classification:

`RRI-20260528-001` contains the completed USER Review Gate semantics repair and the completed admitted Governance Reliability / Repo Split Reform source-truth contract cycles. Helper/validator code beyond already-committed review-gate false-green prevention, external-state mutation, repo split execution, FAM worktree mutation, main mutation, private repo creation, runtime work, release work, PR creation, and merge remain separate USER decisions.

PR Readiness Posture:

Historical 2026-05-28 posture: the admitted Governance Reliability / Repo Split Reform cycles and final integration hardening were ready for PR Readiness Stage 1 analysis after USER approval. Current 2026-06-15 posture supersedes that for the broader governance reliability / vision / proof reliability track: PR Readiness is held until all admitted remaining implementation/template/reference work is complete or USER records an explicit limited PR path.

Legal Path Options:

| Path | Meaning | Legal Next Phase | PR Readiness Status |
| --- | --- | --- | --- |
| Limited PR path | Superseded by USER approval to complete all admitted reform cycles in this branch | Not current | Not current |
| Full reform continuation path | Completed admitted docs/source-truth contract cycles before one consolidated PR | Held until remaining admitted implementation/template/reference blockers are resolved or USER selects a limited PR path | Held |

USER Preference Captured:

The USER approved all remaining phases/cycles in bounded mode on 2026-05-28, with USER gates and approvals waived/accepted for completing the admitted reform plan. That approval does not authorize PR creation, merge, release, runtime work, FAM worktree mutation, external-state mutation, repo split execution, private repo creation, file movement/deletion/archival, or helper/validator code mutation beyond the already-committed review-gate false-green prevention.

Current Commit Completion Matrix:

| Plan Section | Current Branch Status | Evidence / Notes |
| --- | --- | --- |
| Active Failure Class - USER Review Gate Bypass | Completed in current branch | Binding source truth, helper behavior, validator checks, fixtures, incident pattern, and USER review packet were updated. |
| Worktree-Delta Reconciliation Findings | Completed for this cycle | Read-only audit of Main, Governance, FAM-006, and FAM-007 was recorded; product worktrees were not mutated. |
| Governance Reliability / Repo Split Reform Planning File | Completed as planning evidence | This file exists as non-binding planning and candidate sequencing evidence. |
| Cycle 1 - Taxonomy / Owner Discipline | Completed for source-truth contract | `Docs/feature_backlog.md`, `Docs/governance_efficiency_operating_model.md`, `Docs/phase_governance.md`, and compact `Docs/Main.md` routing now preserve taxonomy, family rejection, `No Existing Owner Fits`, and owner-discipline rules. |
| Cycle 2 - Architecture / Experience / Policy Impact Matrix | Completed for source-truth contract | `Docs/phase_governance.md` and `Docs/branch_plans/README.md` require the matrix; existing owners remain `Docs/ai_runtime_and_trust_architecture.md`, product vision, and family visions. |
| Cycle 3 - Hypothesis-Driven Reliability | Completed for source-truth contract | `Docs/ai_runtime_and_trust_architecture.md` now records reliability classes and the Observation / Hypothesis / Validation loop. |
| Cycle 4 - PR / Review Drift Prevention | Completed for source-truth contract | USER Review Gate false-green prevention, PR body drift checks, review packet readability QA, and helper/validator evidence boundaries are recorded. |
| Cycle 5 - Main / Dev / Owner Boundary Planning | Completed for public-safe governance boundary | `Docs/governance_efficiency_operating_model.md` records the Main / Dev / Owner boundary contract; concrete private/runtime/FAM-007 work remains separate. |
| Governance Quickstart | Deferred / future candidate | Orientation-only artifact; not required before this reform can proceed unless USER admits it. |
| Optional explicit registries | Deferred / future candidate | May be created only after `No Existing Owner Fits` is proven. |
| Helper / validator implementation beyond current bypass checks | Deferred / separate USER decision | Current branch changed helper/validator only for the USER Review Gate false-green prevention; later code hardening must be separately admitted if needed. |
| Repo split execution, external-state migration, file movement, deletion, archival, private repo creation | Requires separate branch or later cycle | Not authorized and not performed. |
| Final integration hardening | Completed for current admitted source-truth contract | Owner conflicts, mirror drift, phase wording, taxonomy consistency, helper/validator guidance, PR/review drift, packet readability, private/public boundary leakage, and source-truth placement were checked before PR Readiness Stage 1 recommendation. |

Admitted Scope Rule:

Further mutation requires a new legal phase decision. Current USER direction holds PR Readiness for this broader reform until remaining admitted implementation/template/reference blockers are resolved or USER records an explicit limited PR path. PR creation, merge, release, helper/validator code expansion, external-state mutation, repo split execution, file movement/deletion/archival, private repo creation, runtime work, FAM worktree mutation, and main mutation remain separate USER decisions.

## Cycle 1 BR2 Admission - Taxonomy / Owner Discipline

Admission Date: 2026-05-28

Admission Status:

Cycle 1 is admitted as a bounded Governance Reliability / Repo Split Reform cycle for Taxonomy / Owner Discipline.

Current Gate:

Cycle 1 BP1, BP2, BP3, Workstream, Hardening, and LV1/non-applicability were completed under the USER's 2026-05-28 bounded all-phases/all-cycles approval. The earlier BP1 reviewable/pending packet is now superseded by this completion record.

Cycle 1 Packet State:

- Packet Reviewability State: `Superseded`.
- USER Gate State: `USER Waived`.
- BP2 Plan Review: `Completed under bounded all-cycles approval`.
- BP3 Workstream Entry / Orchestration Validation: `Completed under bounded all-cycles approval`.
- Workstream Implementation: `Completed for docs/source-truth contract only`.
- PR Readiness: `Held by current 2026-06-15 USER direction until remaining admitted implementation/template/reference blockers are resolved or USER records an explicit limited PR path`.

Cycle 1 Vision:

Cycle 1 should make taxonomy and owner routing harder to misread. It should prevent Codex from turning architecture layers, policy owners, experience layers, runtime subsystems, capability-pack domains, packages, slices, seams, mirrors, indexes, receipts, or external operational state into backlog families or source-truth owners by inertia.

Cycle 1 Owner Placement:

- `Docs/feature_backlog.md` remains the primary owner for backlog family identity, backlog admission, and the taxonomy gate.
- `Docs/governance_efficiency_operating_model.md` remains the primary owner for source-truth placement discipline, one-owner/mirror rules, compact pointer rules, and repo-docs-as-index/context boundaries.
- `Docs/phase_governance.md` remains the primary owner for phase-gate requirements and Branch Readiness / Branch Planning enforcement.
- `Docs/branch_plans/README.md` remains the primary owner for branch-planning packet structure and BP1/BP2/BP3 artifact expectations.
- `Docs/workstreams/index.md` remains the primary owner for package/slice/seam traceability and workstream-layer identity boundaries.
- `Docs/ai_runtime_and_trust_architecture.md` remains the primary owner for AI-native architecture, policy, reliability, provider, cache, capability-pack, and cross-family AI trust direction.
- `Docs/nexus_vision.md` and `Docs/family_visions/*` remain product-vision owners and should be extended only when Cycle 1 proves a taxonomy/owner-discipline change belongs there.

BP1 Review Questions:

- Does USER accept the Cycle 1 vision that taxonomy/owner discipline is the foundation cycle before architecture/experience/policy impact matrices, reliability classes, PR/review drift prevention, and Main / Dev / Owner boundary planning?
- Does USER agree that Cycle 1 should strengthen existing owners first rather than create new durable registries by default?
- Does USER want Cycle 1 to treat `No Existing Owner Fits` as the required proof before creating any new FAM, source-truth owner, architecture registry, experience registry, or policy registry?
- Does USER want any taxonomy class added, removed, renamed, or split before BP2 engineering/source-truth planning begins?

Forecast Only - Later Gates:

- Later plan gate: define exact owner-file edits, examples, blocker wording, validation expectations, and proof that no binding mutation has occurred by assumption.
- Later orchestration gate: prove the accepted plan is ready for bounded source-truth implementation, with helper/validator code mutation still separate unless explicitly approved.
- Later Workstream: implement only the approved taxonomy/owner-discipline source-truth edits.
- Later Hardening: scan touched owners, mirrors, indexes, packets, and validation guidance for taxonomy drift, owner duplication, and accidental live-state or ledger material.
- Later LV1: record USER-readable proof or `LV1 Applicability: Not Applicable with reason`.

Cycle 1 Stop Conditions:

- Stop if USER wants a new backlog family or durable source-truth owner before `No Existing Owner Fits` is proven.
- Stop if the taxonomy change would mutate FAM-006, FAM-007, main, runtime/provider/model behavior, external operational state, private repo boundaries, file movement, deletion, archival, helper code, or validator code without separate USER approval.
- Stop if packet reviewability is mistaken for BP1 acceptance.
- Stop if BP2, BP3, Workstream, PR Readiness, PR creation, merge, or release is requested before the prior gates close legally.

## Full Reform Completion Record - 2026-05-28

Completion Scope:

The admitted Governance Reliability / Repo Split Reform source-truth contract is complete for the current Governance branch. The completed scope is docs/source-truth governance contract work and USER packet refresh only.

Completed Cycles:

- Cycle 0 - USER Review Gate semantics repair.
- Cycle 1 - Taxonomy / Owner Discipline.
- Cycle 2 - Architecture / Experience / Policy Impact Matrix.
- Cycle 3 - Hypothesis-Driven Reliability.
- Cycle 4 - PR / Review Drift Prevention.
- Cycle 5 - Main / Dev / Owner Boundary Planning, public-safe boundary only.

Cycle Proof Summary:

- Taxonomy / Owner Discipline: backlog taxonomy, family rejection tests, `No Existing Owner Fits`, source-truth authority hierarchy, and mirror drift control are recorded in the existing owners.
- Architecture / Experience / Policy Impact Matrix: Branch Readiness and Branch Planning must classify architecture, experience, policy, runtime subsystem, capability-pack, family vision, package/slice/seam, or no-impact routing before implementation.
- Hypothesis-Driven Reliability: AI runtime/trust architecture records deterministic, high-confidence, advisory, exploratory/hypothesis, and creative reliability classes plus the Observation / Hypothesis / Validation loop.
- PR / Review Drift Prevention: PR body drift checks, USER review packet human-readability QA, packet reviewability versus USER acceptance, and validators-as-evidence boundaries are recorded.
- Main / Dev / Owner Boundary Planning: public-safe repo/source-truth boundary, promotion/disclosure gates, private-reference leak blockers, and FAM-007/private implementation deferral are recorded.

Final Integration Hardening:

- Owner conflicts: no new durable owner file was created; existing owners were extended first.
- Mirror drift: Main and review/packet surfaces remain compact pointers while owner files carry the durable rules.
- Phase wording conflicts: BP1/BP2/BP3 acceptance semantics remain unchanged; this record only notes the USER's all-cycle waiver for this bounded governance run.
- Taxonomy consistency: `FAM-009` remains reusable because workspace/data and safety/privacy fold-source files are not active families or number reservations.
- Validator/helper guidance consistency: helper/validator code expansion remains future/deferred unless separately approved; registry guidance names reuse-first targets.
- PR/review drift: PR body audit and review-packet readability rules are recorded without creating PRs.
- Private/public boundary leakage: Main / Dev / Owner split is public-safe planning only; private repo creation, private remotes, provider/model execution, memory/cache implementation, and private import are still blocked.
- Source-truth placement: no repo docs were moved, deleted, archived, or converted into new ledgers.

Next Legal Phase:

PR Readiness Stage 1 analysis, after USER approval. PR creation, merge, release, external-state mutation, repo split execution, file movement/deletion/archival, private repo creation, runtime work, FAM worktree mutation, main mutation, and helper/validator code expansion remain separate USER decisions.

## Active Failure Class - USER Review Gate Bypass / Packet Validation Treated As USER Acceptance

Failure Title:
USER Review Gate bypass caused by treating packet validation as gate acceptance.

FAM-006 Evidence Summary:

- FAM-006 BP1 packet generation produced stale wrong-family and wrong-phase USER review aid wording, including Governance, PR Readiness, FAM-007, AI Runtime, Stage 2, and Workstream Entry language inside generated review surfaces.
- After BP1 repair, BP2 packet validation reported the BP2 branch-plan review path while generated files still contained BP1-pending and BP2-placeholder state.
- After BP2 repair, BP3 was reported as prepared / implementation-ready while the uploaded packet still described BP2 USER Branch Plan Review as pending USER response.
- This proves a repeatable false-green class: helper/validator packet reviewability, file freshness, or Codex digest state can be misread as USER acceptance, waiver, BP3 approval, or implementation authority.

Affected Phases / Stages:
Branch Planning BP1, BP2, BP3, Workstream Entry / Orchestration Validation, and the first Workstream implementation approval handoff.

Root Cause Hypothesis:
Branch Planning had strong language requiring USER review, but it did not consistently model packet reviewability and USER gate closure as separate machine-readable axes. Helpers and digests could therefore say a packet was valid, reviewable, or implementation-ready without proving USER response receipt and Codex digestion for the active gate.

Governance Owner Files:

- `Docs/phase_governance.md`
- `Docs/branch_plans/README.md`
- `Docs/development_rules.md`
- `Docs/codex_modes.md`
- `Docs/nexus_startup_contract.md`
- `Docs/Main.md`
- `Docs/validation_helper_registry.md`
- `Docs/incident_patterns.md`
- `Docs/orin_task_template.md`

Helper / Validator Owner Files:

- `dev/orin_user_review_bundle.py`
- `dev/orin_branch_governance_validation.py`
- `dev/orin_branch_readiness_planning_fixture_validation.py`
- `dev/fixtures/branch_readiness_planning/valid_branch_planning_review_gate_state.md`
- `dev/fixtures/branch_readiness_planning/invalid_packet_validation_treated_as_user_acceptance.md`

Required Canonical State Model:
Branch Planning review gates must carry two independent axes:

- `Packet Reviewability State`: `Missing`, `Generated`, `Validation Failed`, `Reviewable`, `Stale`, or `Superseded`.
- `USER Gate State`: `Pending USER Review`, `USER Revision Requested`, `USER Accepted`, `USER Approved`, `USER Waived`, `USER Rejected`, `USER Blocked`, or `Superseded`.

Required transition semantics:

- BP1.1 prepares/repairs `USER_BRANCH_VISION_REVIEW.md`; BP1.2 is the USER Review Gate; BP1.3 records USER acceptance, waiver, revision, rejection, or blocker.
- BP2.1 prepares/repairs `USER_BRANCH_PLAN_REVIEW.md` only after BP1 is accepted or waived; BP2.2 is the USER Review Gate; BP2.3 records USER acceptance, waiver, revision, rejection, or blocker.
- BP3.1 prepares/repairs Workstream Entry / Orchestration Validation only after BP1 and BP2 are accepted or waived; BP3.2 is the USER orchestration review gate; BP3.3 records USER approval, waiver, revision, or blocker.
- Workstream implementation remains separately USER-gated after legal BP3 posture.

Required Blockers:

- `BP1 Review Packet Ready But USER Response Pending`
- `BP1 USER Acceptance Proof Missing`
- `BP2 Review Packet Ready But USER Response Pending`
- `BP2 USER Acceptance Proof Missing`
- `BP3 Review Packet Ready But USER Response Pending`
- `BP3 USER Approval Proof Missing`
- `Packet Validation Treated As USER Acceptance`
- `Review Gate Bypass`
- `USER Review Packet Phase-State Conflict`
- `USER Review Packet Not Digested`
- `Branch Planning Acceptance Receipt Missing`
- `Helper False Green On Review Gate State`
- `Codex Digest Conflicts With USER Packet`

Required Fixtures:

- valid BP1/BP2/BP3 gate packet where packet is reviewable but USER gate is pending and implementation remains blocked
- valid accepted/waived gate packet where USER response proof is digested
- invalid stale wrong-family / wrong-phase generated USER-facing review aid
- invalid BP1 template-shell review artifact that tells USER what sections should contain instead of applying branch-specific vision
- invalid BP1 copied-file-list-only `Surface Map`
- invalid BP1 generic USER questions that do not drive branch-specific decisions
- invalid shallow or generic Codex recommendations
- invalid BP1-pending packet used as BP2/BP3 proof
- invalid BP2-placeholder or BP2-pending packet misclassified as BP3
- invalid BP3 packet misclassified as implementation-ready before BP3 USER approval
- invalid Codex digest that conflicts with uploaded USER packet state

Substantive Artifact Standard:
BP1, BP2, and BP3 reviewability requires more than clean headings, stale-language hygiene, copied-file freshness, and ZIP consistency. BP1 must be an applied branch vision contract; BP2 must be an applied engineering plan contract derived from accepted or waived BP1; BP3 must be an applied orchestration-readiness contract against accepted or waived BP1/BP2. Copied source-truth files are context and navigation evidence only. Helper output, validators, and fixtures must reject template-shell prose, generic options, generic recommendations, broad questions, and copied-file manifests when they are used as substitutes for USER-facing vision, plan, or orchestration content. This standard applies globally to every branch and worktree packet, including FAM-006, FAM-007, Governance, and future families after they rebaseline to the merged governance.

Dogfood Fixture Expansion:
The repair should keep representative example coverage so future changes do not only pass abstract marker fixtures. FAM-006 is the UI/runtime/user-visible dogfood lane and should prove active-overlay recording readiness language, visual proof expectations, disabled/future-gated controls, runtime recording deferral, and USER design questions. FAM-007 is the private-boundary/decision-readiness dogfood lane and should prove public-safe Main/Dev/Owner boundary language, provider/runtime/cache/memory deferral, private repo/remote/backup/import gates, leak-prevention proof, and USER design questions. A governance-only source-truth dogfood scenario is also useful because the same BP1 standard applies to non-product branches that alter phase, helper, validator, or review-packet behavior.

Structured USER Hub Packet Layout:
The local USER hub packet should make the human decision surface unmistakable. The stable worktree folder remains `C:\Nexus USER\<label>`, but it should contain root `START_HERE.md`, a `USER Review` folder with exactly one primary current-gate decision file, a `Review Aids` folder for generated supporting digests/checklists, and a `Source Truth Context` folder for copied repo source-truth context. BP1 primary review is `USER_BRANCH_VISION_REVIEW.md`; BP2 primary review is `USER_BRANCH_PLAN_REVIEW.md`; BP3 primary review is the Workstream Entry / Orchestration review artifact. This reduces packet confusion without moving source truth or mutating FAM worktrees.

Required Validation Commands:

- `git diff --check`
- `git diff --check origin/main...HEAD`
- `python dev\orin_branch_governance_validation.py`
- `python dev\orin_branch_governance_validation.py --worktree-confinement-gate`
- `python dev\orin_branch_governance_validation.py --release-readiness-health-gate`
- `python dev\orin_branch_readiness_planning_fixture_validation.py`
- `python dev\orin_governance_efficiency_validation.py`
- `python dev\orin_source_owner_marker_validation.py`
- `python -m compileall -q dev desktop Audio main.py nexus_visual`

Worktree-Delta Reconciliation Findings:

| Worktree | Branch | HEAD vs `origin/main` orientation | Changed-file summary | Governance / helper overlap | Risk |
| --- | --- | --- | --- | --- | --- |
| `C:\Nexus Desktop AI` | `main` | `git rev-list --left-right --count HEAD...origin/main` = `0 12` (`HEAD` is 0 ahead, 12 behind) | no committed branch diff versus `origin/main`; untracked `Docs/Phase_Governance_Full_Digest.md` | none to mutate in this patch | neutral main is behind; read-only only |
| `C:\Nexus Worktrees\Governance` | `feature/release-readiness-source-truth-intake` | `0 0` versus `origin/main`; `1 0` versus upstream | legal write target; current untracked planning file | all current patch files belong here | low, bounded Governance patch |
| `C:\Nexus Worktrees\FAM-006` | `feature/fam-006-active-overlay-recording-runtime-implementation` | `39 0` versus `origin/main` | branch record/plan, family vision, backlog/roadmap, helper, validation registry, and planning fixtures | `Docs/validation_helper_registry.md`, `dev/orin_user_review_bundle.py`, `dev/orin_branch_readiness_planning_fixture_validation.py` | high reusable-governance overlap; do not mutate product branch |
| `C:\Nexus Worktrees\FAM-007` | `feature/fam-007-dev-owner-skeleton-readiness` | `4 0` versus `origin/main` | branch record/index, generated inventory review files, validation registry, docs audit helper, governance efficiency validator, user review bundle helper | `Docs/validation_helper_registry.md`, `dev/orin_user_review_bundle.py` | medium reusable-governance overlap; do not mutate product branch |

Product-Worktree Carry-Forward Notes:
FAM-006 and FAM-007 branch-local helper repairs show the same false-green family in narrower forms. Governance should generalize them here instead of copying FAM-specific packet-wording lists. Product branch files remain pending USER decisions and must be reconciled after this Governance patch lands.

USER Decision Boundaries:
This candidate does not authorize FAM-006 mutation, FAM-007 mutation, Workstream implementation, SLC implementation, PR creation, merge, release, issue mutation, branch cleanup, runtime/provider/model/shortcut/installer work, private import, or direct-main mutation.

Migration / Backfill Needs:
New or regenerated BP1/BP2/BP3 packets should include both state axes. Existing active product-branch packets may need reissue after rebaseline, but that belongs to the owning product branch after this Governance patch lands and USER approves continuation there.

Rollout Plan:

1. Patch binding source truth with the two-axis Branch Planning Review Gate State Model.
2. Patch helper/validator guidance and fixture checks so reusable false-green cases are machine-checkable.
3. Keep FAM-006/FAM-007 worktrees read-only during this Governance patch.
4. After merge, rebaseline product worktrees and let their owning branches regenerate BP packets under the new model.

Acceptance Criteria:

- Source truth says reviewability is not USER acceptance.
- BP1/BP2/BP3 gate transitions are explicit.
- The helper reports review-packet state separately from implementation approval state.
- Fixture validation rejects a reviewable packet used as implementation approval while USER response is pending.
- Generated USER-facing review aid drift is classified separately from copied source-truth context files.

## Executive Recommendation

The ChatGPT response is directionally correct: the next governance risk is not lack of rules, but owner duplication and architecture/experience drift as AI-native planning grows.

The strongest near-term reform is not to create many new registries immediately. The safer reform is:

1. Add a formal `Architecture / Experience / Policy Impact Matrix` to Branch Readiness / Branch Planning packets.
2. Strengthen the backlog taxonomy rejection tests so architecture layers, experience layers, runtime subsystems, policy owners, and capability domains cannot become FAMs by inertia.
3. Add a compact Source Truth Authority Hierarchy to existing governance owners.
4. Extend `Docs/ai_runtime_and_trust_architecture.md` before creating a separate architecture registry.
5. Add validator guidance to detect architecture/experience/policy owner drift using existing reusable validators first.
6. Add future Main / Dev / Owner repo boundary rules before any private repo split begins.

Cycle Strategy Clarification:

The recommended implementation posture is focused internal governance cycles, not one shallow pass and not one PR per cycle. Each admitted reform area should run through the normal phase path from Branch Readiness through Branch Planning, Workstream, Hardening, and LV1 when applicable. After one reform area completes LV1 or records a documented LV1 not-applicable reason, the work returns to Branch Readiness Stage 1 for the next admitted reform area. PR Readiness, PR creation, merge, and release remain later phases after all admitted cycles and final integration hardening are complete.

## ChatGPT Recommendation Review

| ChatGPT Recommendation | Evaluation | Adjusted Recommendation |
| --- | --- | --- |
| Add `Docs/architecture_layers.md`. | Good problem diagnosis, but premature as a new file unless `No Existing Owner Fits` is proven. | First add an `Architecture Layer Registry` section or appendix to `Docs/ai_runtime_and_trust_architecture.md`. Split to `Docs/architecture_layers.md` only if the owner grows too large or includes non-AI architecture that no existing file owns. |
| Add Branch Readiness Architecture Impact Matrix. | Strongly agree. This is the most practical drift-prevention improvement. | Add a matrix to Branch Readiness / Branch Planning so every branch declares whether it touches Permission-State, Trust Journal, Cache Governance, Deterministic Routing, Provider Orchestration, Competitive Integrity, Experience Layers, and Cross-Family Policies. |
| Add Architecture Drift Validator. | Agree, but use existing validator families first. | Extend `dev/orin_branch_governance_validation.py` and fixture validation before adding a new validator. New helper only after reuse order proves no existing helper fits. |
| Add Formal Experience Layer Registry. | Agree with the need; watch for owner sprawl. | Start with `Experience Layer` rules in `Docs/nexus_vision.md` or `Docs/ai_runtime_and_trust_architecture.md` depending on whether the concept is product-wide UX or AI-runtime behavior. Create `Docs/experience_layers.md` only after placement preflight. |
| Add "What Cannot Become A FAM" rule. | Strongly agree. This is directly aligned with current backlog repair. | Add explicit `Automatic Family Rejection Tests` to `Docs/feature_backlog.md`. |
| Add Governance Memory vs Source Truth Rule. | Agree; partially exists already. | Add a compact `Source Truth Authority Hierarchy` to `Docs/governance_efficiency_operating_model.md`, with a pointer in `Docs/Main.md` only if Main needs it. |
| Add Governance Quickstart. | Agree as onboarding, but it must be non-authoritative. | Create a future `Docs/governance_quickstart.md` as a 15-minute orientation that points to owners and never overrides them. |
| AI Runtime Trust Architecture should become canon. | Mostly already true. | Treat `Docs/ai_runtime_and_trust_architecture.md` as current first-class canon, then strengthen routing and impact checks around it. |
| Add Reliability Class ownership. | Strongly agree. | Add an `AI Reliability Class Model` to `Docs/ai_runtime_and_trust_architecture.md`, with deterministic / high-confidence / advisory / creative classes and proof implications. |
| Biggest risk is governance mirrors. | Strongly agree. | Add a `Governance Mirror Drift Control` rule: one owner, compact mirrors only, generated/index surfaces not hand-authored state. |

## Codex Self-Evaluation

My prior custom-instruction recommendation was useful as a compact app-level behavior shim, but it is not repo source truth and should stay subordinate to Main-first loading.

What it got right:

- Main-first source truth.
- Phase machine.
- Branch Planning before Workstream.
- External state split.
- Protected main.
- Validators as evidence.
- Release Readiness file-freeze.
- Digest non-compaction.

What it should not do:

- Become a parallel governance document.
- Replace `Docs/Main.md`.
- Encode detailed source-truth rules that may drift.
- Add project policy that is not already in repo canon.

Recommended custom-instruction improvement:

Keep app custom instructions compact and stable. They should say "load repo truth and obey it", not try to restate every phase rule.

## Governed Cycle Strategy For This Planning Reform

Cycle Definition:

One governance reliability reform cycle is:

```text
Branch Readiness Stage 1 -> BP1 / BP2 / BP3 -> Workstream -> Hardening -> LV1 if applicable -> return to Branch Readiness Stage 1 for the next admitted cycle
```

The cycle does not include PR Readiness, PR creation, merge, release execution, branch cleanup, FAM worktree mutation, helper implementation, validator implementation, external-state mutation, private repo creation, or repo split execution unless a later USER approval explicitly admits that work in the proper phase.

Cycle Semantics:

- Branch Readiness Stage 1 analyzes the focused reform area, confirms source-truth owner placement, identifies blockers, and asks USER questions.
- BP1 records or confirms the USER-facing vision/reform intent when product, AI behavior, repo split, review UX, or source-truth ownership direction could affect future implementation.
- BP2 records the engineering/source-truth plan for that reform area, including likely files, proof path, checks, stop conditions, and scope exclusions.
- BP3 proves the plan is ready to enter bounded implementation for that reform area.
- Workstream performs only the approved source-truth/planning updates for that area.
- Hardening checks the cycle's actual edits against accepted BP1/BP2 intent, source-truth owner boundaries, and drift risks.
- LV1 applies when USER-facing review, planning digest readability, branch-planning packet shape, PR body shape, or public/private boundary language needs USER-inspectable proof. If LV1 is not materially relevant, record `LV1 Applicability: Not Applicable with reason`.
- After LV1 or documented non-applicability, return to Branch Readiness Stage 1 for the next admitted reform area.

One Final PR Intent:

The preferred outcome is one consolidated PR after all admitted cycles finish and final integration hardening is green. A cycle may require a separate PR only when repo truth or merge-risk analysis shows that combining it would blur source-truth ownership, mix helper/validator code with docs-only contract work, execute private/repo-split work, mutate a FAM worktree, or create release/runtime risk.

### Proposed Cycle Order

| Cycle | Reform Area | Likely Owner Files | LV1 Proof / Waiver | Validation / Check Updates Needed | Drift Risks Introduced | Stop Conditions | Final Hardening Carry-Forward |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Taxonomy / Owner Discipline | `Docs/feature_backlog.md`, `Docs/governance_efficiency_operating_model.md`, compact pointer in `Docs/Main.md` only if needed | USER-readable taxonomy/owner decision proof; LV1 may be not applicable if no USER-facing packet shape changes | Future validator guidance for FAM rejection and owner placement checks | Over-rejecting legitimate future FAMs; duplicating taxonomy across mirrors | `No Existing Owner Fits` unproven; USER wants new FAM identity; owner conflict | Confirm every later cycle uses the same taxonomy vocabulary |
| 2 | Architecture / Experience / Policy Impact Matrix | `Docs/phase_governance.md`, `Docs/branch_plans/README.md`, `Docs/ai_runtime_and_trust_architecture.md`, `Docs/validation_helper_registry.md` | USER-inspectable matrix shape and example decision path | Marker-first validator/fixture guidance after source-truth contract lands | Matrix becomes another ledger; architecture/policy/experience owners conflict | Matrix tries to authorize runtime work; owner class unclear; new owner file requested without preflight | Check Branch Planning, taxonomy, and AI architecture agree |
| 3 | Hypothesis-Driven Reliability | `Docs/ai_runtime_and_trust_architecture.md`, `Docs/nexus_vision.md`, FAM-007 vision pointer if needed | USER-readable explanation that reliability improves accuracy without suppressing adaptive intelligence | Future AI/provider/cache validation guidance for reliability class and evidence labels | Deterministic class flattens ORIN; hypotheses presented as facts; creative/advisory answers over-claim certainty | Reliability class conflicts with AI architecture; FAM-007-specific runtime behavior appears | Check reliability language across architecture, vision, Branch Planning, and FAM-007 |
| 4 | PR / Review Drift Prevention | `Docs/phase_governance.md`, `Docs/workstreams/index.md`, `Docs/branch_plans/README.md`, `Docs/validation_helper_registry.md` | USER-readable PR/review packet shape; stale/readability proof where applicable | Future PR body drift and USER review readability checks | PR body becomes phase digest; USER packet becomes metadata dump; helper green accepted without review | PR body standard conflicts; review packet requires helper code not approved | Check PR Readiness, review hub, helper registry, and digest rules align |
| 5 | Main / Dev / Owner Boundary Planning | `Docs/governance_efficiency_operating_model.md`, `Docs/ai_runtime_and_trust_architecture.md`, `Docs/nexus_vision.md`, `Docs/family_visions/FAM-007_local_ai_and_capability_packs.md`, `Docs/family_visions/FAM-007_ai_edition_capability_trust_boundary_release_plan.md` | USER-readable public/private boundary and promotion-gate proof; no private repo execution | Future private/public leak scan and promotion packet guidance | Governance tries to own FAM-007 implementation; FAM-007 trust work becomes incidental to another branch; private details leak into Main | Requires private repo creation, provider/runtime work, memory/cache implementation, or FAM worktree mutation | Decide whether this stays public-safe governance boundary or moves to a dedicated FAM-007 carrier |

### Final Integration Hardening

After all admitted cycles complete, run one final integration hardening pass before PR Readiness. It must check:

- owner conflicts across every touched source-truth file
- mirror drift and duplicate rule text
- phase wording conflicts
- taxonomy consistency
- validator/helper guidance consistency
- PR/readiness drift
- USER review packet readability
- private/public boundary leakage
- source-truth placement conflicts across all cycles
- whether any cycle introduced a new durable owner without `No Existing Owner Fits`
- whether any FAM-007-specific Main / Dev / Owner implementation detail must be deferred to FAM-007 instead of staying in repo-wide governance

Final PR Decision Rule:

After final integration hardening, decide whether to land the admitted cycles as one consolidated PR, multiple PRs, or a split strategy. Default preference is one consolidated PR for docs-only governance/source-truth contract work. Separate PRs are required when the work mixes docs-only contract with helper/validator code, private repo setup, runtime implementation, external-state mutation, FAM worktree mutation, or high-risk owner-file rewrites.

## Reform Candidate 1 - Architecture Layer Ownership

Problem:

AI-native planning now names durable architecture systems: Permission-State System, Deterministic Routing, Provider Orchestration, Context Engine, Routine Engine, Trust Journal, Competitive Integrity, AI Operational Cache Governance, capability-pack architecture, and Windows Health recommendation boundaries.

Current Owner:

- `Docs/ai_runtime_and_trust_architecture.md`

Risk:

Branches may redefine these architecture layers differently, or treat them as backlog families, runtime implementations, or branch-local details.

Candidate Rule:

Architecture layers are cross-family structural systems. They are not FAMs by default, not runtime authorization by themselves, and not active branch plans. A branch that touches one must cite the owner, classify its impact, and state whether it is extending, consuming, or proposing a change to the architecture layer.

Recommended Owner:

- First pass: `Docs/ai_runtime_and_trust_architecture.md`
- Compact pointer if needed: `Docs/Main.md`
- Validator guidance: `Docs/validation_helper_registry.md`
- Branch packet integration: `Docs/branch_plans/README.md` and `Docs/phase_governance.md`

Implementation Shape:

Add a section such as:

```text
## Architecture Layer Registry

| Layer | Owner | Status | Affected Families | Policy Impact | Runtime Approval Required |
| --- | --- | --- | --- | --- | --- |
```

Do not create `Docs/architecture_layers.md` unless the existing AI runtime/trust owner is proven too broad or non-AI architecture layers require a separate owner.

## Reform Candidate 2 - Experience Layer Ownership

Problem:

Experience concepts such as Calm Technology, Daily Continuity, Ambient Assistance, Session Framing, Interruption Awareness, Assistance Intensity, and Trust-Visible UI may affect many families without being runtime subsystems or backlog families.

Risk:

Experience language may drift between family visions, branch plans, and UI implementation without a clear durable owner.

Candidate Rule:

Experience layers are reusable product interaction principles. They are not FAMs, not active branch plans, and not runtime implementation authority. They route through project vision or a named experience-layer owner before becoming branch acceptance criteria.

Recommended Owner Options:

- `Docs/nexus_vision.md` when the experience layer is project-wide product philosophy.
- `Docs/family_visions/FAM-XXX_*.md` when the experience layer is family-specific.
- `Docs/ai_runtime_and_trust_architecture.md` when the experience layer is AI/trust/provider/cache-specific.
- Future `Docs/experience_layers.md` only after `No Existing Owner Fits`.

Candidate Matrix:

```text
| Experience Layer | Product Meaning | Applies To | Default Owner | Branch Planning Question |
| --- | --- | --- | --- | --- |
```

## Reform Candidate 3 - Cross-Family Policy Owner Classification

Problem:

Some rules are policy, not architecture and not backlog identity: privacy lockdown, local-only mode, provider-cache sanitization, competitive integrity, cache clearability, public/private repo promotion, Owner-data privacy, and release/public-output safety.

Risk:

Policy rules can be scattered across family visions, branch plans, and helper outputs.

Candidate Rule:

Cross-family policy owners define constraints and enforcement expectations across families. A branch that touches a policy must cite the policy owner, state whether it is consuming or changing the policy, and identify the validator/helper impact.

Recommended Initial Owner:

- `Docs/ai_runtime_and_trust_architecture.md` for AI/trust policies.
- `Docs/governance_efficiency_operating_model.md` for source-truth/external-state policies.
- `Docs/phase_governance.md` for phase/proof policies.
- Future policy registry only if repeated policies do not fit existing owners.

## Reform Candidate 4 - Branch Readiness Architecture / Experience / Policy Impact Matrix

Problem:

Branch Readiness currently asks strong product/plan questions, but architecture/experience/policy impacts can still be implied instead of declared.

Candidate Rule:

Every Branch Readiness Stage 1 packet and BP1/BP2 Branch Planning packet for product/runtime/UI/provider/cache/AI work must include an Architecture / Experience / Policy Impact Matrix.

Candidate Fields:

```text
## Architecture / Experience / Policy Impact Matrix

| Owner Class | Named Owner | Touches? | Impact Type | Current Branch Scope | Deferred / Future Scope | Proof / Validation Needed |
| --- | --- | --- | --- | --- | --- | --- |
| Architecture Layer | Permission-State System | Yes / No | Consume / Extend / Change / New Candidate | ... | ... | ... |
| Architecture Layer | Deterministic Routing | Yes / No | Consume / Extend / Change / New Candidate | ... | ... | ... |
| Architecture Layer | Provider Orchestration | Yes / No | Consume / Extend / Change / New Candidate | ... | ... | ... |
| Architecture Layer | AI Operational Cache Governance | Yes / No | Consume / Extend / Change / New Candidate | ... | ... | ... |
| Policy Owner | Privacy Lockdown / Local-Only Mode | Yes / No | Consume / Extend / Change / New Candidate | ... | ... | ... |
| Experience Layer | Assistance Intensity / Interruption Awareness | Yes / No | Consume / Extend / Change / New Candidate | ... | ... | ... |
```

Allowed Impact Type:

- `No Impact`
- `Consume Existing`
- `Extend Existing`
- `Change Existing`
- `New Candidate`
- `USER Decision Required`

Blocking Condition:

- `Architecture Impact Unclassified`
- `Experience Layer Impact Unclassified`
- `Cross-Family Policy Impact Unclassified`
- `New Owner Candidate Without Placement Preflight`

Recommended Owner Files:

- `Docs/phase_governance.md` for required gate.
- `Docs/branch_plans/README.md` for packet structure.
- `Docs/feature_backlog.md` for taxonomy link.
- `Docs/validation_helper_registry.md` for validator guidance.

## Reform Candidate 5 - Automatic Family Rejection Tests

Problem:

The backlog should not absorb every important concept. FAMs are broad long-lived product families, not architecture layers, policies, runtime subsystems, capability domains, or branch work packets.

Candidate Rule:

Before Codex proposes or admits a new FAM, it must prove the concept is not better classified as:

- Family vision update.
- Architecture layer.
- Cross-family policy owner.
- Experience layer.
- Runtime subsystem.
- Capability-pack domain.
- Package.
- Slice.
- Seam.
- Workstream evidence.
- External operational state.
- Durable receipt.

If any of those owner classes fit, backlog admission is rejected unless USER explicitly approves new family identity.

Recommended Owner:

- `Docs/feature_backlog.md`

Candidate Blocker:

- `Backlog Family Rejection Test Missing`
- `Backlog Identity Created By Inertia`

## Reform Candidate 6 - Source Truth Authority Hierarchy

Problem:

The project repeatedly has to distinguish source truth from evidence, memory, chat, helper output, and review artifacts.

Candidate Hierarchy:

1. Repo durable source truth.
2. External operational state.
3. Git/GitHub/helper-derived live facts.
4. USER-reviewed local artifacts.
5. Validator/helper output.
6. Codex/ChatGPT response text.
7. Codex memory/chat history.

Important nuance:

Git/GitHub live facts outrank stale repo docs for volatile facts, but do not override durable product/governance law. Repo durable source truth owns governance rules; Git/GitHub owns live facts.

Recommended Owner:

- `Docs/governance_efficiency_operating_model.md`
- Compact pointer only in `Docs/Main.md` if needed.

Candidate Blocker:

- `Authority Hierarchy Ambiguous`
- `Evidence Treated As Source Truth`

## Reform Candidate 7 - Hypothesis-Driven Reliability And Reliability Class Model

Problem:

AI-native features need a consistent proof standard for objective, high-risk, advisory, exploratory, and creative output without making ORIN feel like a rigid calculator.

Product Goal:

ORIN should feel like an extension of human reasoning: curious, evidence-seeking, calm about uncertainty, and capable of forming and refining hypotheses. Deterministic routing should improve accuracy without suppressing adaptive intelligence, exploratory reasoning, or creative problem-solving.

Candidate Reliability Classes:

| Class | Meaning | Default Proof Requirement | Example |
| --- | --- | --- | --- |
| Deterministic | Exact answer/action required | Tool-backed or source-derived proof; no LLM-only truth | Health state, file path, release version |
| High Confidence | Strong evidence required, may include model reasoning | Source citations, validator/helper proof, confidence explanation | Policy routing, setup recommendation |
| Advisory | Guidance or recommendation | Explain basis, alternatives, uncertainty | Planning suggestions, workflow advice |
| Exploratory / Hypothesis | Possible explanations, diagnostic reasoning, missing-context discovery, or evidence-gathering plan | Label as hypothesis, separate observations from inference, ask clarifying questions or propose next evidence | Windows Health diagnosis, planning root-cause analysis, ambiguous UX issue |
| Creative | Open-ended generation | USER acceptance and safety boundaries | Copy, layout ideas, naming candidates |

Candidate Rule:

A branch that adds AI/provider/cache/capability-pack behavior must classify each user-facing AI output path by reliability class and define proof, fallback, cache behavior, Trust Journal requirements, and uncertainty communication requirements.

Observation / Hypothesis / Validation Loop:

1. Notice abnormality or user-stated goal.
2. Separate observed evidence, learned pattern, inferred explanation, uncertain hypothesis, and validated truth.
3. Ask who/what/where/when/why/how questions when missing context controls the answer.
4. Form one or more hypotheses when deterministic proof is unavailable.
5. Seek evidence before recommending action when the action has meaningful risk.
6. Communicate uncertainty calmly instead of using ego-like certainty.
7. Refine, reject, or validate hypotheses as evidence arrives.

Invalid Reliability Behaviors:

- treating experience or learned patterns as unquestionable reality
- presenting hypotheses as facts
- using deterministic class to suppress useful exploratory reasoning
- using creative/advisory language to bypass proof for objective facts
- recommending risky action before seeking available evidence

Suggested Durable Concept Names:

- `Hypothesis-Driven Reasoning Model`
- `Evidence-Seeking Reasoning`
- `Observation / Hypothesis / Validation Loop`
- `Truth Over Fluency, With Curiosity Preserved`
- `Human-Readable Reasoning Summary`
- `Confidence-Calibrated Inquiry`

Recommended Owner:

- `Docs/ai_runtime_and_trust_architecture.md`
- Family-specific implementation in FAM-007 or relevant family vision.

## Reform Candidate 8 - Governance Mirror Drift Control

Problem:

The digest identifies many governance mirrors. The risk is no longer missing policy; it is duplicated policy drifting across Main, phase governance, development rules, codex modes, loader contracts, helper registry, branch records, branch plans, and generated audits.

Candidate Rule:

Every durable governance rule has exactly one owner file. Mirrors must be compact pointers or execution reminders. If a mirror contains detailed rule text, it must name the owner and must not add new semantics.

Candidate Fields:

```text
Rule Owner:
Mirror Files:
Mirror Purpose:
Do Not Duplicate In:
Validator / Helper Owner:
```

Recommended Owner:

- `Docs/governance_efficiency_operating_model.md`

Potential Future Helper:

- Extend existing governance validation to detect conflicting rule definitions by owner phrase/Rule ID where machine-checkable.

## Reform Candidate 9 - Governance Quickstart

Problem:

The governance stack is too large for a new Codex session or contributor to internalize quickly.

Candidate Artifact:

- `Docs/governance_quickstart.md`

Status:

- Non-authoritative orientation only.

Recommended Contents:

- 15-minute governance tour.
- Source-truth load order.
- Phase lifecycle.
- Repo docs vs external state split.
- Backlog taxonomy.
- Branch Planning BP1/BP2/BP3.
- Validators as evidence.
- Common blockers.
- Where to inspect next.

Guardrail:

The quickstart must state that it is not execution authority and must route to Main and owner docs.

## Reform Candidate 10 - Review Packet Human-Readability QA

Problem:

USER-facing packets can drift into metadata dumps or validator output rather than readable decision packets.

Candidate Rule:

Every USER-facing review packet should pass a human-readability QA:

- Plain-language purpose.
- Exact decision requested.
- What USER will see or inspect.
- What will change.
- Options/tradeoffs.
- Open questions.
- Files to inspect.
- Not a validator log dump.
- Technical metadata moved to helper output, external state, or Codex digest.

Recommended Owner:

- `Docs/branch_plans/README.md`
- `Docs/governance_efficiency_operating_model.md`
- `dev/orin_user_review_bundle.py` guidance only after separately approved.

## Reform Candidate 11 - PR Body / PR Creation Drift Prevention

Problem:

USER observed PR body drift and had to manually delete bad PR content.

Candidate Rule:

PR Readiness Stage 1 should explicitly run a PR Body Drift Check before Stage 2 PR creation. The check compares proposed PR body sections against the repo PR output standard and rejects phase-digest fields, next legal phase language, release execution text, broad governance digests, or unapproved scope.

Candidate PR Body Sections:

- `## Summary`
- `## Branch Evidence`
- `## Validation`

Candidate Blocker:

- `PR Body Drift`
- `PR Body Contains Phase Handoff Fields`
- `PR Body Scope Overrun`

Recommended Owner:

- `Docs/phase_governance.md`
- `Docs/workstreams/index.md` where PR summary contract is already described.
- `Docs/validation_helper_registry.md` for helper/validator guidance.

## Reform Candidate 12 - Future Main / Dev / Owner Repo Split Boundary

Problem:

The future vision includes separate Main, Dev, and Owner repositories or repo-like trust zones. Without deterministic boundaries, private state, provider experiments, owner memory, and public source truth can leak across lanes.

Candidate Repository / Trust-Zone Model:

| Zone | Purpose | May Own | Must Not Own |
| --- | --- | --- | --- |
| Main / Public Current Repo | Public-safe app source, durable public governance, product vision, family visions, public architecture, release truth, public-safe validators | Buildable app, public docs, public-safe source truth, release notes, public validators | Secrets, private Owner memory, private credentials, private provider keys, private Dev experiments as authority |
| Dev / Private Development Repo | Private experiments, provider SDK spikes, internal diagnostics, private implementation prototypes, non-public proof | Experimental code, private test harnesses, Dev-only logs, candidate implementation before promotion | Public release truth, accepted governance law unless promoted to Main, Owner-private data |
| Owner / Private Local Repo Or Vault | USER-private preferences, memory, private profiles, local-only Owner data, secrets when later encrypted vault is approved | Owner data, private memory, local vault config, personal context, encrypted secrets | Public app source truth, public governance law, release artifacts, unredacted import into Main |

Candidate Import / Promotion Gates:

- `Main-to-Dev Import Packet`: imports public Main source into Dev for private experimentation.
- `Dev-to-Main Promotion Packet`: promotes sanitized Dev work to Main with public-safety review, license/security review, source-truth placement, validator expectations, and no private data.
- `Owner-to-Main Disclosure Gate`: blocks Owner data from entering Main unless USER explicitly approves a sanitized durable summary.
- `Owner-to-Dev Access Gate`: controls whether Dev tools may read Owner-private state.

Candidate Blockers:

- `Private Data Boundary Missing`
- `Dev-To-Main Promotion Packet Missing`
- `Owner Disclosure Approval Missing`
- `Private Path Leak`
- `Secret / Credential Leak`
- `Shadow Governance In Private Repo`

Recommended Owners:

- `Docs/governance_efficiency_operating_model.md` for repo/source-truth boundary.
- `Docs/ai_runtime_and_trust_architecture.md` for provider/cache/memory/trust implications.
- `Docs/nexus_vision.md` for project-wide privacy/local-first principle.
- `Docs/validation_helper_registry.md` for future scanner/helper guidance.

Cycle 5 Routing Clarification:

This governance reliability reform may define the public-safe Main / Dev / Owner boundary contract, source-truth ownership split, promotion packet concepts, private/public leak-prevention expectations, and ChatGPT/new-chat prompt boundary. It must not implement the split.

FAM-007 should carry later AI/provider/Dev/Owner trust implementation planning when the work becomes concrete FAM-007 behavior, including provider runtime, model behavior, capability-pack behavior, memory/cache implementation, Dev/Owner private roots, private repo creation, private remotes, or private-to-public sanitization workflows.

Governance may plan now:

- Main/Public repo durable source-truth boundary
- Dev/Owner private boundary as public-safe policy
- promotion and disclosure packet concepts
- private reference/path leak-prevention expectations
- ChatGPT/new-chat prompt rule that split state is source-truth-governed, not memory-governed
- cross-repo external state partitioning concept

FAM-007 or a later dedicated split carrier should own later:

- concrete Dev/Owner repo setup
- private provider/runtime behavior
- memory/cache implementation
- Owner/Dev private prompts, roots, remotes, or hosting
- Public-to-Dev import execution
- Dev-to-Main implementation promotion
- Owner disclosure execution

Separate PR Required When:

- Cycle 5 expands beyond public-safe governance/source-truth boundary
- FAM-007 family vision needs a substantive rewrite rather than a compact pointer
- private repo setup, remotes, roots, secrets, memory, provider/model execution, cache runtime, or FAM worktree mutation enters scope
- helper/validator implementation for private/public leak scanning is included

## Reform Candidate 13 - Cross-Repo External State Partitioning

Problem:

If Main, Dev, and Owner split later, `C:\Nexus Governance State` must coordinate operational state without making private state public or letting one repo's state become another repo's authority.

Candidate Layout Extension:

```text
C:\Nexus Governance State\
  repos\
    main\
    dev\
    owner\
  cross_repo_promotions\
  private_disclosure_packets\
  repo_acknowledgements\
```

Candidate Lock Scope Additions:

- Repo lock.
- Cross-repo promotion lock.
- Private disclosure lock.
- Owner-vault access lock.

Candidate Rule:

External operational state may coordinate Main/Dev/Owner workflow, but accepted public governance still returns to Main by USER-approved repo update and merge. Private Dev or Owner state cannot become public source truth by reference.

## Reform Candidate 14 - Private Reference And Path Leak Scanner

Problem:

Future Dev/Owner split increases risk that private paths, branch names, local-only memory, provider keys, model paths, or owner-specific details leak into Main docs, PRs, releases, or USER review bundles.

Candidate Scanner Behavior:

- Scan Main repo docs and PR bodies for private-root path patterns.
- Detect Owner/Dev private references outside approved public-safe summaries.
- Detect provider key/token/cookie patterns.
- Detect local-only model/cache/memory paths.
- Detect private repo branch names in public release notes.

Recommended Helper Strategy:

- Extend existing public-leak / source-owner / governance validators first.
- Add a dedicated scanner only if reuse is not sufficient.

Candidate Blocker:

- `Private Reference Leak`
- `Owner Data Leak`
- `Dev Private Evidence Leak`

## Reform Candidate 15 - Governance Candidate Promotion Queue Hardening

Problem:

External state can hold lessons and governance candidates, but if candidates are not promoted or rejected, important lessons may be lost.

Candidate Rule:

Every cross-worktree lesson, governance candidate, validator candidate, or source-truth placement candidate must have:

- Owner.
- Status.
- Target owner file.
- Promotion path.
- USER decision state.
- Final disposition.
- Expiration or review trigger.

Recommended Owner:

- `Docs/governance_efficiency_operating_model.md`
- `Docs/external_operational_state_store_reform_plan.md`
- External state schemas after a later approved external-state schema pass.

## Reform Candidate 16 - Error Checking Improvements

Recommended future machine-checkable gates:

- Architecture / Experience / Policy Impact Matrix present when product/runtime/UI/provider/cache/AI scope exists.
- FAM rejection tests completed before any new FAM/package identity proposal.
- Source Truth Authority Hierarchy cited when evidence conflicts.
- PR body drift check before Stage 2 PR creation.
- USER review packet human-readability QA.
- Private Dev/Owner leak scan for Main-facing PR/release/review outputs.
- Governance mirror drift scan for owner/mirror contradictions.
- Reliability class declaration for AI user-facing outputs.
- Dev-to-Main promotion packet check before importing private Dev work.
- Owner disclosure gate before any Owner-private data becomes public durable source truth.

## Reform Candidate 17 - Efficiency Improvements

Recommended future efficiency moves:

- Keep Main compact and router-only.
- Avoid creating one file per concept unless placement preflight proves no existing owner fits.
- Prefer sections in existing owner files for architecture, experience, policy, and reliability until they outgrow the owner.
- Use generated reports for inventory/drift views; do not hand-maintain global indexes.
- Keep active operational state external.
- Keep USER review packets concise and decision-focused.
- Use one consolidated governance reliability PR for related owner-model improvements instead of many tiny PRs, but only after exact owner files and validators are named.

## Reform Candidate 18 - Reliability Improvements

Recommended future reliability moves:

- Add `Reliability Class` to AI/provider/capability Branch Planning packets.
- Require deterministic outputs to cite tool/source proof.
- Require high-confidence outputs to include evidence and confidence basis.
- Require advisory outputs to show alternatives/tradeoffs.
- Require creative outputs to remain USER-accepted before implementation.
- Tie reliability class to cache behavior, Trust Journal recording, provider routing, and fallback.

## Reform Candidate 19 - Drift Prevention Improvements

Recommended future drift controls:

- One owner per durable rule.
- Compact mirrors only.
- New files only after `No Existing Owner Fits`.
- PR body drift check.
- Architecture/experience/policy matrix.
- Private split boundary scan.
- Source-truth authority hierarchy.
- External-state candidate promotion queue.
- Branch Planning packet stale guard remains mandatory.
- Validators remain evidence, not authority.

## Proposed Implementation Staging

This planning file recommends cycle-based implementation, not one shallow source-truth pass and not one PR per reform area.

### Stage A - Planning File Review

Current file only. USER reviews this recommendation set and decides whether to admit the cycles.

No binding source-truth law changes.
No validators.
No helpers.
No PR requirement unless USER wants to preserve this planning artifact.

### Stage B - Admitted Governance Reliability Cycles

Run each admitted reform cycle through the phase-consistent path:

```text
BR1 -> BP1/BP2/BP3 -> Workstream -> Hardening -> LV1 if applicable -> return to BR1
```

Cycle admission should name:

- reform area
- source-truth owner files
- expected write set
- proof needed before leaving the cycle
- LV1 applicability
- validation/check guidance changes
- drift risks
- stop conditions
- carry-forward items for final integration hardening

### Stage C - Final Integration Hardening

After all admitted cycles complete, run a final hardening pass across the combined reform surface. This pass decides whether the cycles are coherent enough for PR Readiness or whether a repair cycle is required.

### Stage D - PR Strategy Decision

After final integration hardening, choose:

- one consolidated PR for docs-only governance/source-truth contract work
- separate PRs when code/helper/validator/private/repo-split/FAM-specific work enters scope
- a split strategy when merge risk or owner conflict makes one PR unsafe

### Stage E - Later Helper / Validator / Repo Split Work

Helper code, validator code, private/public leak scanners, architecture drift scanners, repo split execution, private repo creation, external-state mutation, FAM worktree mutation, and runtime/provider/model/memory/cache behavior remain separate USER decisions after the docs/source-truth contract work.

## Template / Golden Reference Source-Truth Carrier Implementation - 2026-06-16

Document Status: Non-Binding Planning / Source-Truth Carrier Receipt. Binding authority remains with `Docs/family_visions/FAM-002_desktop_interface.md` for current presentation grammar, `Docs/family_feature_visions/F2-FF01.md` for the UI reference-system feature-category vision and missing-proof rows, `Docs/ui_reference_catalog/` for promoted reference records only after USER-approved promotion, and `Docs/phase_governance.md` for the dependency gate that prevents template/reference claims by inference.

Accepted Packet Evidence: USER accepted `C:\Nexus USER\Governance-20260616-123541.zip` as the Missing-Proof / Promotion-Planning Approval Packet with SHA256 `191D69C96E1457532F94FCD56A96F403EE7B31DB1347824CF4D3DAF3216543E1` and 12 files. That packet approved the source-truth carrier implementation-planning cycle before PR Readiness, not actual template creation, golden-reference promotion, design-token/shared-primitive implementation, helper/validator/fixture mutation, FAM worktree mutation, external-state mutation, PR creation, merge, release, or USER visual acceptance.

Carrier Result:

- Created `Docs/family_feature_visions/F2-FF01.md` as `F2-FF01 Nexus UI Reference System`.
- Added `F2-FF01` to `Docs/family_feature_visions/index.md`.
- Created `Docs/ui_reference_catalog/README.md` and `Docs/ui_reference_catalog/index.md` as an empty promoted-reference schema/index with zero promoted references.
- Routed the new catalog through `Docs/Main.md`, `Docs/governance_efficiency_operating_model.md`, and FAM-002 canonical pointers.
- Regenerated `Docs/governance_docs_full_inventory_reform_audit.md` and `Docs/governance_docs_reform_user_review_index.md` so generated Docs inventory counts include the new carrier files.
- Preserved the repo/external-state split: repo docs own durable rules, schemas, pointers, vision, missing-proof facts, and historical receipts; live proof inventories, active adoption state, candidate evidence, helper output, and current operational facts remain outside repo source truth until promoted by USER-approved packet.

Carrier Decision Table:

| Item | Carrier Result | Promotion Status | Blocking / Deferred State |
| --- | --- | --- | --- |
| FAM-002 UI Reference System FFV | `Docs/family_feature_visions/F2-FF01.md` created | Durable feature-category vision only | Does not promote any UI reference |
| UI Reference Catalog | `Docs/ui_reference_catalog/` schema/index created | Empty catalog, `Promoted Reference Count: 0` | No golden reference exists until promotion packet |
| HUD/FAM-006 evidence | Preserved as candidate evidence in planning | Not promoted | Requires USER visual proof and promotion record |
| PR #269 AI Control Center evidence | Preserved as candidate evidence in planning | Not promoted | Requires USER visual proof and promotion record |
| Golden window/control-cluster candidates | Missing-proof rows recorded in F2-FF01 | Not promoted | `Golden Reference Promotion Blocked` |
| Button/dropdown/dialog/status/tray references | Deferred carryforward recorded in F2-FF01 | Not promoted | Future proof/promotion or implementation approval required |
| Design tokens/shared primitives | Future-gated in F2-FF01 | Not implemented | `Shared Primitive Promotion Blocked` |
| Helper/validator/fixture enforcement | Future-gated in F2-FF01 | Not mutated | Future enforcement approval required |

Missing-Proof Rows Preserved:

- Golden window template: full-window visual proof across eligible top-level windows, geometry/resize proof, default/hover/focus/disabled control states, platform-exception classification, and USER visual acceptance.
- Golden control-cluster reference: close/minimize/maximize/restore applicability matrix, blocked-control behavior, hitbox/accessibility proof, hover/focus/pressed states, and top-level versus child-window distinction.
- HUD/FAM-006 surface reference: USER-accepted HUD/recording/log visual evidence, state proof, and consuming-FAM ownership confirmation.
- PR #269 AI Control Center surface reference: Project UI Vision/FAM-002 grammar comparison without treating FAM-007 private/provider/runtime deferrals as implemented AI.
- Reference surface library schema: zero promoted references until promotion proof is recorded.

Active Blockers Preserved:

- `Current Branch Template Work Incomplete` remains active until the USER either completes admitted reference-promotion/proof work or explicitly reclassifies remaining work out of the current PR scope.
- `Golden Reference Promotion Blocked` remains active for every candidate without USER-approved promotion proof.
- `Template Treated As Existing Proof` remains the blocker if any branch treats FAM-002 grammar, candidate evidence, helper output, screenshots, or Live Validation proof as an existing promoted golden reference.
- `Shared Primitive Promotion Blocked` remains active for design-token/shared-primitive implementation.
- Future helper/validator enforcement remains deferred until USER approves code/fixture mutation.

Next Legal Use:

The next legal phase is not PR Readiness unless USER explicitly reclassifies all remaining template/reference work out of current PR scope. The normal next step is a bounded Template / Golden Reference visual proof collection and promotion-review packet for named candidate references, or a narrower USER decision to promote a specific reference after evidence is loaded, compared, and accepted.

## Recommended Next USER Decision

The admitted Governance Reliability / Repo Split Reform source-truth contract cycles and final integration hardening are complete, but USER later clarified that the planned Template / Reference work must be completed on the current Governance branch before PR Readiness. The Template / Golden Reference admission, USER candidate packet repair, USER decision digestion, and source-truth carrier implementation-planning cycle are now recorded. `F2-FF01 Nexus UI Reference System` and the empty `Docs/ui_reference_catalog/` schema/index exist, but no golden references, templates, design tokens, shared primitives, helper/validator checks, fixtures, or active FAM adoption work have been promoted. The next legal USER decision is a bounded visual proof collection and promotion-review packet, or an explicit reclassification of remaining template/reference work out of current PR scope.

Suggested exact decision shape:

```text
I approve a bounded Template / Golden Reference visual proof collection and promotion-review packet on C:\Nexus Worktrees\Governance / feature/release-readiness-source-truth-intake before PR Readiness.

Current approval covers loading the F2-FF01 and UI Reference Catalog carrier, collecting or copying existing candidate visual evidence from approved/read-only sources, comparing HUD/FAM-006 and PR #269 AI Control Center evidence against Project UI Vision, FAM-002 grammar, and F2-FF01 missing-proof rows, producing a USER-reviewable promotion packet with named promote/revise/defer/reject options, preserving deferred candidates and blockers, enforcing clean USER packet regeneration and timestamped upload ZIP rules, running validation, committing and pushing docs/review-packet updates if green, and returning the exact approval text for any later specific reference promotion. This does not approve PR Readiness, PR creation, merge, release, external-state mutation, repo split execution, file movement/deletion/archival, private repo creation, FAM-006/FAM-007/main mutation, runtime/provider/model/shortcut/installer work, issue mutation, cleanup, Private Dev ORIN import, AI Product Contract import, helper/validator code mutation, fixture mutation, design-token/shared-primitive implementation, shared UI primitive implementation, actual template creation, actual golden-reference promotion, or USER visual acceptance unless the returned packet is separately approved.
```

Other legal USER responses:

- Request more hardening detail before template/reference admission.
- Explicitly reclassify one or more planned template/reference items out of current PR scope with reason.
- Approve a limited PR path despite incomplete template/reference work. This is not the current default.

## Template / Golden Reference Consolidated Package A-E Proof Collection Execution - 2026-06-17

Document Status: Non-Binding Planning / Source-Truth Receipt. Binding authority remains with `Docs/family_visions/FAM-002_desktop_interface.md` for reusable presentation grammar, `Docs/family_feature_visions/F2-FF01.md` for the UI reference-system feature-category vision and missing-proof rows, `Docs/ui_reference_catalog/` for USER-promoted reference records only after explicit promotion approval, and `Docs/phase_governance.md` / `Docs/branch_plans/README.md` for proof and phase-gate boundaries.

Accepted Evidence Posture:

- USER accepted the consolidated Package A-E proof-intake / promotion-route packet as reviewable evidence only.
- USER visual/product review result is `REVISE`.
- FAM-007 AI Control Center is the strongest top-level window and compact window-control seed currently available, but it is not promoted.
- HUD/FAM-006 remains useful comparison evidence and likely future consuming/adoption-target evidence, but it is not promoted.
- No Package A-E candidate has USER visual acceptance, USER waiver, promotion packet final disposition, or catalog record authority.
- `Docs/ui_reference_catalog/index.md` remains `Promoted Reference Count: 0`.

Execution Result:

Governance executed the bounded no-promotion proof collection corridor by collecting existing proof from approved USER packet/evidence folders, preserving FAM-003/FAM-006/FAM-007 as read-only consumer/context proof sources, copying/inventorying selected FAM-006 and FAM-007 proof artifacts into a regenerated `C:\Nexus USER\Governance` packet, and generating one consolidated proof review surface with proof, promotion-readiness, and blocker tables. This execution did not run runtime proof generation, mutate product worktrees, mutate external state, create a promoted catalog record, promote a reference, create a template, implement shared primitives/design tokens, mutate helpers/validators/fixtures, create issues, create a PR, merge, release, or record USER visual acceptance.

Proof Collection Table:

| Package | Candidate | Required State / Proof | Evidence Collected | Source | Independent? | Sufficient? | Visual/Product Notes | Remaining Gap | Next Legal Route |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | AI Control Center top-level window | Default focused top-level window, geometry/resize, window class matrix, platform exceptions, USER visual acceptance | Focused default screenshot, close-hover screenshot, corner/right/bottom resize screenshots, full-desktop screenshots, ordered frame sequence, live resize manifest | FAM-007 USER packet evidence | Partially yes | No | Strongest current top-level window seed; visually cohesive and closest to desired Nexus window grammar | Full state matrix, minimize-hover independence, maximize/restore applicability, platform exception classification, accessibility/hitbox proof, multi-surface comparison, USER acceptance | Continue proof collection or request USER evidence for a later Package A promotion packet |
| A | Compact window-control cluster | Close/minimize/maximize/restore applicability, blocked/disabled/focus/pressed/hover states, child/top-level distinction | Default screenshot, duplicate minimize-hover screenshot, independent close-hover screenshot, resize evidence | FAM-007 USER packet evidence | Mixed | No | Close-hover is useful; claimed minimize-hover remains duplicate by SHA256, so hover independence is not proven | Independent minimize-hover, maximize/restore/blocked-control proof, hitbox/accessibility proof, USER acceptance | Later focused control-cluster proof collection or USER-provided evidence |
| A | HUD/FAM-006 dashboard/window comparison | Cross-surface comparison against accepted reference candidate and FAM-006 ownership confirmation | HUD/dashboard screenshots and short video evidence copied from approved proof roots | FAM-006 USER/evidence folders | Yes as comparison | No | Useful contrast; likely future consumer/adoption target if AI Control Center grammar is later promoted | UTS acceptance remains pending/withheld; not complete top-level/window-control proof | Later FAM-006 adoption/evaluation after a reference is promoted or USER provides visual acceptance/waiver |
| B | Buttons, dropdowns, menus, lists, filters | Full control taxonomy and state coverage | FAM-006 quick-access controls, FAM-006 selector closed state, FAM-007 Run Local Check hover/no-tooltip, FAM-007 scrollbar context | FAM-006/FAM-007 evidence folders | Yes for individual examples | No | Useful comparison only; FAM-007 button evidence is promising but narrow | Dropdown open, menu, list rows, filters, keyboard/accessibility, disabled/loading/error, USER acceptance | Continue proof collection or route to later owning-FAM/runtime proof |
| C | Modal/dialog, status/failure/recovery, tray/settings doorway | Modal/dialog taxonomy, status/failure/recovery path, tray/menu doorway proof, settings proof | FAM-006 Log Viewer/Recording Studio screenshots, returned UTS failure review, F3-FF01 resident-access context | FAM-006 packet and Governance source-truth context | Partial | No | Existing evidence is context, not a reusable modal/status/tray reference | Runtime-truth mapping, tray/menu visuals, focus/keyboard/accessibility, failure/recovery sequence, USER acceptance | Later FAM-001/FAM-003/FAM-006/FAM runtime proof or USER evidence |
| D | Design tokens/shared UI rules | Token taxonomy, values/ranges, code-to-visual trace, reusable primitive boundary, adoption proof | FAM-002 grammar plus candidate visual evidence | Source truth and copied screenshots | Partial | No | Planning input only; no design-token implementation is approved | Accepted token values, code trace, contrast proof, migration/rollback, USER acceptance | Future implementation-planning carrier after reference candidates stabilize |
| E | Negative examples/helper/validator expectations | Executable negative/positive fixtures, helper/validator code changes, false-green regression proof | Planning receipts and no-overclaim rules | Governance source-truth context | Yes as planning evidence | No | Useful enforcement design, but no code/fixture mutation is approved | Helper/validator/fixture approval, red/green fixtures, false-positive review | Future enforcement carrier after USER approval |

Promotion-Readiness Table:

| Package | Candidate | Promotion Readiness | Reason | Can Move To USER Promotion Review? | Later Approval Needed |
| --- | --- | --- | --- | --- | --- |
| A | AI Control Center top-level window | Strongest seed, proof-blocked | Best current visual candidate but lacks full state/exception/accessibility/USER acceptance proof | Not yet as a promotion packet; yes as a proof-target packet | USER evidence or owning-FAM/runtime proof plus USER visual acceptance |
| A | Compact window-control cluster | Strong seed, proof-blocked | Close-hover proof exists; minimize-hover is duplicate and control applicability matrix is incomplete | Not yet | Independent control-state proof and USER visual acceptance |
| A | HUD/FAM-006 comparison/adoption target | Comparison only | Useful contrast and likely future consumer, but not accepted as standard | No | Later FAM-006 adoption/evaluation after reference promotion |
| B | Buttons/dropdowns/menus/lists/filters | Insufficient | Individual examples exist but no taxonomy/state matrix | No | More proof or later FAM/runtime evidence |
| C | Modal/dialog/status/failure/tray/settings | Insufficient | Mostly context/planning evidence; runtime/user-path proof missing | No | Later FAM-001/FAM-003/FAM-006 proof or USER evidence |
| D | Tokens/shared rules | Not ready | Needs implementation-planning carrier and accepted values | No | Separate implementation approval |
| E | Negative fixtures/helper/validator checks | Not ready | Needs code/fixture approval and false-positive review | No | Separate helper/validator/fixture approval |

Blocker Ledger:

| Blocker | Current Status | Cleared By This Cycle? | Reason | Next Legal Action |
| --- | --- | --- | --- | --- |
| `Current Branch Template Work Incomplete` | Active | No | Packages A-E remain current-PR scope and unresolved | USER chooses more proof, USER evidence, later FAM/runtime proof, waiver/reclassification, reject/defer, or blocked posture |
| `Golden Reference Promotion Blocked` | Active | No | No USER visual acceptance or catalog record exists | Collect proof and request explicit later promotion approval |
| `Package A proof incomplete` | Active | No | Strong candidates exist but key control/window states and USER acceptance are missing | Focused Package A proof collection or USER evidence |
| `Package B proof incomplete` | Active | No | Control state matrix is incomplete | Additional proof or later owning-FAM proof |
| `Package C proof incomplete` | Active | No | Modal/status/tray/settings proof is insufficient | Later owning-FAM/runtime proof |
| `Package D implementation/proof incomplete` | Active | No | Token/shared-primitive carrier is future-gated | Separate implementation-planning approval |
| `Package E enforcement implementation incomplete` | Active | No | Helper/validator/fixture mutation is future-gated | Separate enforcement approval |

Next Legal Use:

The next legal phase is still not PR Readiness. USER should decide whether to continue proof collection, provide USER evidence, route later owning-FAM/runtime proof, explicitly waive/reclassify named lanes, reject/defer named lanes, or keep the branch blocked. If USER wants AI Control Center to become the reference seed, the next legal route is a named Package A proof/USER visual acceptance path; promotion still requires explicit USER approval and a later catalog record.

## Template / Golden Reference Consolidated Package A-E Runtime Proof Collection - 2026-06-17

Document Status: Non-Binding Planning / Source-Truth Receipt. Binding authority remains with `Docs/family_visions/FAM-002_desktop_interface.md`, `Docs/family_feature_visions/F2-FF01.md`, `Docs/ui_reference_catalog/`, `Docs/phase_governance.md`, and `Docs/branch_plans/README.md`.

Accepted Evidence Posture:

- USER accepted the consolidated Package A-E proof collection execution corridor as reported.
- USER approved bounded runtime proof collection using FAM-003/FAM-006/FAM-007 surfaces as evidence sources only.
- FAM-007 AI Control Center remains the strongest Package A seed but is not promoted.
- HUD/FAM-006 remains comparison evidence and possible future adoption/refit target but is not promoted.
- Package E enforcement remains future-gated until visual proof/reference lanes are clearer.
- `Docs/ui_reference_catalog/index.md` remains `Promoted Reference Count: 0`.

Proof-Source Identity Result:

| Source | Worktree / Evidence Root | Branch / State | Runtime Capture Decision |
| --- | --- | --- | --- |
| FAM-003 | `C:\Nexus Worktrees\FAM-003`; `C:\Nexus USER\FAM-003`; `dev\logs\desktop_entrypoint_validation` | Clean; upstream-aligned feature branch; ahead of origin/main | No new runtime capture. Existing logs are runtime/log context only; no visual tray/settings proof found. |
| FAM-006 | `C:\Nexus Worktrees\FAM-006`; `C:\Nexus USER\FAM-006`; `dev\logs\fam_006_human_client_validation` | Clean; upstream-aligned feature branch; ahead of origin/main | No new runtime capture required. Existing human-client screenshots, short video, and manifests are copied as evidence. |
| FAM-007 | `C:\Nexus Worktrees\FAM-007`; `C:\Nexus USER\FAM-007`; `dev\logs\fam_007_ai_control_center_live_resize` | Clean; upstream-aligned historical feature branch; behind current origin/main | No new runtime capture. Existing AI Control Center live-resize proof is copied as candidate evidence only. |

Runtime Proof Table:

| Package | Candidate | Required State / Proof | Evidence Collected | Source | Independent? | Sufficient? | Visual/Product Notes | Remaining Gap | Next Legal Route |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | AI Control Center top-level window | Default, resize, geometry, frame/chrome, multi-surface comparison, USER visual acceptance | FAM-007 live-resize focused/full-desktop screenshots for default, close-hover, scrollbar, run-local-check hover, corner/right/bottom/top-right resize plus manifest | Existing FAM-007 USER/log evidence | Mostly yes | No | Strongest current Package A seed; runtime evidence is useful but still source-candidate only | Independent minimize-hover, maximize/restore applicability, platform exception classification, accessibility/hitbox proof, USER acceptance | Later Package A proof/USER visual acceptance path |
| A | Compact window-control cluster | Close/minimize/maximize/restore applicability, hover/focus/pressed/blocked/disabled states | FAM-007 close-hover proof plus duplicate default/minimize-hover proof | Existing FAM-007 USER/log evidence | Mixed | No | Close-hover remains useful; minimize-hover remains duplicate by SHA256 | Independent minimize-hover, maximize/restore, disabled/blocked/focus/pressed/hitbox proof | Later focused control-cluster proof |
| A | HUD/FAM-006 dashboard/window comparison | User-facing HUD/Dashboard surface, tray open/close, geometry context, video proof | FAM-006 human-client screenshots, short videos, manifests, HUD launch/open/close/resize/tray menu evidence | Existing FAM-006 dev log and USER evidence | Yes as comparison | No | Strong runtime comparison evidence; visually not promoted and UTS acceptance remains separate | USER acceptance and any adoption/refit proof after reference promotion | Later FAM-006 adoption/evaluation path |
| B | Buttons/dropdowns/menus/lists/filters | Button, selector, menu, list/filter states, keyboard/accessibility, hover/focus/disabled/loading/error | FAM-006 tray menu, HUD quick actions, selector evidence; FAM-007 Run Local Check hover and scrollbar evidence | Existing FAM-006/FAM-007 evidence | Partial | No | Gives better runtime coverage than the prior packet but still not full state taxonomy | Open dropdown/menu/list/filter matrices, keyboard/accessibility, disabled/loading/error proof, USER acceptance | Continue proof collection or later FAM/runtime proof |
| C | Modal/dialog, status/failure/recovery, tray/settings doorway | Modal/dialog taxonomy, status/failure/recovery sequence, resident tray/menu doorway, settings surfaces | FAM-006 returned UTS/failure context, FAM-006 tray-menu screenshots, FAM-003 desktop-entrypoint logs, F3-FF01 context | Existing FAM-003/FAM-006 evidence | Partial | No | Runtime logs and tray screenshots are useful, but FAM-003 lacks visual proof and modal/status taxonomy remains incomplete | FAM-003 tray/settings visual proof, FAM-001/FAM-006 status/failure proof, focus/keyboard/accessibility, USER acceptance | Later owning-FAM/runtime proof |
| D | Design tokens/shared UI rules | Token taxonomy, accepted ranges, source-to-visual trace, reusable primitive boundary | FAM-002 grammar plus FAM-006/FAM-007 visual comparison evidence | Source truth and copied evidence | Partial | No | Candidate extraction input only; no shared primitive or token implementation approved | Accepted values, code-to-visual trace, contrast proof, migration/adoption plan, USER acceptance | Future implementation-planning carrier |
| E | Anti-pattern/helper/validator expectations | Negative examples, false-green prevention, helper/validator/fixture proof | Existing no-overclaim rules and current runtime proof gaps | Governance source-truth context | Yes as planning evidence | No | The proof gaps are useful future fixture examples, but no helper/validator/fixture mutation is approved | USER approval for fixture/helper/validator work and false-positive review | Future enforcement carrier |

Promotion-Readiness Table:

| Package | Candidate | Promotion Readiness | Reason | Can Move To USER Promotion Review? | Later Approval Needed |
| --- | --- | --- | --- | --- | --- |
| A | AI Control Center top-level window | Strongest seed, still proof-blocked | Runtime evidence improved, but acceptance, state coverage, and applicability matrix remain incomplete | Not yet as promotion; yes as focused proof target | USER evidence or later FAM/runtime proof plus USER visual acceptance |
| A | Compact window-control cluster | Strong seed, proof-blocked | Independent minimize-hover and control applicability are still missing | Not yet | Focused state proof and USER visual acceptance |
| A | HUD/FAM-006 comparison/adoption target | Comparison only | Runtime proof is useful but not accepted as standard | No | Later consuming-FAM adoption/evaluation |
| B | Controls/dropdowns/menus/lists/filters | Better evidence, insufficient | Runtime examples exist but state taxonomy is incomplete | No | More proof or later owning-FAM/runtime evidence |
| C | Modal/status/tray/settings | Better context, insufficient | FAM-003 visual tray/settings proof is missing; FAM-006 status/failure proof is not a promoted reference | No | Later owning-FAM/runtime proof |
| D | Tokens/shared rules | Not ready | Requires implementation-planning carrier after references stabilize | No | Separate implementation approval |
| E | Negative fixtures/helper/validator checks | Not ready | Requires code/fixture approval and false-positive review | No | Separate enforcement approval |

Blocker Ledger:

| Blocker | Current Status | Cleared By This Cycle? | Reason | Next Legal Action |
| --- | --- | --- | --- | --- |
| `Current Branch Template Work Incomplete` | Active | No | Runtime proof improves evidence but Packages A-E remain unresolved | USER chooses more proof, USER evidence, later FAM/runtime proof, waiver/reclassification, reject/defer, or blocked posture |
| `Golden Reference Promotion Blocked` | Active | No | No USER visual acceptance or catalog record exists | Collect proof and request explicit later promotion approval |
| `Package A proof incomplete` | Active | No | Strongest seed remains missing key state/accessibility/acceptance proof | Focused Package A proof or USER evidence |
| `Package B proof incomplete` | Active | No | Runtime control evidence is partial | Additional proof or later owning-FAM proof |
| `Package C proof incomplete` | Active | No | FAM-003 visual tray/settings proof and failure/status taxonomy are incomplete | Later owning-FAM/runtime proof |
| `Package D implementation/proof incomplete` | Active | No | Token/shared-primitive carrier is future-gated | Separate implementation-planning approval |
| `Package E enforcement implementation incomplete` | Active | No | Helper/validator/fixture mutation is future-gated | Separate enforcement approval |

Next Legal Use:

The next legal phase remains blocker-disposition digestion for Packages A-E. Runtime evidence makes AI Control Center the strongest candidate seed, but the branch remains blocked until USER either continues proof collection, supplies USER evidence, routes later FAM/runtime proof, explicitly waives/reclassifies named lanes, rejects/defers named lanes, or keeps the branch blocked.

## Template / Golden Reference Consolidated Package A-E Green Completion - 2026-06-17

Document Status: Non-Binding Planning / Source-Truth Receipt. Binding authority remains with `Docs/ui_reference_catalog/` for promoted reference records, `Docs/family_feature_visions/F2-FF01.md` for the UI reference-system feature vision, `Docs/family_visions/FAM-002_desktop_interface.md` for reusable presentation grammar, and `Docs/phase_governance.md` / `Docs/branch_plans/README.md` for phase and proof boundaries.

USER Decision Applied:

- USER approved bounded continuation until all Package A-E lanes are green.
- Governance may promote durable UI reference catalog records when the record includes USER acceptance/waiver, source evidence, applicability, known limitations, adoption rule, and final disposition.
- Missing runtime states must not be rewritten as proven; they must be recorded as known limitations or future consuming-branch proof obligations.
- FAM worktree mutation, runtime UI implementation, issue mutation, PR creation, merge, release, external-state mutation, and code-level helper/validator/fixture/shared-primitive implementation remain outside this completion pass.

Package Green Table:

| Package | Green Disposition | Source-Truth Record | What Is Green Now | What Remains Future-Owned |
| --- | --- | --- | --- | --- |
| A | `GREEN - promoted with known limitations` | `UIREF-001`, `UIREF-002` | Top-level window frame grammar and compact window-control cluster grammar are promoted as durable references. | Consuming branches still prove their own control states, accessibility, geometry/reset behavior, and exceptions. |
| B | `GREEN - promoted with known limitations` | `UIREF-003` | Baseline button/control/selector grammar is promoted. | Dropdown/menu/list/filter open states, keyboard accessibility, disabled/loading/error states, and branch-specific controls remain proof obligations. |
| C | `GREEN - promoted with known limitations` | `UIREF-004` | Dialog/status/recovery/doorway surface grammar is promoted. | FAM-001/FAM-003/FAM-006/FAM-007/FAM-008 runtime adoption and visual proof remain owned by those legal carriers. |
| D | `GREEN - source-truth baseline accepted; implementation deferred` | `UIREF-005` | Design-token and shared-rule baseline is promoted as durable source-truth reference. | Code-level design-token/shared-primitive implementation, migration, rollback, and visual parity proof remain future implementation work. |
| E | `GREEN - enforcement contract accepted; code deferred` | `UIREF-006` | Negative-example and enforcement contract is promoted as durable guidance. | Executable fixtures, helper code, validator code, and false-positive review remain future implementation work. |

Promoted Catalog Result:

- `Docs/ui_reference_catalog/index.md` now records `Promoted Reference Count: 6`.
- `UIREF-001` and `UIREF-002` are Package A references.
- `UIREF-003` is the Package B reference.
- `UIREF-004` is the Package C reference.
- `UIREF-005` is the Package D baseline record.
- `UIREF-006` is the Package E enforcement contract record.

No-Overclaim Guard:

- Promoted-with-known-limitations does not mean every screenshot, runtime state, or FAM implementation is accepted.
- Candidate FAM-006/FAM-007 evidence remains evidence; catalog records own the durable reference contract, not live proof inventories.
- Consuming branches must cite the applicable UIREF record and still prove their own UI/UX implementation against Project Vision, FAM-002 grammar, the relevant Family/Family Feature Vision, BP2/BP3 proof plan, Hardening, Live Validation, and USER review where required.
- A future branch must not claim code-level design tokens, shared primitives, helper enforcement, validator enforcement, or fixture coverage exists until that code/fixture work is separately implemented and validated.

Blocker Disposition Table:

| Prior Blocker | Current Disposition | Why |
| --- | --- | --- |
| `Current Branch Template Work Incomplete` | `Cleared for Package A-E source-truth scope` | All current Package A-E lanes now have a durable green disposition or accepted future-owned implementation boundary. |
| `Golden Reference Promotion Blocked` | `Cleared for UIREF-001 through UIREF-006` | USER-approved completion allowed promoted records with known limitations and explicit adoption boundaries. |
| `Package A proof incomplete` | `Cleared by UIREF-001/UIREF-002 with known limitations` | Missing states remain consuming-branch proof obligations instead of blocking Governance source-truth promotion. |
| `Package B proof incomplete` | `Cleared by UIREF-003 with known limitations` | Baseline control grammar is promoted; state-specific proof remains per branch. |
| `Package C proof incomplete` | `Cleared by UIREF-004 with known limitations` | Grammar is promoted; runtime/status/tray/settings implementation proof remains with owning FAMs. |
| `Package D implementation/proof incomplete` | `Cleared by UIREF-005 as source-truth baseline; implementation deferred` | Governance promoted the design-rule baseline but did not implement code-level tokens/shared primitives. |
| `Package E enforcement implementation incomplete` | `Cleared by UIREF-006 as enforcement contract; code deferred` | Governance promoted the enforcement contract but did not mutate helpers, validators, or fixtures. |

PR Readiness Impact:

Package A-E source-truth completion is no longer the current PR hold. PR Readiness Stage 1 may be the next legal analysis phase after validation, but PR Readiness, PR creation, merge, release, FAM adoption, runtime implementation, code-level design-token/shared-primitive work, helper/validator/fixture work, issue mutation, external-state mutation, and cleanup remain separate USER decisions.

## Final Recommendation

ChatGPT's strongest insight is correct: the next governance risk is ownership duplication. The best repair is not "more governance everywhere"; it is better owner classification before new concepts become FAMs, architecture systems, policies, experience layers, or implementation work.

Recommended priority order:

1. Taxonomy / Owner Discipline.
2. Architecture / Experience / Policy Impact Matrix.
3. Hypothesis-Driven Reliability.
4. PR / Review Drift Prevention.
5. Main / Dev / Owner boundary planning, public-safe only unless a later FAM-007 or split carrier is approved.
6. Governance quickstart.
7. Optional explicit registries only after existing owners prove insufficient.
