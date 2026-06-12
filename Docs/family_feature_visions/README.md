# Family Feature Visions

Family Feature Vision records are durable feature-category owners between broad Family Vision and branch-local Branch Vision snapshots.

This folder is repo source truth for approved Family Feature Vision structure and future USER-approved content files. It is not active branch state, not a live operational state store, not a selected-next tracker, not an active branch ledger, not a PR ledger, not a release-window ledger, and not a worktree assignment owner.

## Purpose

Family Feature Vision files preserve detail that is too specific for a broad Family Vision and too durable to live only in an active branch plan. They should help Branch Readiness, BP1, BP2, BP3, Workstream, Hardening, and Live Validation carry the same feature intent forward.

Family Feature Vision records own:

- durable feature-category purpose inside exactly one FAM
- user-facing surfaces and experience flow
- included capabilities and explicit non-goals
- durable feature element inventory
- Deferred Feature Carryforward facts
- design options and tradeoffs
- proof expectations
- Branch Readiness and BP1 consumption notes
- durable fold-down history when a branch promotes accepted feature-category facts

## Product Detail Quality Bar

A Family Feature Vision must contain enough durable product detail for BP1 to create a real branch vision without inventing feature direction from branch-local reasoning. It should describe the feature category outcome, user-visible surfaces, expected workflow, visual/interaction expectations, durable element inventory, design options, proof expectations, non-goals, deferred carryforward, and dependency triggers.

An FFV is not sufficient when it is only a branch route, Slice/SLC plan, seam plan, implementation package, copied-file list, placeholder, or explanation of what an FFV should do. Slices, SLCs, seams, and branch packages are engineering route details under the selected FFV; they are not the durable feature-category vision identity.

When FFV work discovers additional durable feature elements, deferred items, proof expectations, UI expectations, failure/recovery expectations, or cross-FAM dependency facts, the owning pass must record those facts in the FFV or the correct higher owner before BP1 proceeds, or must name the durable deferred disposition. Do not leave durable feature intent only in chat, helper output, generated USER packets, or active external state.

Family Feature Vision records must not own:

- active branch status
- selected-next truth
- current worktree assignment
- open PR state
- release-window status
- implementation approval
- live validation evidence ledgers
- temporary handoff state

## Identity

Family Feature Vision content files should use compact IDs:

- `F<family>-FF<two digits>.md`
- Example: `F7-FF01.md`

Durable elements inside a file should use:

- `F<family>-FF<two digits>-E<two digits>`
- Example: `F7-FF01-E03`

The file title and `Feature Category:` must name a durable product feature category. They must not be named after a branch route, Slice/SLC, seam, implementation package, selected-next posture, or temporary branch wording.

`Family Feature Vision`, `Feature Category`, and `Family Feature Vision Element` are the binding source-truth terms. `Sub-feature` may be used only as USER-friendly explanatory language for a durable feature category or element inside one FAM; it is not a separate canonical hierarchy, backlog identity, branch route, or worktree lane.

`Feature Category Vision` is allowed as a USER-facing alias for `Family Feature Vision` when readability helps review. It is not a rename migration, not a new file class, and not a replacement for the canonical `Family Feature Vision` / `FFV` term, compact ID pattern, validators, or owner paths.

`Docs/family_feature_visions/index.md` is a compact registry. It may name FFV IDs, parent FAMs, feature-category titles, file paths, registry dispositions, and compact notes. It must not carry branch gate state, selected-next state, active dependency queues, branch lifecycle status, PR state, release-window state, or worktree assignment.

## Deferred Feature Carryforward

Deferred Feature Carryforward preserves feature ideas, dependencies, grouping recommendations, and proof expectations without turning repo vision canon into active branch state.

Each deferred item should include:

- deferred item title
- origin planning event
- feature surface
- dependency trigger
- grouping recommendation
- proof expectation
- durable disposition

BR2 consumes this section dynamically. For each USER-selectable branch option, BR2 should report which deferred items apply, why the dependency trigger is satisfied, which items remain future-gated, why they remain future-gated, and how validation/proof changes if the option is selected.

## Cross-FAM Dependency Records

Family Feature Vision files may record durable cross-FAM dependency records when one feature category needs another family to expose a stable surface, contract, policy, proof route, or implementation capability.

A cross-FAM dependency record must identify the dependency ID, originating FAM, originating FFV or element, affected FAMs, affected FFV or element when known, scope class, required contract or capability, suggested grouping, proof expectation, durable disposition, fold-down target, and whether worktree-to-worktree mutation is approved.

Allowed dependency scope classes are `awareness`, `dependency-bounded`, `priority carry-in`, `platform contract`, `coordinated cross-FAM patch`, `repo-wide migration / halt`, and `transferred FAM work`.

The originating FAM may record the dependency and may implement bounded work inside its own legal carrier when its own feature category requires it. That record does not make the originating FAM the permanent owner of another FAM's feature category, does not authorize direct mutation of another active worktree, and does not create a live dependency queue in repo docs.

Affected FAMs consume the record through their own Branch Readiness path. When an affected FAM reaches BR1 or BR2 and the dependency applies to the selected feature category, the branch packet must either include the applicable dependency as a priority carry-in inside the coherent FFV package, future-gate it with reason, or route it to a USER decision when the dependency is too large or independent for the selected branch.

If the affected FAM has no matching Family Feature Vision yet, the dependency remains recorded at the Family Vision or originating FFV layer until the affected FAM admits the relevant FFV. The originating FAM must not create the affected FAM's FFV unless USER explicitly approves that content-file creation through the affected FAM or Governance source-truth carrier.

## UI Carrydown

When a Family Feature Vision contains user-visible UI, controls, windows, cards, HUDs, overlays, setup flows, status indicators, folder pickers, or evidence surfaces, it must reference the project-wide Project UI Vision in `Docs/nexus_vision.md`, the owning Family Vision's UI specialization, and FAM-002 presentation standards when the surface needs shared Desktop Interface guidance.

The consuming FAM still owns the feature behavior and feature-specific UI implementation; FAM-002 supplies reusable presentation law. The FFV should name the feature-specific control grammar, visual inheritance, surface classification, platform-native exceptions, USER-facing proof surfaces, and photo/video or manual-validation expectations without copying broad UI principles into a second owner.

For every visible window, panel, dialog, status surface, settings surface, or tray-opened surface in the feature category, the FFV should classify it as `Nexus-Owned Product Surface`, `Platform-Native Exception`, `Diagnostic / Developer Surface`, or `External Surface`. `Nexus-Owned Product Surface` items inherit NDAI/FAM-002 window chrome and component grammar by default. `Platform-Native Exception` items must explain why platform chrome is required and what proof keeps the exception from becoming accidental UI drift.

## Runtime Failure / Recovery Carrydown

When a Family Feature Vision contains launchable behavior, runtime behavior, user-facing commands, provider actions, recording/log actions, setup/update/repair paths, diagnostics panels, or failure-visible UI, it must consume the `Runtime Failure / Recovery Carrydown Gate` from `Docs/phase_governance.md`.

The FFV should classify applicable fatal launcher/runtime failure, recoverable action/launch failure, degraded-but-running state, blocked-by-policy state, disabled/deferred feature state, and unavailable-prerequisite state. It should name the USER-facing failure state, recovery option, fallback behavior, support/log/bundle behavior, privacy/safety boundary, photo/video or USER manual proof, owning FAM, and consumed FAM-001/FAM-002/FAM-006/FAM-007/FAM-008 rules.

FAM-001 owns fatal launcher/runtime diagnostics and future recovery-surface vision. FB-034 is historical released evidence for one bounded recoverable `launch_failed` class only. FAM-002 supplies presentation standards for visible diagnostics or failure panels. The consuming FAM owns feature-specific failure behavior. FFV files must preserve durable failure/recovery expectations without becoming live incident ledgers, current validation ledgers, support-bundle ledgers, or active failure queues.

## Visual Inheritance Matrix

When a Family Feature Vision creates or changes visible UI, BP2/BP3 and later proof should include a Visual Inheritance Matrix that names the surface classification, existing element or surface inherited from, owning UI rule, window chrome / frame treatment, shape/radius comparison, spacing/density comparison, typography comparison, card/row/divider treatment, color/shadow/glow treatment, hover/focus/disabled states, scroll/resize/transient-state proof, allowed exception or new grammar, proof artifact, and verdict.

`Helper green`, `marker PASS`, or `screenshot exists` is not a visual inheritance verdict. If no valid existing element exists, the branch must route the new grammar through USER acceptance before implementation or stop on the relevant visual inheritance blocker.

## Active-State Boundary

Family Feature Vision files may preserve durable planning facts. They must not use durable vision sections to maintain active branch, current worktree, selected-next, PR, or release-window state.

Active operational facts belong to Git, GitHub, approved helpers, USER decision packets, or `C:\Nexus Governance State` as routed by repo source truth.
