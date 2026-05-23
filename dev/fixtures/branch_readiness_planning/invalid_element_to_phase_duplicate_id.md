# Fixture: Invalid Element-to-Phase Proof Matrix Duplicate ID

## Element-to-Phase Proof Matrix

Matrix Status: Accepted for Workstream Entry review before implementation begins.
USER Review Status: Pending - USER green-light pending; this fixture intentionally duplicates an element ID.
Open Element Questions: None - current element proof paths are mapped except the duplicate ID.
Element Coverage Owner: Docs/branch_plans/feature_fam_000_runtime_plan_fixture.md.
Element Validation Ledger Owner: Docs/branch_records/feature_fam_000_runtime_plan_fixture.md.

| Element ID | Element / Surface | Element Classification | Workstream Implementation Plan | Workstream Proof Plan | Hardening Proof Plan | Live Validation Proof / Waiver Plan | UTS / USER Acceptance Path | Future / Deferred Boundary | USER Decision State | Source Owner / Ledger Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ELEM-000-DUP | Provider readiness status surface | Planned | Workstream implements provider readiness status fields, desktop copy, and source-truth mapping in one admitted seam. | Workstream proof runs branch governance validation, provider-state fixtures, and static UI copy review. | Hardening compares implemented state, UI copy, validators, and source truth against the accepted branch plan. | Live Validation records static visible proof or an explicit waiver because provider execution remains disabled. | USER acceptance path uses a UTS prompt or USER waiver for disabled setup copy proof. | Current release element with no future boundary beyond execution remaining gated. | Accepted by USER for invalid fixture setup. | Active branch plan and Element Validation Ledger owner. |
| ELEM-000-DUP | Runtime warning copy surface | Planned | Workstream implements warning copy and source-truth mapping in a bounded implementation seam. | Workstream proof runs governance validation and static UI copy review after implementation. | Hardening compares warning copy, branch plan proof, and validator results against accepted scope. | Live Validation records screenshot proof or waiver for disabled runtime behavior. | USER acceptance path uses UTS review of warning copy or explicit waiver. | Current release element with no future boundary beyond execution remaining gated. | Accepted by USER for invalid fixture setup. | Active branch plan and Element Validation Ledger owner. |
