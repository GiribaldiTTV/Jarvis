# UI Reference Catalog

## Purpose

`Docs/ui_reference_catalog/` is the durable catalog for USER-promoted Nexus UI reference contracts.

The catalog exists so future branches can cite accepted reference contracts after USER-approved promotion instead of inferring a golden reference from candidate screenshots, helper output, Live Validation proof, or branch-local evidence.

## Source-Truth Boundary

FAM-002 owns reusable Desktop Interface presentation grammar in `Docs/family_visions/FAM-002_desktop_interface.md`.

`Docs/family_feature_visions/F2-FF01.md` owns the durable UI reference-system feature-category vision, missing-proof rows, deferred candidate preservation, and BR/BP1 context.

This catalog owns promoted reference records only after explicit USER promotion approval.

This catalog must not own candidate evidence, active proof ledgers, current screenshots or video inventories, issue state, PR state, release-window state, worktree adoption status, helper/validator pass state, or live operational UI drift rows.

Promotion may include known limitations when the USER explicitly accepts or waives the missing proof for source-truth reference purposes. A promoted-with-known-limitations record is binding as reference grammar, but it does not prove every consuming branch state, implement code-level shared primitives, or clear branch-specific visual proof obligations.

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

## Current Package Green Disposition

The 2026-06-17 Package A-E completion pass promoted six durable records:

- `UIREF-001` and `UIREF-002` clear Package A for top-level window and compact window-control reference grammar.
- `UIREF-003` clears Package B for baseline control-state and selector grammar.
- `UIREF-004` clears Package C for dialog, status, recovery, and doorway-surface grammar.
- `UIREF-005` clears Package D as a source-truth design-rule baseline while deferring code-level token/shared-primitive implementation.
- `UIREF-006` clears Package E as an enforcement contract while deferring helper, validator, and fixture code implementation.

These records do not mutate FAM worktrees, create runtime UI, create issues, implement shared primitives, or prove adoption in existing branches. Consuming branches must cite the applicable reference and still prove their own UI/UX implementation at their next legal gate.

## Empty-Catalog Safety

The catalog may exist with zero promoted references.

An empty catalog is a carrier and schema, not proof that any golden reference exists.
