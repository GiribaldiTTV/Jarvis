# FB-042 Desktop Startup Runtime Family Dossier

## Dossier Identity

- Family ID: `FB-042`
- Family Title: `Desktop startup runtime family anchor`
- Dossier Type: `Lifetime family dossier`
- Dossier State: `Shell only`
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

- Historical Content Migration: `Not started`
- Alias Record Conversion Status: `Not started`
- Pass Index Status: `Structure introduced in Slice R4-S3`
- Slice / Seam Ledger Status: `Structure introduced in Slice R4-S3`
- Validator / Helper Index Status: `Structure introduced in Slice R4-S4`
- Artifact Index Status: `Structure introduced in Slice R4-S4`
- Dossier Stability Validation Status: `Validated in Slice R4-S5`
- Last Structural Update: `2026-04-27 during Phase 4 / Slice R4-S4`

## Lifetime Tracking Scope

- family-anchor identity and routing
- historical proof aggregation across the FB-042 runtime family
- alias-to-anchor traceability without reopening independent selection truth
- future validator/helper and artifact indexes once later slices populate them
- no new implementation, release, or selected-next authority

## Historical Alias Coverage

- Family Alias IDs Preserved In Backlog: `FB-043`, `FB-044`, `FB-045`, `FB-046`, `FB-047`, `FB-048`
- Alias Preservation Rule: these remain historical aliases of `FB-042` in `Docs/feature_backlog.md` and are not independently selectable.
- Current Alias Record Migration State: each alias still keeps its existing historical workstream record; no alias content moved into this dossier in R4-S1.

## Historical Anchor Record

- Anchor Historical Workstream Record: `Docs/workstreams/FB-042_desktop_entrypoint_runtime_refinement.md`
- Anchor Historical Scope: released `v1.6.7-prebeta` desktop launch-path runtime refinement
- Current Relationship: the released FB-042 workstream remains the first historical proof under this family anchor and stays intact in R4-S1.

## Pass Index

Pass Index Status: `Structure introduced in Slice R4-S3`
Pass Index Population State: `No historical pass entries migrated yet`

| Pass ID | Family Role | Source Record | Migration State | Notes |
| --- | --- | --- | --- | --- |
| `Placeholder only` | `Reserve rows for anchor or alias pass history` | `Populate from existing historical workstream records in later slices` | `Not started` | `R4-S3 adds shared pass-index structure only; no historical pass data migrates in this slice.` |

## Slice And Seam Ledger

Slice / Seam Ledger Status: `Structure introduced in Slice R4-S3`
Ledger Population State: `No historical slice or seam entries migrated yet`

| Phase / Slice | Seam / Scope | Classification | Migration State | Notes |
| --- | --- | --- | --- | --- |
| `Placeholder only` | `Reserve rows for future converted seams` | `Anchor or alias family history` | `Not started` | `R4-S3 adds shared ledger structure only; no historical slice or seam data migrates in this slice.` |

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
- Later Phase 4 and Phase 5 slices will populate indexes and convert historical records incrementally.
- Until later migration lands, the existing workstream and alias records remain the authoritative detailed history.
