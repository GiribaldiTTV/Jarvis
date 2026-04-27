# FB-042 Desktop Startup Runtime Family Dossier

## Dossier Identity

- Family ID: `FB-042`
- Family Title: `Desktop startup runtime family anchor`
- Dossier Type: `Lifetime family dossier`
- Dossier State: `Structured shell with partial historical pass migration`
- Family Anchor: `Self`
- Backlog Anchor Record: `Docs/feature_backlog.md`
- Roadmap Anchor Section: `Docs/prebeta_roadmap.md`
- Historical Anchor Workstream Record: `Docs/workstreams/FB-042_desktop_entrypoint_runtime_refinement.md`
- Created By Seam: `Phase 4 - Lifetime Dossier Conversion / Slice R4-S1 - Convert the FB-042 dossier shell`

## Dossier Purpose

- This dossier is the additive lifetime traceability surface for the FB-042 runtime family anchor.
- It layers over the existing FB-042 historical workstream record instead of replacing or rewriting that record.
- Slice R4-S1 introduces only the shell structure required for later family-level migration and indexing.
- Slice R4-S3 adds pass index and slice/seam ledger templates without migrating historical family content into them yet.
- Slice R4-S4 adds validator/helper and artifact index templates without migrating historical family content into them yet.

## Current Dossier Status

- Historical Content Migration: `In progress`
- Alias Record Conversion Status: `FB-043 through FB-048 workstream records converted in Slice R5-S1`
- Pass Index Status: `Populated for FB-043 through FB-048 in Slice R5-S1`
- Slice / Seam Ledger Status: `Populated for FB-043 through FB-048 in Slice R5-S1`
- Validator / Helper Index Status: `Structure introduced in Slice R4-S4`
- Artifact Index Status: `Structure introduced in Slice R4-S4`
- Dossier Stability Validation Status: `Validated in Slice R4-S5`
- Last Structural Update: `2026-04-27 during Phase 5 / Slice R5-S1`

## Lifetime Tracking Scope

- family-anchor identity and routing
- historical proof aggregation across the FB-042 runtime family
- alias-to-anchor traceability without reopening independent selection truth
- future validator/helper and artifact indexes once later slices populate them
- no new implementation, release, or selected-next authority

## Historical Alias Coverage

- Family Alias IDs Preserved In Backlog: `FB-043`, `FB-044`, `FB-045`, `FB-046`, `FB-047`, `FB-048`
- Alias Preservation Rule: these remain historical aliases of `FB-042` in `Docs/feature_backlog.md` and are not independently selectable.
- Current Alias Record Migration State: FB-043 through FB-048 now keep their existing historical workstream narratives as explicit FB-042 historical pass records; corresponding branch-record conversion and future-selection cleanup remain later Phase 5 work.

## Historical Anchor Record

- Anchor Historical Workstream Record: `Docs/workstreams/FB-042_desktop_entrypoint_runtime_refinement.md`
- Anchor Historical Scope: released `v1.6.7-prebeta` desktop launch-path runtime refinement
- Current Relationship: the released FB-042 workstream remains the first historical proof under this family anchor and stays intact in R4-S1.

## Pass Index

Pass Index Status: `Populated for FB-043 through FB-048 in Slice R5-S1`
Pass Index Population State: `FB-043 through FB-048 historical pass rows migrated; additional family migration remains pending`

| Pass ID | Family Role | Source Record | Migration State | Notes |
| --- | --- | --- | --- | --- |
| `F042-P02` | `Historical pass alias` | `Docs/workstreams/FB-043_top_level_entrypoint_handoff_refinement.md` | `Converted in Slice R5-S1` | `Released in v1.6.8-prebeta; preserves the top-level entrypoint and explicit main.py handoff refinement chain.` |
| `F042-P03` | `Historical pass alias` | `Docs/workstreams/FB-044_boot_desktop_handoff_outcome_refinement.md` | `Converted in Slice R5-S1` | `Released in v1.6.9-prebeta; preserves the desktop-settled handoff outcome refinement chain.` |
| `F042-P04` | `Historical pass alias` | `Docs/workstreams/FB-045_active_session_relaunch_outcome_refinement.md` | `Converted in Slice R5-S1` | `Released in v1.6.9-prebeta; preserves the post-settled lifecycle classification follow-through for the same release package.` |
| `F042-P05` | `Historical pass alias` | `Docs/workstreams/FB-046_active_session_relaunch_reacquisition.md` | `Converted in Slice R5-S1` | `Released in v1.6.10-prebeta; preserves accepted relaunch reacquisition and replacement-session settled re-entry proof.` |
| `F042-P06` | `Historical pass alias` | `Docs/workstreams/FB-047_active_session_relaunch_decline_preservation.md` | `Converted in Slice R5-S1` | `Released in v1.6.11-prebeta; preserves decline-preservation and session-owner continuity proof.` |
| `F042-P07` | `Historical pass alias` | `Docs/workstreams/FB-048_active_session_relaunch_signal_failure_and_wait_timeout_truth.md` | `Converted in Slice R5-S1` | `Released in v1.6.12-prebeta; preserves accepted relaunch signal-failure and wait-timeout truth.` |

## Slice And Seam Ledger

Slice / Seam Ledger Status: `Populated for FB-043 through FB-048 in Slice R5-S1`
Ledger Population State: `Historical summary rows added for FB-043 through FB-048; deeper family migration remains pending`

| Phase / Slice | Seam / Scope | Classification | Migration State | Notes |
| --- | --- | --- | --- | --- |
| `FB-043 / WS-1, WS-2, H-1, LV-1, PR historical proof` | `Top-level entrypoint ownership and explicit main.py handoff refinement` | `Historical pass chain` | `Converted in Slice R5-S1` | `Detailed branch-local narrative stays in the preserved FB-043 workstream record.` |
| `FB-044 / WS-1, H-1, LV-1, PR historical proof` | `Desktop-settled handoff outcome refinement` | `Historical pass chain` | `Converted in Slice R5-S1` | `Released together with FB-045 in v1.6.9-prebeta; detailed narrative stays in the preserved FB-044 workstream record.` |
| `FB-045 / WS-1, H-1, LV-1, PR historical proof` | `Post-settled runtime stability follow-through` | `Historical pass chain` | `Converted in Slice R5-S1` | `Release-package relationship to FB-044 remains preserved in the workstream and backlog records.` |
| `FB-046 / WS-1, H-1, LV-1, PR, Release historical proof` | `Accepted relaunch reacquisition and replacement-session settled re-entry` | `Historical pass chain` | `Converted in Slice R5-S1` | `Preserves accepted relaunch ownership-transfer proof and release history.` |
| `FB-047 / WS-1, H-1, LV-1, PR, Release historical proof` | `Declined relaunch preserved-session truth` | `Historical pass chain` | `Converted in Slice R5-S1` | `Preserves repeated decline-owner continuity proof and successor relationship to FB-048.` |
| `FB-048 / WS-1, H-1, LV-1, PR, Release historical proof` | `Accepted relaunch signal-failure and wait-timeout truth` | `Historical pass chain` | `Converted in Slice R5-S1` | `Preserves failure/timeout truth, review-repair containment, and selected-next FB-049 lock.` |

## Validator And Helper Index

Validator / Helper Index Status: `Structure introduced in Slice R4-S4`
Validator / Helper Index Population State: `No historical validator or helper entries migrated yet`

| Surface | Classification | Source Record | Migration State | Notes |
| --- | --- | --- | --- | --- |
| `Placeholder only` | `Reserve rows for validator, helper, or harness history` | `Populate from existing historical workstream or branch records in later slices` | `Not started` | `R4-S4 adds shared validator/helper index structure only; no historical validator or helper entries migrate in this slice.` |

## Artifact Index

Artifact Index Status: `Structure introduced in Slice R4-S4`
Artifact Index Population State: `No historical artifact entries migrated yet`

| Artifact Path | Classification | Source Record | Migration State | Notes |
| --- | --- | --- | --- | --- |
| `Placeholder only` | `Reserve rows for reusable evidence, report, or helper artifacts` | `Populate from existing historical workstream or branch records in later slices` | `Not started` | `R4-S4 adds shared artifact index structure only; no historical artifact entries migrate in this slice.` |

## Migration Notes

- R4-S1 intentionally does not migrate historical narrative, proof logs, pass summaries, or alias record bodies into the dossier.
- R4-S3 introduces pass index and slice/seam ledger templates only; it does not migrate historical pass rows, ledger rows, proof logs, or alias record bodies into the dossier.
- R4-S4 introduces validator/helper and artifact index templates only; it does not migrate historical validator rows, helper rows, artifact rows, proof logs, or alias record bodies into the dossier.
- R4-S5 validates that the FB-042 dossier shell, routing, and index-template surfaces remain stable after the Phase 4 structural slices, and it does so without migrating historical rows or narrative content.
- R5-S1 converts FB-043 through FB-048 workstream records into explicit FB-042 historical pass records and populates family pass-index plus slice/seam summary rows without migrating full narrative, validator/helper, artifact, or branch-record bodies into the dossier itself.
- Later Phase 4 and Phase 5 slices will populate indexes and convert historical records incrementally.
- Until later migration lands, the existing workstream and alias records remain the authoritative detailed history.
