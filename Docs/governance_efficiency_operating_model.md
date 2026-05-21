# Governance Efficiency Operating Model

## Purpose

This document is the compact operating model for governance reform after the multi-worktree transition.

It exists to reduce repeated source-truth updates, shrink routine prompt load, and keep safety gates enforceable without turning backlog, roadmap, or branch records into duplicate live-state ledgers.

## Scope

This model applies to governance/source-truth/process reform only.

It does not authorize runtime implementation, FAM-006 mutation, FAM-007 mutation, successor branch creation, release execution, tag or GitHub Release work, issue closeout, branch deletion, worktree cleanup, provider/model execution, downloads, memory work, voice/Core sync, shortcut or installer work, AI Product Contract import, or private Dev ORIN import.

## Rule ID And Owner Model

Future governance changes should use a rule ID, one owner, and compact mirrors.

Rule ID format:

- `GEF-001`

Required fields for new reform rules:

- `Rule ID:`
- `Rule Name:`
- `Owner File:`
- `Compact Mirrors:`
- `Validator / Helper Owner:`
- `Allowed Mutation Carrier:`
- `Do Not Duplicate In:`
- `Historical Receipt Rule:`

Full normative policy belongs in the owner file. Mirrors should summarize the rule and point to the owner instead of repeating full policy prose.

## Source-Truth Ownership Matrix

Use this ownership model before creating or updating a governance/source-truth file:

| Surface | Owns | Must Not Own |
| --- | --- | --- |
| `Docs/Main.md` | highest-level routing map, source-truth layer ownership, recovery pointers | detailed branch execution narratives |
| `Docs/phase_governance.md` | normative phase rules, phase enum, blockers, gates, proof hierarchy | branch-local implementation details |
| `Docs/development_rules.md` | developer-facing execution rules and compact phase mirrors | duplicate full policy blocks already owned elsewhere |
| `Docs/codex_modes.md` | Codex operating posture and mode behavior | branch-local truth or release receipts |
| `Docs/orin_task_template.md` | reusable prompt skeleton fields | current live branch facts |
| `Docs/codex_user_guide.md` | human-readable operator guide | machine-enforced current-state authority |
| `Docs/worktree_slots.md` | stable slot IDs and intended assignment receipts | `HEAD`, dirty state, ahead/behind, PR state, latest tag, latest release |
| `Docs/feature_backlog.md` | compact feature-family registry, status, and pointer layer | detailed active-branch execution planning |
| `Docs/prebeta_roadmap.md` | release sequencing and milestone posture | volatile Git/GitHub operational state |
| `Docs/branch_records/index.md` | active/historical branch authority routing | detailed branch implementation checklists |
| `Docs/branch_records/<branch>.md` | branch authority, phase history, approvals, legal next phase, compact branch receipt | reusable family-level implementation history after fold-down |
| `Docs/branch_plans/<branch>.md` | active runtime branch engineering plan, per-seam checklist, plan-to-implementation traceability | permanent family-level dossier after PR fold-down unless explicitly retained |
| `Docs/workstreams/index.md` | canonical workstream and dossier routing | per-branch live state by inertia |
| `Docs/workstreams/<id>.md` | durable promoted implementation history and reusable continuity | volatile branch/PR state |
| `Docs/validation_helper_registry.md` | durable helper inventory, statuses, reuse/consolidation decisions | workstream evidence details already owned by branch/workstream docs |
| `Docs/governance_process_efficiency_reform_plan.md` | reform inventory, sequencing, and implementation records | operational live Git/GitHub facts |
| `Docs/governance_intake_triage_and_digest_profiles.md` | governance intake and digest profile standard | branch-specific blocker narratives |
| `Docs/pr_watcher_mode_contract.md` | watcher mode contract and approval default | live PR state beyond explicit watcher proof packets |

## Docs Source-Truth Reform Model

Docs Source-Truth Reform Model: Compact Pointer Layer.

The post-audit reform model has one owner per active fact class:

- backlog owns compact product-family identity and canonical pointers
- roadmap owns release sequencing and public milestone posture
- worktree slots own reusable slot definitions and intended assignment receipts
- branch records own branch authority, approvals, phase history, and compact branch receipts
- branch plans own detailed active runtime-branch engineering plans
- workstreams and family dossiers own durable package trace, slice trace, proof history, and reusable continuity
- Git, GitHub, and approved helpers own live operational truth

Backlog and roadmap must not contain `Package Trace:` or `Slice Trace:` sections. Those detailed ledgers belong in workstream records, family dossiers, branch plans, or compact branch receipts.

Backlog and roadmap must not manually maintain latest public prerelease, latest tag, release URL, target commit, open PR state, active branch identity, review-thread state, worktree dirty state, or ahead/behind state as active truth. They may point to the helper or owner that derives that truth.

Historical receipts remain allowed when they are explicitly historical interpretation, compact, and routed to the owning receipt surface.

## Derived Live Truth Versus Historical Receipt

Derived live truth comes from Git, GitHub, or approved helpers. Examples include current `HEAD`, `origin/main`, merge base, dirty state, branch ahead/behind state, remote ref existence, open PR state, review-thread state, latest tag, latest GitHub Release, and issue state.

Governance receipts are recorded after live truth is checked. Examples include USER assignment decisions, branch admission, release scope interpretation, merge closeout, watcher repair proof, and branch-plan fold-down.

Docs may record historical receipts, but they must not pretend to be live operational truth. When a current operational fact is needed, run a helper or live check and report it as evidence.

## Duplicate Live-State Guard

Backlog, roadmap, branch records, worktree slots, and workstream docs must not all manually track the same volatile state.

Allowed compact current-state markers:

- a current decision surface in backlog or roadmap
- branch authority status in the active branch record
- slot assignment receipt in `Docs/worktree_slots.md`
- historical receipts after live truth is validated

Prohibited duplication by default:

- raw `HEAD` or `origin/main` hash as current truth outside an operator packet or historical receipt
- open PR state in merged-main current-state sections
- live watcher state in backlog or roadmap
- detailed per-seam runtime plan narrative in backlog or roadmap
- release/latest-tag truth copied into multiple docs without validator or GitHub check
- `Package Trace:` or `Slice Trace:` detail inside backlog or roadmap
- repeated release-window PR lists inside both backlog and roadmap

If duplication is unavoidable for scanability, name the owner and make the mirror explicitly compact.

## Current Summary And Historical Appendix Split

Large branch records should keep current machine-readable truth near the top and move long narrative to a historical appendix or folded receipt.

Preferred structure:

- top current summary and required markers
- current blockers and next legal phase
- active plan pointers
- validation and receipt summary
- historical appendix or fold-down receipt

Validators should prefer the current summary when checking phase posture. Historical appendices must not retain live active-branch, live PR, or pending watcher wording unless clearly labeled historical.

## Phase Alias UX

Canonical phase names remain unchanged for validators:

- `Branch Readiness`
- `Workstream`
- `Hardening`
- `Live Validation`
- `PR Readiness`
- `Release Readiness`

Human-facing aliases may be used only as explanatory labels:

- `Branch Readiness Stage 1` -> `Plan Review`
- `Branch Readiness Stage 2` -> `Setup / Admission`
- `Workstream` -> `Build`
- `Hardening` -> `Stabilize`
- `Live Validation` -> `User Proof`
- `PR Readiness Stage 1` -> `Merge Readiness Audit`
- `PR Readiness Stage 2` -> `PR Execution / Watch`
- `Release Readiness` -> `Release Validation`
- `Standing Governance Intake` -> `Policy Repair Lane`

Aliases must never replace canonical phase markers in source truth.

## Branch Planning UX Standard

Runtime Branch Readiness should separate dense planning into:

- `Product Intent Summary`
- `Engineering Contract`
- `Decision Ledger`
- `Deferred / Future Ledger`
- `Implementation Sequence`
- `Proof Plan`

The user-facing packet should summarize each area and point to the Branch Runtime Engineering Plan for detail. The detailed plan remains in `Docs/branch_plans/<branch_slug>.md`; backlog and roadmap stay compact pointer/status surfaces.

## Branch Record / Plan / Workstream Fold-Down Model

Branch records, branch plans, and workstreams are related but not interchangeable.

Use this split:

- branch records own branch authority, approvals, phase history, blockers, legal next phase, and compact branch receipts
- branch plans own detailed active runtime planning while the branch is active
- workstreams and family dossiers own durable package trace, slice trace, proof history, reusable lessons, and family continuity

At PR Readiness, every runtime-focused branch needs a fold-down or retention decision:

- keep the branch plan as historical branch source truth when the detail is branch-specific evidence
- compact only the receipt into the branch authority record when the plan is too detailed for long-term active loading
- promote reusable lessons, package trace, slice trace, validators, and proof history to workstreams or family dossiers
- leave backlog and roadmap as compact pointers instead of copying the plan or trace tables

Historical receipts may preserve PRs, tags, releases, and commit hashes when they are evidence for a closed decision. They must not be presented as live operational truth or repeated across backlog and roadmap.

## Standing Governance Ledger Compaction

The standing Governance record may keep one compact current cycle summary plus a latest closed cycle pointer.

Detailed historical RRI cycles should be folded into compact historical receipts, PR links, or appendices instead of forcing dedicated closeout PRs that only clear cycle wording.

Required current fields:

- `Active RRI Cycle:`
- `Latest Closed RRI Cycle:`
- `Intake State:`
- `Return Digest Status:`
- `Sync Rule:`
- `Next Legal Phase:`

## Release Ownership UX

Release Readiness remains file-frozen. Release execution requires separate approval.

When multiple runtime or governance PRs merge before the next release, the default release ownership model is:

- `Release Ownership Model: Aggregated release window`

A release assembler or release captain packages the selected release window. This role does not own implementation and may not mutate source truth during Release Readiness.

Release packets must distinguish:

- implementation contributors
- governance/readiness contributors
- excluded or future-gated work
- public user-facing highlights
- internal validation support that should not dominate public notes

## Public Language Mapping

Release and public-facing text should translate internal engineering work into user value.

Mapping fields:

- `Internal Scope:`
- `Public-Facing Scope:`
- `User-Visible Benefit:`
- `Excluded Work:`
- `Future-Gated Capabilities:`
- `Validation Confidence:`
- `Internal Jargon Review:`

Internal governance names, branch names, helper names, and automation wording should appear in public release notes only when needed for transparency.

## Validator Modularization Boundary

`dev/orin_branch_governance_validation.py` remains the stable CLI wrapper.

Future modularization may split internals into helper modules only if:

- the command interface stays stable
- existing validation output remains understandable
- module ownership is registered in `Docs/validation_helper_registry.md`
- the split is validated before any behavior-changing enforcement is added

Do not mix broad validator modularization with runtime implementation.

## Validation Runner And Registry Query Rule

Use `dev/orin_validation_suite.py` when a branch needs a validation recommendation packet.

That helper is report-only. It recommends commands with rationale and does not execute commands or mutate files.

## Naming Drift Scan Rule

Product/persona naming cleanup requires a named governance or product-surface carrier.

Historical GitHub tags, release titles, old branch records, and prior evidence may preserve old names as historical truth. Current public UI, release notes, branch plans, and new docs should avoid introducing retired/internal names unless the owning source truth explicitly allows historical context.

## Reform Pass Completion Model

The consolidated governance reform PR may complete the policy, pointer, and validator scaffolding for all reform categories in `Docs/governance_process_efficiency_reform_plan.md`.

It must not perform broad historical migration, branch deletion, worktree cleanup, runtime mutation, release execution, or FAM lane mutation. Those remain separate USER decisions.

## Next Legal Phase

After this operating model merges, future governance efficiency work should use the owner matrix and helper validation instead of creating new duplicate current-state surfaces.
