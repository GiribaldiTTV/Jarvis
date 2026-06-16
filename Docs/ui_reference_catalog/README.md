# UI Reference Catalog

## Purpose

`Docs/ui_reference_catalog/` is the durable catalog for USER-promoted Nexus UI reference contracts.

The catalog exists so future branches can cite accepted reference contracts after USER-approved promotion instead of inferring a golden reference from candidate screenshots, helper output, Live Validation proof, or branch-local evidence.

## Source-Truth Boundary

FAM-002 owns reusable Desktop Interface presentation grammar in `Docs/family_visions/FAM-002_desktop_interface.md`.

`Docs/family_feature_visions/F2-FF01.md` owns the durable UI reference-system feature-category vision, missing-proof rows, deferred candidate preservation, and BR/BP1 context.

This catalog owns promoted reference records only after explicit USER promotion approval.

This catalog must not own candidate evidence, active proof ledgers, current screenshots or video inventories, issue state, PR state, release-window state, worktree adoption status, helper/validator pass state, or live operational UI drift rows.

## Reference Record Schema

Each promoted reference record must include:

- Reference ID
- Reference Name
- Reference Class
- Owning Vision Layer
- Source Evidence
- USER Acceptance Receipt
- Applicable Surface Classes
- Non-Applicable Surface Classes
- Required Element Groups
- Required States
- Geometry / Resize / Accessibility Expectations
- Proof Artifacts
- Known Limitations
- Adoption Rule
- Validator / Helper Guidance
- Promotion Result
- Final Disposition

## Reference Classes

Allowed reference classes:

- `Top-Level Window`
- `Child / Modal / Dialog`
- `Window Control Cluster`
- `Button / Control State`
- `Dropdown / Menu / List / Filter`
- `Card / Row / Divider`
- `Status / Failure / Recovery Panel`
- `Tray / Doorway Surface`
- `Proof / Review Surface`
- `Platform-Native Exception`

## Promotion Rule

A reference is not promoted until a USER-approved promotion packet records the required schema fields, visual proof or USER waiver, source evidence, applicability, known limitations, and final disposition.

Candidate evidence may be cited from USER review packets, branch proof, screenshots, videos, helper output, or Codex digests, but it remains evidence only until a promoted reference record exists in this catalog.

## Empty-Catalog Safety

The catalog may exist with zero promoted references.

An empty catalog is a carrier and schema, not proof that any golden reference exists.
