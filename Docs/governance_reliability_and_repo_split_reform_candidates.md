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

## Recommended Next USER Decision

The admitted Governance Reliability / Repo Split Reform source-truth contract cycles and final integration hardening are complete, but USER later clarified that the planned Template / Reference work must be completed on the current Governance branch before PR Readiness. The next legal USER decision is a bounded Template / Golden Reference Promotion admission cycle on the current branch, not PR Readiness Stage 1.

Suggested exact decision shape:

```text
I approve a bounded Template / Golden Reference Promotion admission cycle on C:\Nexus Worktrees\Governance / feature/release-readiness-source-truth-intake before PR Readiness.

Current approval covers admitting and planning the remaining current-branch Template / Reference work, deciding owner/location/schema, deciding which candidate references may proceed to USER review, deciding whether design tokens/shared primitives/helper/validator/fixture/product-worktree adoption are included now or explicitly reclassified, and returning the exact implementation approval packet. This does not approve PR Readiness, PR creation, merge, release, external-state mutation, repo split execution, file movement/deletion/archival, private repo creation, FAM-006/FAM-007/main mutation, runtime/provider/model/shortcut/installer work, issue mutation, cleanup, Private Dev ORIN import, AI Product Contract import, helper/validator code mutation, fixture mutation, design-token/shared-primitive implementation, or actual template/golden-reference promotion unless the returned packet is separately approved.
```

Other legal USER responses:

- Request more hardening detail before template/reference admission.
- Explicitly reclassify one or more planned template/reference items out of current PR scope with reason.
- Approve a limited PR path despite incomplete template/reference work. This is not the current default.

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
