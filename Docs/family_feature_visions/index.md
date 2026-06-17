# Family Feature Vision Index

This index is a compact durable registry for USER-approved Family Feature Vision content files. It names durable feature-category records and points to their files; it does not own selected-next state, active branch status, BP gate state, PR state, release-window state, worktree assignment, active dependency queues, or implementation ledgers.

Future content files should use compact IDs such as `F<family>-FF<two digits>` and durable element IDs such as `F<family>-FF<two digits>-E<two digits>`.

Binding terms are `Family Feature Vision`, `Feature Category`, and `Family Feature Vision Element`. `Sub-feature` is USER-friendly shorthand only and must not become a new source-truth hierarchy.

| FFV ID | Parent FAM | Feature Category | File | Registry Disposition | Notes |
| --- | --- | --- | --- | --- | --- |
| `F2-FF01` | `FAM-002` | Nexus UI Reference System | `Docs/family_feature_visions/F2-FF01.md` | USER-approved durable planning | Source-truth carrier for UI reference-system vision, missing-proof rows, promotion criteria, and catalog relationship; no references are promoted by this index row. |
| `F3-FF01` | `FAM-003` | Nexus Resident Access And Quick Actions | `Docs/family_feature_visions/F3-FF01.md` | USER-approved durable planning | Resident tray doorway, compact quick-access menu, privacy-visible status fallback, and cross-family surface routing. |
