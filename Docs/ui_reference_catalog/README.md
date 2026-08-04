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

External Reference Candidate synchronization does not change this catalog boundary. Branch-owned candidate proposals may live as evidence under `D:\Nexus Desktop AI Data\Governance State\branches\<branch_slug>\reference_candidates\...`, and generated aggregate/collision reports may summarize those proposals under `D:\Nexus Desktop AI Data\Governance State\reference_standards\...` after the current workflow admits that external evidence. Those external records are not promoted UIREF records, are not accepted references, are not implementation templates, are not shared primitives, and do not override this catalog. A candidate becomes catalog source truth only when a USER-approved Governance source-truth update adds or updates the relevant repo catalog record and index.

## General Reference Standard Relationship

UIREF is the first domain implementation of the broader Nexus Reference Standard lifecycle. A Reference Standard is a USER-promoted durable comparator for a class of product behavior, UI, UX, runtime/backend behavior, proof, privacy, recovery, trust, or other repeated product/governance need. This folder remains UI-only until source truth admits another reference family. New non-UI reference families must not be created by naming inertia, branch-local evidence, or Codex recommendation alone; they require repeated evidence, a clear source-truth owner, a USER-reviewed promotion packet, adoption rules, known limitations, and a branch/RAR carrydown path.

Reference Standard lifecycle: `Candidate -> USER Review -> Promoted Reference -> Consumed By Branch -> Effectiveness Reviewed -> Updated / Superseded / Deferred`.

Candidate synchronization lifecycle: `Branch Candidate Proposal -> External Candidate Sync -> Collision Review When Needed -> USER Review / Promotion Packet -> Repo Catalog Update -> Consuming Branch Rebaseline / RAR`. External sync is a visibility step, not a promotion step.

PR Readiness Stage 1 is the normal fold-down checkpoint for reference effectiveness. If an accepted reference produced repeated same-class repair cycles, unresolved exceptions, USER visual correction, or evidence that the reference failed to guide implementation, PR Readiness must record a Reference Standard Repair Candidate, supersession candidate, or deferred future carrier instead of treating the branch result as proof that the standard was sufficient.

## Reference, Template, Primitive, And Comparative Synthesis Model

Nexus UI reuse has five distinct model terms. `Accepted Reference` is reusable reference authority. `Implementation Template` and `Shared Primitive` are reusable implementation authority levels. `Accepted Reference Set` and `Comparative Synthesis` are comparison/proof structures that determine how those authorities apply to a specific branch surface.

- `Accepted Reference`: a USER-promoted visual, behavior, or proof grammar record. It tells Codex what accepted output should resemble, but it is not reusable implementation code and does not prove a consuming branch adopted the grammar correctly.
- `Implementation Template`: a USER-approved scaffold or starting implementation with a named source path, applicability, required states, known limitations, and proof artifacts. A template may be copied or instantiated, but the consuming branch must still prove the result and classify any differences.
- `Shared Primitive`: reusable code, component, style token, helper, or runtime/UI module intended to produce identical-by-construction output across windows or families. A shared primitive must have an owner, source path, state coverage, proof coverage, migration/rollback posture, and USER-approved consumption rule before a branch may claim it exists.
- `Accepted Reference Set`: the set of applicable USER-accepted references for the same element class or product behavior. It may include UIREF records, FAM-002 grammar, AI Control Center where a UIREF names it as the strongest seed, and later USER-accepted windows or surfaces.
- `Comparative Synthesis`: the deterministic comparison step that identifies invariant traits across the Accepted Reference Set, feature-specific traits that may differ, conflicts or missing proof, and the required disposition for a new or repaired surface.

Codex must not collapse these terms. A UIREF record is not an Implementation Template by itself. A screenshot, branch packet, helper result, or attractive accepted window is not a Shared Primitive. A branch that says it "used the template" must name the actual template or primitive source. If no approved template or primitive exists, the branch must classify the work as `Reference-Derived Implementation` and prove element-by-element parity against the Accepted Reference Set.

Required `Implementation Authority Classification:` values:

- `Shared Primitive Consumed`
- `Implementation Template Instantiated`
- `Reference-Derived Implementation`
- `One-Off Implementation`
- `USER-Approved Exception`
- `Reference Gap`
- `Template Gap`
- `Shared Primitive Gap`
- `Source-Truth Gap`

`Accepted Reference Set Compared` is not an implementation-authority classification. It is a comparative-synthesis / proof disposition that may appear in accepted-reference or visual-family proof rows after the branch names the implementation authority. When no approved template or primitive exists and the branch compares against the accepted reference set, the implementation-authority value is `Reference-Derived Implementation`.

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
- `Window Geometry / Resize`
- `Proof / Review Surface`
- `Platform-Native Exception`

## Promotion Rule

A reference is not promoted until a USER-approved promotion packet records the required schema fields, visual proof or USER waiver, source evidence, applicability, known limitations, and final disposition.

Candidate evidence may be cited from USER review packets, branch proof, screenshots, videos, helper output, or Codex digests, but it remains evidence only until a promoted reference record exists in this catalog.

Candidate evidence may also be cited from admitted external reference-candidate records or generated collision reports. The citing branch must still say whether an applicable promoted reference exists, whether the candidate conflicts with another candidate, whether the candidate is branch-local or reusable, and whether USER promotion, variant approval, supersession, rejection, or deferment is needed. A consuming branch must not call the candidate canon while waiting for that decision.

## Current Package Green Disposition

The 2026-06-17 Package A-E completion pass promoted six durable records, and the 2026-06-25 Window Geometry / Resize intake promoted one additional source-truth geometry contract:

- `UIREF-001` and `UIREF-002` clear Package A for top-level window and compact window-control reference grammar.
- `UIREF-003` clears Package B for baseline control-state and selector grammar.
- `UIREF-004` clears Package C for dialog, status, recovery, and doorway-surface grammar.
- `UIREF-005` clears Package D as a source-truth design-rule baseline while deferring code-level token/shared-primitive implementation.
- `UIREF-006` clears Package E as an enforcement contract while deferring helper, validator, and fixture code implementation.
- `UIREF-007` records the Nexus Window Geometry And Resize Contract for min/default/max/fullscreen policy, breakpoint/reflow behavior, DPI/multi-monitor posture, geometry proof, and per-FAM carrydown while deferring product adoption to consuming FAM worktrees.

These records do not mutate FAM worktrees, create runtime UI, create issues, implement shared primitives, or prove adoption in existing branches. Consuming branches must cite the applicable reference and still prove their own UI/UX implementation at their next legal gate.

Current implementation-template status: no catalog record currently promotes a reusable Implementation Template.

Current shared-primitive status: no catalog record currently promotes code-level Shared Primitives or design-token implementation.

Current comparative-reference status: UIREF-001 through UIREF-004 and UIREF-007 provide accepted reference grammar with known limitations. AI Control Center is the strongest accepted compact top-level seed where the individual UIREF record names it, but it is not automatically a complete template or primitive. FAM-006 HUD Dashboard remains comparison/adoption-target evidence for dashboard / parent-class geometry where UIREF-007 says it applies.

## Empty-Catalog Safety

The catalog may exist with zero promoted references.

An empty catalog is a carrier and schema, not proof that any accepted reference, implementation template, or shared primitive exists.
