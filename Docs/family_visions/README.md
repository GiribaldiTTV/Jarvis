# Family Vision Records

## Purpose

`Docs/family_visions/` owns durable product-direction records for broad Nexus feature families when the backlog needs more than a compact pointer but less than an active external branch plan. During the AI-native taxonomy repair, the directory may temporarily retain source files whose filenames contain removed FAM labels while their content is being analyzed and folded into the correct existing owners. Those filenames are not active backlog identity and do not reserve future FAM numbers.
Codex reaches family vision through the Main-first loader chain: `Docs/Main.md` routes to `Docs/nexus_vision.md` for project-wide vision, then to the relevant family vision record, then to the active external branch plan for branch-local snapshots and implementation proof.

Docs Source-Truth Reform Model: Compact Pointer Layer.

Family vision records:

- preserve USER-accepted product direction and reusable design standards for a feature family
- keep future package boundaries visible without admitting implementation
- give Branch Readiness a stable vision owner to compare against before creating a Branch Vision Contract Snapshot
- receive reusable vision updates folded down from PR Readiness when they apply beyond one branch
- route detailed feature-category direction to USER-approved Family Feature Vision records when a family vision would become too broad or too crowded

Family vision records do not own:

- active branch authority
- active external branch implementation plans
- live Git, GitHub, release, PR, issue, worktree, or review state
- package/slice execution ledgers
- runtime implementation approval
- dependency work for another backlog family

Backlog family work stays local to its owning family/worktree. A family vision may cite cross-family context constraints, but it must not turn another backlog family or context owner into an implementation dependency queue.

## Family Feature Vision Layer

`Family Feature Vision` is the approved name for the durable middle vision layer between `Family Vision` and the active `Branch Vision Contract Snapshot`.

Do not use `Sub-Family Vision` as current terminology. That wording risks creating hierarchy drift under `FAM` identity and could make detailed feature categories look like new backlog families.

Family Feature Vision records are recommended under:

```text
Docs/family_feature_visions/
```

Recommended file naming:

```text
Docs/family_feature_visions/FAM-006_recording.md
Docs/family_feature_visions/FAM-006_hud_dashboard.md
Docs/family_feature_visions/FAM-006_overlay_profiles.md
Docs/family_feature_visions/FAM-006_monitor_groups.md
```

Creating the folder, creating the first content files, migrating existing family-vision text into those files, or treating any file as the active owner requires a separate USER approval. Until those files exist, `Docs/family_visions/` remains the durable family-level owner and active branch plans provide branch-local feature context.

BP1 entry for a selected feature-bearing branch route is blocked on `Family Feature Vision Required For Selected Feature` until the required USER-approved Family Feature Vision exists and passes the `Feature Vision Sufficiency Check`. If the branch route is governance-only, release-support, pure helper/validator, source-truth-only, or otherwise non-product, the branch planning packet may record `Family Feature Vision Not Applicable` with the reason.

`Feature Vision Sufficiency Check` requires enough durable content for BP1 to create a branch-specific vision without inventing feature direction: feature purpose, USER-facing surfaces, experience flow, included capabilities, explicit non-goals, dependency/deferred map, design options, proof expectations, Branch Readiness consumption notes, BP1 context notes, fold-down history when applicable, and active-state wording scan. A shallow, placeholder, copied-list-only, or branch-local implementation-only file does not satisfy BP1 entry.

When Family Feature Vision planning exposes durable feature ideas, deferrals, surfaces, proof expectations, grouping rules, or routing constraints, those items must be folded into the relevant vision owner before BP1 or given a durable deferred disposition. Repo vision files must preserve the planning without storing live branch state.

Family Feature Vision owns durable feature-category direction inside exactly one FAM:

- feature purpose
- USER-facing surfaces
- experience flow
- included capabilities
- explicit non-goals
- future feature candidates
- dependency/deferred map
- design options
- proof expectations
- Branch Readiness consumption notes
- BP1 context notes
- fold-down history

Family Feature Vision must not own:

- backlog family identity
- active branch status
- selected-next status
- PR status
- release-window status
- worktree assignment
- implementation approval
- live operational ledgers
- per-seam implementation checklists

Nested surfaces such as a Log Viewer inside a Recording feature stay inside the owning Family Feature Vision by default. Create another lower-level durable vision file only after a later `Source-Truth Placement Preflight` proves the single Family Feature Vision cannot preserve the detail safely and the USER approves a new owner.

## Deferred Feature Carryforward

Deferred Feature Carryforward is a durable planning-preservation section inside each Family Feature Vision. It preserves future feature ideas, dependency-bound items, and grouping recommendations without turning repo vision canon into active branch state.

Allowed durable dispositions:

- `Candidate`
- `Deferred Until Dependency`
- `Future Package Candidate`
- `Rejected`
- `Folded Into Branch Vision`
- `Implemented Receipt`
- `Superseded`

Each deferred item must record:

- deferred item title
- originating FAM
- originating feature vision
- origin branch or planning event
- originating gate
- feature surface
- description
- dependency trigger
- future grouping recommendation
- owner/worktree
- validation/proof expectation
- durable disposition
- fold-down receipt

Deferred Feature Carryforward must avoid active branch-state terms such as `active`, `current branch`, `selected next`, `pending PR`, `in progress`, `next branch`, or `release window status`. Those terms belong to BR2 output, active external branch planning, `C:\Nexus Governance State`, Git/GitHub/helper-derived truth, or USER decision packets.

## Owner Relationship

- Project-wide vision: `Docs/nexus_vision.md`
- Family-level vision: `Docs/family_visions/FAM-XXX_<slug>.md`
- Family Feature Vision: `Docs/family_feature_visions/FAM-XXX_<feature_slug>.md` after USER-approved content-file creation
- Active branch vision snapshot: `C:\Nexus Governance State\branches\<branch_slug>\branch_plan.md`
- Durable implementation/proof history: `Docs/workstreams/` records or structured branch receipts
- Compact family registry and pointers: `Docs/feature_backlog.md`

## Family Vision Index

| FAM ID | Family | Vision Record |
| --- | --- | --- |
| `FAM-001` | Boot Interface | `Docs/family_visions/FAM-001_boot_interface.md` |
| `FAM-002` | Desktop Interface | `Docs/family_visions/FAM-002_desktop_interface.md` |
| `FAM-003` | Interaction and Actions | `Docs/family_visions/FAM-003_interaction_and_actions.md` |
| `FAM-004` | Voice and Audio | `Docs/family_visions/FAM-004_voice_and_audio.md` |
| `FAM-005` | External Integrations | `Docs/family_visions/FAM-005_external_integrations.md` |
| `FAM-006` | Monitoring and HUD | `Docs/family_visions/FAM-006_monitoring_and_hud.md` |
| `FAM-007` | Local AI and Capability Packs | `Docs/family_visions/FAM-007_local_ai_and_capability_packs.md` |
| `FAM-008` | Packaging and Install Experience | `Docs/family_visions/FAM-008_packaging_and_install_experience.md` |

## Pending Fold-Source Files

These records are source material for no-loss folding before any deletion, rename, archive, or migration. They are not parseable backlog families, selected-next work, active package owners, independent worktree lanes, or FAM number reservations. Deleting or renaming them requires proof that their durable content has been folded into existing owner files and remains USER-reviewable.

| Source File | Fold Target |
| --- | --- |
| `Docs/family_visions/FAM-009_workspace_and_data.md` | Existing architecture, FAM-006/FAM-007/FAM-008 family visions, and AI runtime/trust architecture where workspace/data constraints apply |
| `Docs/family_visions/FAM-010_safety_and_privacy.md` | Existing FAM-003/FAM-005/FAM-006/FAM-007/FAM-008 family visions and AI runtime/trust architecture where safety/privacy constraints apply |

## Fold-Down Rule

PR Readiness may fold reusable branch vision updates into a family vision record only when the update is USER accepted, applies beyond the current branch, and does not duplicate branch-local implementation detail. Proposed or unresolved design ideas remain in the active external branch plan as UFD items, question queue entries, or future-package candidates until USER decides their final owner.

Use the `Vision Update Decision Matrix` in `Docs/phase_governance.md` before editing a family vision. Family vision records receive reusable USER-accepted family standards; they do not receive project-wide Nexus principles, branch-local implementation detail, proposed ideas, unresolved design questions, or live branch state.
