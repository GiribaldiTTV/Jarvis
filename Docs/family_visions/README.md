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
- implementation responsibility for another backlog family

Backlog family work stays local to its owning family/worktree. A family vision may preserve durable cross-family dependency candidates, constraints, platform-contract implications, and future carry-in context, but it must not turn another backlog family or context owner into an active implementation dependency queue.

## Vision Carrydown And UI Specialization

Family Vision records consume `Docs/nexus_vision.md` first. They specialize the project-wide product direction and Project UI Vision for one broad FAM without copying the whole project vision into each file.

Family-level UI specialization should name the FAM-specific visual system, interaction model, proof expectations, and safety/recovery posture that branches in that family must inherit. It should not duplicate branch-local layouts, per-seam checklists, current validation status, or temporary USER review packet text.

FAM-002 is the shared Desktop Interface presentation authority. Other FAMs normally consume FAM-002 presentation standards while retaining ownership of their own feature behavior, feature-specific UI implementation, and proof path. A dedicated FAM-002 branch is the exception path and requires USER admission of a concrete Desktop Interface feature category that no consuming FAM owns.

Family Feature Vision records consume both the Project Vision and the owning Family Vision. They specialize only the durable feature-category layer: feature purpose, surfaces, experience flow, included capabilities, non-goals, durable elements, deferred carryforward, design options, and proof expectations. They should reference the higher-level UI and proof rules, then add the feature-specific details needed for BP1, BP2, BP3, Workstream, Hardening, and Live Validation.

If Family Feature Vision planning discovers new durable UI rules, feature ideas, deferred items, dependency triggers, or proof expectations, the owning pass must fold those facts into the correct durable vision owner or record a durable deferred disposition before BP1 proceeds. Do not leave them only in chat, helper output, a USER packet, active external branch planning, or a branch-local digest.

## Family Feature Vision Layer

`Family Feature Vision` is the approved name for the durable middle vision layer between `Family Vision` and the active `Branch Vision Contract Snapshot`.

Do not use `Sub-Family Vision` as current terminology. That wording risks creating hierarchy drift under `FAM` identity and could make detailed feature categories look like new backlog families.

`Feature Category Vision` is a USER-facing alias for `Family Feature Vision` only. It may improve review readability, but it does not rename the source-truth layer, create another hierarchy, or change the canonical FFV file/ID rules.

Family Feature Vision records are recommended under:

```text
Docs/family_feature_visions/
```

Recommended file naming:

```text
Docs/family_feature_visions/index.md
Docs/family_feature_visions/F6-FF01.md
Docs/family_feature_visions/F6-FF02.md
Docs/family_feature_visions/F7-FF01.md
```

Compact aliases use `F<number>` for the owning FAM without leading zeroes: `FAM-006` becomes `F6`, `FAM-007` becomes `F7`, and `FAM-008` becomes `F8`. Family Feature Vision IDs use `F<family>-FF<two digits>`, and durable feature elements inside the file use `F<family>-FF<two digits>-E<two digits>`. Example: `F7-FF01-E03` is the third durable element in the first FAM-007 Family Feature Vision.

`Docs/family_feature_visions/index.md`, once USER-approved and created, owns the compact FFV registry. It maps each compact FFV ID to the family, human-readable category title, file path, source owner, and durable status. The index is a compact registry only; it must not record selected-next truth, active branch status, gate status, PR state, release-window state, or worktree assignment. Until that index exists, this README owns the compact ID rule, and existing FFV filenames are transition aliases that must be normalized by the owning branch when USER approves FFV content mutation.

Family Feature Vision filenames should be compact IDs. Human-readable category names live in the file title and the index. The FFV title and `Feature Category` must name a durable product feature category, not a branch route, Slice/SLC, seam, current implementation package, or temporary branch wording. A branch may select a route such as a "three-NDAI assisted desktop AI" implementation package inside a category, but the FFV identity itself must stay category-level.

Creating the folder, creating the first content files, renaming existing FFV files, migrating existing family-vision text into those files, updating branch/external-state pointers to new FFV names, or treating any file as the active owner requires a separate USER approval unless the current approved branch explicitly includes FFV content-file mutation. Until those files exist or are repaired, `Docs/family_visions/` remains the durable family-level owner and active branch plans provide branch-local feature context.

Every FFV creation, rename, or repair pass must inventory all currently tracked `Docs/family_feature_visions/*.md` files in the owning worktree. The pass must classify each file as `Valid Category-Level FFV`, `Rename / Reframe Required`, `Compact ID Missing`, `Pointer Migration Required`, `Live-State Wording Repair Required`, `Historical Transition Alias`, or `USER Decision Required`. When approval covers FFV content mutation, all affected FFVs in that worktree must be repaired or explicitly deferred with a named blocker before BP1 proceeds. Leaving stale branch-record, branch-plan, external-state, USER packet, backlog, roadmap, or source-truth pointers to old FFV names blocks on `Family Feature Vision Pointer Migration Missing`.

BP1 entry for a selected feature-bearing branch route is blocked on `Family Feature Vision Required For Selected Feature` until the required USER-approved Family Feature Vision exists and passes the `Feature Vision Sufficiency Check`. If the branch route is governance-only, release-support, pure helper/validator, source-truth-only, or otherwise non-product, the branch planning packet may record `Family Feature Vision Not Applicable` with the reason.

`Feature Vision Sufficiency Check` requires enough durable content for BP1 to create a branch-specific vision without inventing feature direction: stable FFV ID or approved transition alias, parent FAM, human-readable category title, category-level purpose, USER-facing surfaces, experience flow, included capabilities, explicit non-goals, durable feature element inventory, dependency/deferred map, design options, proof expectations, Branch Readiness consumption notes, BP1 context notes, fold-down history when applicable, category-scope scan, pointer-migration scan, and active-state wording scan. A shallow, placeholder, copied-list-only, branch-route-specific, Slice/SLC-specific, seam-specific, or branch-local implementation-only file does not satisfy BP1 entry.

When Family Feature Vision planning exposes durable feature ideas, deferrals, surfaces, proof expectations, grouping rules, or routing constraints, those items must be folded into the relevant vision owner before BP1 or given a durable deferred disposition. Repo vision files must preserve the planning without storing live branch state.

Family Feature Vision owns durable feature-category direction inside exactly one FAM:

- stable FFV ID or approved transition alias
- parent FAM
- human-readable category title
- feature purpose
- USER-facing surfaces
- experience flow
- included capabilities
- explicit non-goals
- durable feature element inventory with element IDs
- future feature candidates
- dependency/deferred map
- design options
- proof expectations
- Branch Readiness consumption notes
- BP1 context notes
- fold-down history

Runtime observability carrydown: when a Family Feature Vision contains runtime, desktop, user-facing, file/folder, launcher, bridge, Dev Toolkit, recording, or validation-critical behavior, it must reference the project-wide Runtime Observability and USER Proof direction in `Docs/nexus_vision.md` and specialize only what is feature-specific. It should name expected exact-launcher proof, photo/video proof, manual USER validation needs, user-visible storage/folder boundaries, troubleshooting-mode relevance, and proof expectations without becoming an active Live Validation evidence ledger.

UI carrydown: when a Family Feature Vision contains user-visible UI, controls, windows, cards, HUDs, overlays, setup flows, status indicators, folder pickers, or evidence surfaces, it must reference the project-wide Project UI Vision in `Docs/nexus_vision.md`, the owning Family Vision's UI specialization, and FAM-002 presentation standards when the surface needs shared Desktop Interface guidance. The consuming FAM still owns the feature behavior and feature-specific UI implementation; FAM-002 supplies reusable presentation law. The FFV should then name the feature-specific control grammar, visual inheritance, allowed exceptions, USER-facing proof surfaces, and photo/video or manual-validation expectations without copying broad UI principles into a second owner.

Family Feature Vision must not own:

- backlog family identity
- branch route identity
- Slice/SLC identity
- seam identity
- branch-local implementation sequence
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

- element ID when the deferred item is also a durable feature element
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

Deferred carryforward may preserve durable planning facts even when the implementation is future-gated. It must not become a live dependency ledger. BR2, BP1, BP2, BP3, Workstream, Hardening, and Live Validation dynamically select, map, prove, defer, or block the durable FFV elements; the FFV itself owns only the durable visioned inventory, deferred facts, proof expectations, and fold-down receipts.

## Cross-FAM Dependency Candidates

Cross-FAM Dependency Candidates preserve durable dependency facts discovered by an originating FAM without authorizing cross-worktree mutation, creating another FAM's missing Family Feature Vision, or turning repo vision canon into active branch state.

The originating FAM should record dependency candidates when its Family Vision, Family Feature Vision, BR1, BR2, BP1, BP2, BP3, Workstream, Hardening, Live Validation, or PR Readiness evidence discovers that another FAM may need future adoption, compatibility work, proof, or feature-specific follow-through. The affected FAM owns its own later FFV creation, FFV repair, branch selection, implementation, and feature-specific adoption unless the current branch receives explicit USER approval for dependency-bounded cross-FAM work.

When the affected FFV exists, record the dependency against the affected FFV and element ID. When the affected FFV does not exist, record the dependency at affected-FAM level as a durable dependency candidate and mark the affected FFV / element as `Not Created`. The originating FAM must not create, rename, or fully design the affected FAM's missing FFV unless USER approves a bounded FFV content-file carrier for that work.

Each cross-FAM dependency candidate should use the marker shape validated by the Branch Readiness planning fixture helper:

- `Cross-FAM Dependency Map:`
- `Dependency ID:`
- `Originating FAM:`
- `Originating FFV / Element:`
- `Affected FAMs:`
- `Affected FFV / Element or Not Created:`
- `Dependency Scope Class:`
- `Carry-In / Deferral / Transfer Decision:`
- `Required Contract / Capability:`
- `Suggested Grouping:`
- `Proof Expectation:`
- `Durable Disposition:`
- `Affected FAM Receipt / Fold-Down Target:`
- `Worktree-To-Worktree Mutation:`

Allowed `Dependency Scope Class:` values:

- `Awareness Only`
- `Compatibility Default`
- `Future Adoption`
- `Priority Carry-In`
- `Platform Contract`
- `Dependency-Bounded Cross-FAM Work`
- `Coordinated Cross-FAM Patch`
- `Repo-Wide Migration / Halt`
- `Transferred FAM Work`

Allowed durable dispositions:

- `Candidate`
- `Mapped To FFV`
- `Future Carry-In`
- `Implemented Receipt`
- `Rejected`
- `Superseded`

Dependency candidates must avoid active branch-state terms such as `active`, `current branch`, `selected next`, `pending PR`, `in progress`, `next branch`, or `release window status`. Those terms belong to BR2 output, active external branch planning, `C:\Nexus Governance State`, Git/GitHub/helper-derived truth, or USER decision packets.

`Priority Carry-In, Not Scope Capture`: when a cross-FAM contract creates required work for an affected FAM, that work must be evaluated by the affected FAM's next BR1, but it does not automatically become the only branch objective. The affected FAM should group the carry-in into the relevant FFV or coherent package when practical, and split only when source truth proves the carry-in cannot safely share the branch package.

`Implementation Ownership Split`: the branch that introduces a dependency owns the introduced contract, compatibility default, and proof that existing affected families are not broken. The affected FAM owns later feature-specific adoption, FFV creation or repair, polish, expansion, and user-facing follow-through inside its own normal Branch Readiness path.

## Owner Relationship

- Project-wide vision: `Docs/nexus_vision.md`
- Family-level vision: `Docs/family_visions/FAM-XXX_<slug>.md`
- Family Feature Vision index and compact aliases: `Docs/family_feature_visions/index.md` after USER-approved index creation
- Family Feature Vision content: `Docs/family_feature_visions/F<family>-FF<two digits>.md` after USER-approved content-file creation
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
