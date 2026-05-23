# Family Vision Records

## Purpose

`Docs/family_visions/` owns durable product-direction records for broad Nexus feature families when the backlog needs more than a compact pointer but less than an active branch plan.

Docs Source-Truth Reform Model: Compact Pointer Layer.

Family vision records:

- preserve USER-accepted product direction and reusable design standards for a feature family
- keep future package boundaries visible without admitting implementation
- give Branch Readiness a stable vision owner to compare against before creating a Branch Vision Contract Snapshot
- receive reusable vision updates folded down from PR Readiness when they apply beyond one branch

Family vision records do not own:

- active branch authority
- active branch implementation plans
- live Git, GitHub, release, PR, issue, worktree, or review state
- package/slice execution ledgers
- runtime implementation approval

## Owner Relationship

- Project-wide vision: `Docs/nexus_vision.md`
- Family-level vision: `Docs/family_visions/FAM-XXX_<slug>.md`
- Active branch vision snapshot: `Docs/branch_plans/<branch_slug>.md`
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
| `FAM-009` | Workspace and Data | `Docs/family_visions/FAM-009_workspace_and_data.md` |
| `FAM-010` | Safety and Privacy | `Docs/family_visions/FAM-010_safety_and_privacy.md` |

## Fold-Down Rule

PR Readiness may fold reusable branch vision updates into a family vision record only when the update is USER accepted, applies beyond the current branch, and does not duplicate branch-local implementation detail. Proposed or unresolved design ideas remain in the active branch plan as UFD items, question queue entries, or future-package candidates until USER decides their final owner.
