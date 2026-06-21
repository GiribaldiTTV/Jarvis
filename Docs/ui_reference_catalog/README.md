# UI Reference Catalog

## Purpose

`Docs/ui_reference_catalog/` is the durable catalog for USER-promoted Nexus UI reference contracts.

The catalog exists so future branches can cite accepted reference contracts after USER-approved promotion instead of inferring reusable reference, template, or primitive authority from candidate screenshots, helper output, Live Validation proof, or branch-local evidence.

## Source-Truth Boundary

FAM-002 owns reusable Desktop Interface presentation grammar in `Docs/family_visions/FAM-002_desktop_interface.md`.

`Docs/family_feature_visions/F2-FF01.md` owns the durable UI reference-system feature-category vision, missing-proof rows, deferred candidate preservation, and BR/BP1 context.

This catalog owns promoted reference records only after explicit USER promotion approval.

This catalog must not own candidate evidence, active proof ledgers, current screenshots or video inventories, issue state, PR state, release-window state, worktree adoption status, helper/validator pass state, or live operational UI drift rows.

Promotion may include known limitations when the USER explicitly accepts or waives the missing proof for source-truth reference purposes. A promoted-with-known-limitations record is binding as reference grammar, but it does not prove every consuming branch state, implement code-level shared primitives, or clear branch-specific visual proof obligations.

## Reference, Template, Primitive, And Comparative Synthesis Model

Nexus UI reuse has four distinct authority levels.

- `Accepted Reference`: a USER-promoted visual, behavior, or proof grammar record. It tells Codex what accepted output should resemble, but it is not reusable implementation code and does not prove a consuming branch adopted the grammar correctly.
- `Implementation Template`: a USER-approved scaffold or starting implementation with a named source path, applicability, required states, known limitations, and proof artifacts. A template may be copied or instantiated, but the consuming branch must still prove the result and classify any differences.
- `Shared Primitive`: reusable code, component, style token, helper, or runtime/UI module intended to produce identical-by-construction output across windows or families. A shared primitive must have an owner, source path, state coverage, proof coverage, migration/rollback posture, and USER-approved consumption rule before a branch may claim it exists.
- `Accepted Reference Set`: the set of applicable USER-accepted references for the same element class or product behavior. It may include UIREF records, FAM-002 grammar, AI Control Center where a UIREF names it as the strongest seed, and later USER-accepted windows or surfaces.
- `Comparative Synthesis`: the deterministic comparison step that identifies invariant traits across the Accepted Reference Set, feature-specific traits that may differ, conflicts or missing proof, and the required disposition for a new or repaired surface.

Codex must not collapse these levels. A UIREF record is not an Implementation Template by itself. A screenshot, branch packet, helper result, or attractive accepted window is not a Shared Primitive. A branch that says it "used the template" must name the actual template or primitive source. If no approved template or primitive exists, the branch must classify the work as `Reference-Derived Implementation` and prove element-by-element parity against the Accepted Reference Set.

Required implementation classification values:

- `Shared Primitive Consumed`
- `Implementation Template Instantiated`
- `Reference-Derived Implementation`
- `Accepted Reference Set Compared`
- `USER-Approved Exception`
- `Reference Gap`
- `Template Gap`
- `Shared Primitive Gap`
- `Source-Truth Gap`

Same-class element work should follow this order:

1. consume the approved Shared Primitive when one exists
2. instantiate the approved Implementation Template when no primitive exists
3. derive from the strongest applicable Accepted Reference Set when no template exists
4. stop on a gap or USER decision when references conflict, proof is insufficient, or the branch needs a product exception

Comparative Synthesis must not average styles, invent a new style by intuition, or treat a single screenshot as universal law. It must determine the element class, select applicable references, separate invariant traits from feature-specific traits, identify conflicts, and classify each mismatch as repair, exception, issue candidate, reference gap, template gap, shared primitive gap, source-truth gap, or USER waiver need.

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

Implementation Template records, when later admitted, must additionally include `Template Source Path`, `Instantiation Rule`, `Editable Regions`, `Non-Editable Visual / Behavior Invariants`, `Required State Matrix`, `Source-To-Visual Proof`, `Accessibility Proof`, `Backend / State Mapping`, `Migration / Rollback Guidance`, and `USER Template Acceptance Receipt`.

Shared Primitive records, when later admitted, must additionally include `Primitive Source Path`, `Owning Module`, `Public API / Props / Inputs`, `State Machine`, `Token / Style Source`, `Required Consumer Contract`, `Regression Proof`, `Version / Migration Policy`, and `USER Primitive Acceptance Receipt`.

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

Current implementation-template status: no catalog record currently promotes a reusable Implementation Template.

Current shared-primitive status: no catalog record currently promotes code-level Shared Primitives or design-token implementation.

Current comparative-reference status: UIREF-001 through UIREF-004 provide accepted reference grammar with known limitations. AI Control Center is the strongest accepted seed where the individual UIREF record names it, but it is not automatically a complete template or primitive.

## Empty-Catalog Safety

The catalog may exist with zero promoted references.

An empty catalog is a carrier and schema, not proof that any accepted reference, implementation template, or shared primitive exists.
