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

## Active-State Boundary

Family Feature Vision files may preserve durable planning facts. They must not use durable vision sections to maintain active branch, current worktree, selected-next, PR, or release-window state.

Active operational facts belong to Git, GitHub, approved helpers, USER decision packets, or `C:\Nexus Governance State` as routed by repo source truth.
