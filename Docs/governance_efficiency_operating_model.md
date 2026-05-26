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
| `Docs/Main.md` | least-updated canonical docs index, source-truth layer ownership, recovery pointers, and clear digest of valid governance/source-truth files | detailed branch execution narratives or volatile current-state ledgers |
| `Docs/phase_governance.md` | normative phase rules, phase enum, blockers, gates, proof hierarchy | branch-local implementation details |
| `Docs/development_rules.md` | developer-facing execution rules and compact phase mirrors | duplicate full policy blocks already owned elsewhere |
| `Docs/codex_modes.md` | Codex operating posture and mode behavior | branch-local truth or release receipts |
| `Docs/orin_task_template.md` | reusable prompt skeleton fields | current live branch facts |
| `Docs/codex_user_guide.md` | human-readable operator guide | machine-enforced current-state authority |
| `Docs/worktree_slots.md` | stable slot IDs and intended assignment receipts | `HEAD`, dirty state, ahead/behind, PR state, latest tag, latest release |
| `Docs/feature_backlog.md` | compact feature-family registry, status, and pointer layer | detailed active-branch execution planning |
| `Docs/prebeta_roadmap.md` | release-stage schedule outline, milestone breakpoints, and broad feature-family checkpoints | volatile Git/GitHub operational state or active release ledger fields |
| `Docs/nexus_vision.md` | project-wide product vision contract, long-term standards, and durable product direction | active branch implementation plans or family-specific execution ledgers |
| `Docs/family_visions/` | family-specific durable product direction and reusable USER-accepted standards | active branch authority, live state, or per-seam implementation checklists |
| `Docs/branch_records/index.md` | active/historical branch authority routing | detailed branch implementation checklists |
| `Docs/branch_records/<branch>.md` | branch authority, phase history, approvals, legal next phase, compact UFD pointer/status markers, structured traceability receipt | volatile live state, unindexed execution diaries, full feedback text, or reusable family-level implementation history after promotion |
| `Docs/branch_plans/<branch>.md` | active runtime branch engineering plan, non-runtime Branch Engineering Plan when overlap intent evidence is required, USER Feedback Disposition full-detail owner while active, Branch Change Intent Ledger owner for `Rebaseline Overlap Files:`, per-seam checklist, plan-to-implementation traceability while active | permanent family-level dossier, active authority after fold-down, duplicate feedback ledger, or live-state ledger after retirement |
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
- roadmap owns the pre-Beta/Beta/release schedule outline, milestone breakpoints, and broad feature-family checkpoints
- worktree slots own reusable slot definitions and intended assignment receipts
- branch records own branch authority, approvals, phase history, and structured branch traceability receipts
- branch plans own detailed active runtime-branch engineering plans, full active USER Feedback Disposition items, USER-reviewable Element-to-Phase Proof Matrix planning, and retire after fold-down
- branch plans own full active Branch Change Intent Ledger evidence when rebaseline overlap exists; branch records receive compact fold-down receipts only when durable evidence remains useful
- workstreams and family dossiers own durable package trace, slice trace, proof history, and reusable continuity
- Git, GitHub, and approved helpers own live operational truth

Backlog and roadmap must not contain `Package Trace:` or `Slice Trace:` sections. Those detailed ledgers belong in workstream records, family dossiers, active branch plans, or structured branch receipts.

Backlog and roadmap must not manually maintain latest public prerelease, latest tag, release URL, target commit, open PR state, active branch identity, review-thread state, worktree dirty state, or ahead/behind state as active truth. The roadmap is a stage-breakpoint reference, not a release ledger. These surfaces may point to the helper or owner that derives live truth.

Historical receipts remain allowed when they are explicitly historical interpretation, compact, and routed to the owning receipt surface.

## Derived Live Truth Versus Historical Receipt

Derived live truth comes from Git, GitHub, or approved helpers. Examples include current `HEAD`, `origin/main`, merge base, dirty state, branch ahead/behind state, remote ref existence, open PR state, review-thread state, latest tag, latest GitHub Release, and issue state.

Governance receipts are recorded after live truth is checked. Examples include USER assignment decisions, branch admission, release scope interpretation, merge closeout, watcher repair proof, and branch-plan fold-down.

Docs may record historical receipts, but they must not pretend to be live operational truth. When a current operational fact is needed, run a helper or live check and report it as evidence.

## Duplicate Live-State Guard

Backlog, roadmap, branch records, worktree slots, and workstream docs must not all manually track the same volatile state.

Allowed compact non-live markers:

- compact backlog/roadmap status and owner pointers that do not manually maintain volatile live facts
- branch authority status in the active branch record
- slot assignment receipt in `Docs/worktree_slots.md`
- historical receipts after live truth is validated

Canonical docs and context docs are distinct. `Docs/Main.md` is the highest-level canonical docs index: it should be updated rarely, point to the current valid governance/source-truth files, and explain each file's intended purpose clearly enough to recover the system. Context docs may preserve historical evidence, workstream detail, branch receipts, product reasoning, or implementation lessons, but they must point back to their canonical owner and must not pretend to be the top-level source of current governance law.

Main-first loader chain: `Docs/Main.md` routes Codex to the owning source-truth files. Context docs and review bundles may point to Main and the relevant owner, but they must not become alternate first loaders or duplicate detailed policy that belongs in phase governance, vision owners, branch plans, branch records, or helper registries.

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

- branch records own branch authority, approvals, phase history, blockers, legal next phase, and structured branch traceability receipts
- branch plans own detailed active runtime planning, Element-to-Phase Proof Matrix planning, and current element proof-path mapping while the branch is active
- workstreams and family dossiers own durable package trace, slice trace, proof history, reusable lessons, and family continuity

At PR Readiness, every runtime-focused branch needs a fold-down or retirement decision:

- retire the branch plan after durable content is migrated and no active branch depends on it
- preserve branch-specific evidence in a structured branch receipt when it is needed for later debugging, rollback analysis, or USER memory
- promote reusable lessons, package trace, slice trace, validators, and proof history to workstreams or family dossiers
- leave backlog and roadmap as compact pointers instead of copying the plan or trace tables

Traceability compaction must not mean evidence loss. Large branch records may remain large when they are the correct historical ledger, but they should be organized for USER review and Codex indexing: current summary first, clear historical sections, commit/PR/release evidence, changed-surface map, validation proof, and links to promoted workstream/family-dossier detail. The reform target is less chaos and less duplicate live state, not smaller files at the cost of useful evidence.

Historical receipts may preserve PRs, tags, releases, and commit hashes when they are evidence for a closed decision. They must not be presented as live operational truth or repeated across backlog and roadmap.

## Docs Organization Cleanup Pass Rule

When USER asks for a docs organization cleanup pass, the first pass is non-destructive unless USER explicitly approves exact file moves, renames, deletions, archival, or historical rewrites.

The cleanup pass must use `Docs/governance_docs_full_inventory_reform_audit.md` and `Docs/governance_docs_reform_user_review_index.md` as the review surface. It should classify and prioritize cleanup lanes, preserve source-truth owners, identify replacement owners before any retirement/delete recommendation, and return a Desktop review bundle with the files USER needs to inspect.

Safe cleanup planning may:

- clarify queue status and cleanup lane priority
- label oversized branch records for later structured-receipt organization
- label retired branch plans for later reference-proof review
- label low-risk reference docs for possible future consolidation
- identify missing indexes, README routing gaps, and owner-map ambiguity

Safe cleanup planning must not:

- move, rename, delete, archive, or rewrite historical files
- collapse historical receipts into summaries without replacement-owner proof
- treat branch records, backlog, roadmap, worktree slots, or `Docs/Main.md` as live-state ledgers
- mutate runtime, release, FAM, Compact-AI, issue, branch-cleanup, or worktree state

The default cleanup sequence is: inventory and classify, review queue and owner routing, choose one focused cleanup lane, create a USER review bundle, then request exact USER approval before any physical file or history-affecting change.

## Product Vision Contract Model

`Docs/nexus_vision.md` is the Nexus-wide product vision contract. It was promoted from the former `Docs/orin_vision.md` path after focused reference migration so Branch Readiness has a stable project-wide vision owner.

The vision contract should drive backlog-family planning and Branch Readiness recommendations. A backlog item may need its own family-level vision record or vision section when the product intent is not obvious, but that vision is not a branch plan and should not duplicate per-seam implementation detail. The vision explains what outcome the plan must satisfy; the Branch Runtime Engineering Plan explains how the active branch intends to implement and prove it.

Vision records should support USER/Codex back-and-forth. They may grow as implementation teaches the project, but changes should be explicit USER-reviewed product intent, not accidental branch-local drift.

Family vision records live under `Docs/family_visions/` and receive reusable vision updates folded down from PR Readiness only after USER acceptance. Backlog and roadmap point to those records; they do not copy full family vision narratives.

## Vision-To-Plan Interaction Loop

The Vision Contract layer complements Branch Runtime Engineering Plans. It does not create a parallel planning system.

Use this layer when product/design assumptions would otherwise become implementation truth by Codex inference:

- Nexus Vision owns project-wide principles, long-term standards, and durable product direction through `Docs/nexus_vision.md`.
- Family Vision owns broad feature-family direction through `Docs/family_visions/` when the family is large enough to justify a durable owner.
- Branch Vision Contract Snapshot lives inside the active Branch Engineering Plan and records the USER-accepted branch-specific vision state.
- Branch Engineering Plan translates the accepted snapshot into seams, files, validators, proof, and stop conditions.
- Vision Question Digest is the required packet when product/design uncertainty affects planning or execution.
- Branch Plan Revision Packet is the required packet when accepted vision or accepted branch scope needs controlled revision.
- Plan-to-Implementation Traceability proves that implementation followed accepted vision and the branch plan.

Design assumption states:

- `Proposed by Codex`
- `Recommended by ChatGPT`
- `Accepted by USER`
- `Revised by USER`
- `Rejected by USER`
- `Deferred by USER`
- `Deferred With Waiver`
- `Superseded`
- `Needs USER Decision`

Only `Accepted by USER`, `Revised by USER`, or `Deferred With Waiver` design states are implementation-safe for user-facing/runtime behavior. Codex and ChatGPT recommendations remain proposed evidence until USER acts on them.

Before Workstream implementation, runtime/user-facing branches should record `Branch Vision Snapshot Status: Accepted`, `Open Vision Questions: None` or `Deferred With Waiver`, `USER Vision Green: Yes`, accepted implementation scope, accepted seam map, and accepted stop conditions. After that green point, new questions use the severity ladder: Level 1 non-blocking questions queue for later review, Level 2 seam-blocking questions pause only the affected seam, and Level 3 workstream-breaking questions return a Branch Plan Revision Packet before affected scope continues.

Vision Contract is required for user-facing UI/UX behavior change, runtime behavior change, workflow hierarchy change, visual standard change, setup or activation behavior change, provider/model/memory/voice/Core behavior, returned UTS that changes target behavior, broad family planning, ambiguous acceptance criteria, conflicting prior source truth, or any Codex recommendation that would otherwise become product/design truth. It may be marked not required for mechanical docs-only repair, validator-only repair with no product/runtime/user-facing impact, release-body formatting repair, source-truth typo/format repair, or branch metadata repair when the reason is recorded.

Accepted assumptions expire or require review when branch scope changes, returned UTS changes the accepted target, family vision changes, source truth contradicts the prior assumption, new user-facing behavior appears, or implementation would apply an old decision to a new family or surface.

## USER Feedback Disposition Model

USER Feedback Disposition (UFD) preserves meaningful USER feedback without creating another permanent feedback ledger.

The active Branch Runtime Engineering Plan is the full-detail owner for UFD items while the branch is active. Branch records, backlog, roadmap, workstream docs, family dossiers, Nexus Vision, and family vision owners may carry compact UFD pointers or folded outcomes only when they are the correct owner for the final disposition.

The branch plan keeps one ledger-level owner through `UFD Ledger Owner:`, one `UFD Ledger Status:`, `Open UFD Count:`, `Blocking UFD Count:`, and `Fold-Down Status:`. Each meaningful feedback item lives in a repeatable `### UFD Item: UFD-<scope>-YYYYMMDD-NNN` block.

Every meaningful feedback item should have one UFD ID, one canonical owner file, one USER decision state, one disposition type, one item status, one Workstream severity, and one fold-down target. UFD IDs use `UFD-<scope>-YYYYMMDD-NNN`; `FBK-*` is not allowed because it collides visually with historical `FB-###` workstream records.

Meaningful feedback requires UFD disposition when it affects branch scope, accepted vision, user-facing behavior, runtime behavior, validation proof, future work, reusable product standards, approval boundaries, or a USER decision. Minor comments, acknowledgements, typo-level notes, duplicate remarks, or non-actionable conversation may close without durable UFD only when Codex records the no-action reason.

Pointer locations may carry UFD ID, short title, canonical owner, compact status, and fold-down status only. They must not carry full feedback text, full decision history, or live implementation state.

At PR Readiness, each UFD item must be migrated, deferred with waiver, rejected/no-action with reason, closed, or explicitly carried to a future owner. Fold-down must preserve a lookup path from every UFD ID to its final owner after branch-plan fold-down and retirement.

Initial validator support is marker-first. It validates UFD ledger markers, repeated UFD item blocks, UFD IDs, required owner/status/decision markers, `No Durable Owner Needed` guardrails, count consistency, fold-down lookup posture, and exact-normalized duplicate `Feedback Summary:` entries inside one active UFD ledger. Broader fuzzy semantic duplicate or conflict detection remains human-review territory unless future fixtures and false-positive review prove it safe.

## USER Review Integration Decisions

The 2026-05-21 USER review responses are model-changing requirements, not passive review notes.

Required decisions from that intake:

- Complete the Docs reform as staged internal work on this same Governance carrier and one final PR path; avoid revolving PRs for every subtopic.
- Keep `Docs/Main.md` as the least-updated canonical docs index, recovery map, and pointer ledger.
- Distinguish canonical docs from context docs. Canonical docs own law, routing, or source-truth roles; context docs preserve evidence, product reasoning, implementation history, receipts, or review detail.
- Treat Branch Runtime Engineering Plans as canonical while active, then fold down and retire after durable content migrates. Deletion is not the default.
- Treat branch records as structured traceability receipts that may remain large when they preserve useful debugging, rollback, commit, PR, release, validation, and changed-surface evidence.
- Do not use "compaction" to erase traceability. The reform target is duplicate live-state removal, clearer organization, and owner routing.
- Delete or collapse low-risk/reference docs only after a reference scan, replacement owner, and USER acceptance prove the move is safe.
- Use `Docs/nexus_vision.md` as the Nexus Vision contract surface that drives backlog-family planning and Branch Readiness recommendations without duplicating branch plans.
- Use `Docs/family_visions/` for family-specific durable product direction while keeping backlog and roadmap compact.

The generated review dossier and index must expose these decisions through a USER response integration matrix, a single-PR staged execution plan, and explicit disposition changes. PR Readiness must stay held while USER is still correcting this model.

## USER Review Desktop Bundle Rule

When Codex asks USER to inspect repo files, review a generated dossier, approve a planning packet, or compare a source-truth reform surface, Codex must create or refresh the USER-facing stable Desktop review folder for the active worktree.

The Desktop bundle must:

- live under one stable Desktop root, `Nexus USER Review`, under the discovered Desktop path, preferring `C:\Users\<user>\OneDrive\Desktop\Nexus USER Review` when available and `C:\Users\<user>\Desktop\Nexus USER Review` otherwise
- use one child folder per active worktree label, derived from the current worktree root folder name when USER does not provide a label, such as `Governance`, `FAM-006`, or `FAM-007`
- refresh the same worktree-labeled child folder instead of creating a new top-level Desktop folder for each review packet
- copy the selected review files as flat files directly inside the worktree-labeled child folder, with traceable filenames when needed to avoid basename collisions, rather than creating constantly changing nested review folders
- block custom review roots, legacy one-off folder names, or manually supplied worktree labels unless USER grants an explicit custom review path waiver; when a waiver is used, `START_HERE.md` must record `Custom Review Path Waiver:` and `Custom Review Path Reason:`
- include a `START_HERE.md` file with `Review Purpose:`, source repo, `Source Branch:`, `Source HEAD:`, upstream, `origin/main:`, `Review Export Zip:`, `Review Export Zip Source HEAD:`, `Review Export Zip Stale Guard:`, `Validation Summary:`, `Review Order`, `Exact USER Decision This Bundle Supports:`, `Pending USER Decisions`, copied source paths, explicit bundle/copy file counts, and an extra-file count for stale artifacts left in non-cleared folders
- copy only the files relevant to the requested review, not the whole repo or unrelated artifacts
- preserve source traceability in `START_HERE.md` so every flat copied file maps back to its repo-relative source path
- be refreshed when the underlying review files change
- never replace source-truth files, commit artifacts, validation proof, or branch authority records

For Workstream Entry, the Desktop bundle is required before USER green-lights implementation when the branch has runtime, user-facing, source-truth, helper/validator, or workflow impact. The bundle must copy the branch vision, active Branch Runtime Engineering Plan or Branch Engineering Plan, Element-to-Phase Proof Matrix owner, branch authority record, relevant Nexus/family vision files, UFD/change-intent surfaces when applicable, and any other source-truth files the USER needs to inspect. The Workstream Entry digest must report the folder path, copied files, `USER Branch Plan Review Gate` status, `USER Review Packet Finding:`, and whole-package analysis status when multiple slices or seams are admitted. `USER Review Packet Finding:` must name `START_HERE.md`, `USER_BRANCH_PLAN_REVIEW.md`, the exported zip, packet source HEAD, current branch HEAD, freshness result, digest status, and waiver/blocker status. The bundle supports USER accepting, revising, deferring with waiver, rejecting, or requesting more analysis before implementation begins.

For governance review or PR-readiness review, the Desktop bundle should be self-checking: `Bundle File Count:` reports the actual file count present in the worktree review folder after copy plus `START_HERE.md`, `Copied File Count:` counts copied repo files only, `Expected File Count:` must match the intended copied repo-file count, and `Extra Bundle File Count:` reports stale or unrelated files that remain when a bundle is refreshed without `--clear`. Use `dev/orin_user_review_bundle.py` for repeatable local bundle creation; the helper defaults to `Nexus USER Review\<worktree-label>` and should not require USER to name a new folder for active worktrees. The helper must also overwrite a stable zip export at `Nexus USER Review\<worktree-label>.zip` from the freshly refreshed worktree folder and record `Review Export Zip:`, `Review Export Zip Source HEAD:`, and `Review Export Zip Stale Guard:` in `START_HERE.md`; USER-uploadable review zips created outside this helper are stale-risk evidence and must be regenerated before review or PR Readiness. `--review-root-name`, `--worktree-label`, or legacy `--folder-name` customizations require `--allow-custom-review-path` plus a recorded reason. If the Desktop path cannot be discovered or the folder/zip cannot be created, stop with `USER Review Desktop Bundle Missing` and return the exact blocker plus the copy command or helper command USER can run.

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

For `RRI-20260521-001` and related USER-approved bounded governance/source-truth repair carriers, the USER direction is one single final PR with staged internal commits rather than revolving PRs. Analysis, model updates, and planning refinements may continue on the currently approved Governance worktree carrier until USER accepts the reform review surface; cleanup execution remains bounded by this model and PR Readiness stays held until USER approval.

It must not perform broad historical migration, branch deletion, worktree cleanup, runtime mutation, release execution, or FAM lane mutation. Those remain separate USER decisions.

## Next Legal Phase

After this operating model merges, future governance efficiency work should use the owner matrix and helper validation instead of creating new duplicate current-state surfaces.
