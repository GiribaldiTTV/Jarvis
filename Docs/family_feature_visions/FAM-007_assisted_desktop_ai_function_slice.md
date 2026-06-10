# F7-FF01 Public-Safe Assisted Desktop AI Interaction And Edition Boundary

## FFV Identity

FFV ID: `F7-FF01`

FFV Category: `Public-Safe Assisted Desktop AI Interaction And Edition Boundary`

Transition Alias Path: `Docs/family_feature_visions/FAM-007_assisted_desktop_ai_function_slice.md`

Preferred Future Compact Path: `Docs/family_feature_visions/F7-FF01.md`

Path Disposition: `Retained as the USER-approved transition alias for this BR2 repair; a later rename may move this record to the preferred compact path only with full pointer migration.`

Parent Family: `FAM-007 Local AI and Capability Packs`

Package Context: `PKG-007`

Durable Category Scope: `Public-safe local assisted AI interaction, no-provider result behavior, provider-visible-data explanation, capability-pack eligibility display, blocked install intent, and Public / Developer / Owner lane boundary presentation before provider/model execution or private setup exists.`

## Ownership Boundary

This Family Feature Vision owns durable feature-category direction inside FAM-007. It supplies BP1 Feature Vision Context and durable FFV element IDs for branch planning.

It owns:

- compact FFV identity and category title
- durable user value and product purpose
- expected public-safe surfaces and flows
- durable element inventory
- deferred feature carryforward facts
- boundary and proof expectations
- branch-planning guidance for selected/deferred FFV elements

It does not own:

- branch route identity
- Slice, SLC, or seam identity
- active branch state
- selected-next operational authority
- BP gate acceptance
- Workstream implementation approval
- live validation status
- provider/model execution approval
- private Developer or Owner setup
- capability-pack download or install execution
- runtime cache, memory, learning, indexing, or personalization

## Vision Basis

Source-truth basis:

- `Docs/nexus_vision.md`
- `Docs/feature_backlog.md`
- `Docs/family_visions/FAM-007_local_ai_and_capability_packs.md`
- `Docs/family_visions/FAM-007_ai_edition_capability_trust_boundary_release_plan.md`
- `Docs/ai_runtime_and_trust_architecture.md`
- `Docs/family_visions/FAM-008_packaging_and_install_experience.md`
- `Docs/phase_governance.md`
- `Docs/branch_plans/README.md`

FAM-007 direction requires the base app to remain useful without a local LLM. Assisted Desktop Mode and no-provider behavior should be understandable before any real provider execution. Provider-visible data, provider state, capability-pack eligibility, and edition boundaries must be visible and truthful without activating hidden network, prompt, model, download, memory, or private-edition behavior.

## Feature Purpose

The user-facing purpose is to make ORIN's AI posture visible, useful, and honest in the Public Edition before a provider or local model is connected.

The durable product target is not "make the provider work." The target is a public-safe assisted interaction layer that can say what Nexus can do locally, why provider execution is unavailable, what data would be visible to a provider, and which future capability or edition gates remain blocked.

## Category Boundary

This FFV category is broader than one branch route. It covers the public-safe assisted desktop interaction and edition-boundary pattern for FAM-007.

The branch route label `Three-NDAI Assisted Desktop AI Function Slice` is a selected grouped implementation route that may consume a subset of this FFV's elements. It is not the FFV category title and must not turn this FFV into a branch plan or live-state ledger.

## User-Facing Surfaces

- ORIN / AI status surface in the desktop visual layer.
- Local assisted action entrypoint tied to that status surface.
- Deterministic result view for no-provider operation.
- Plain-language provider-visible data display.
- Capability-pack eligibility and blocked install-intent display.
- Public Edition, Developer lane, and Owner lane boundary presentation.

## Durable Experience Flow

1. The user sees an AI / ORIN status surface rather than a hidden or inert provider block.
2. The user activates a local assisted action.
3. Nexus reads only public-safe local app state and provider-boundary state.
4. The result explains that provider execution is unavailable or disabled.
5. The result states provider-visible data as `none` when no prompt/provider path ran.
6. The result names useful local follow-up actions.
7. The result shows capability-pack eligibility without starting download, install, update, uninstall, or execution.
8. Developer lane and Owner lane posture remains visible only as gated boundaries, not as private setup or private asset behavior.

## Durable FFV Element Inventory

Family Feature Vision elements are durable vision units. They are not Slices, SLCs, seams, implementation tasks, or active branch status rows.

| FFV Element ID | Element | Durable User Value | Expected Surface / Flow | Boundary / Gate | Proof Expectation |
| --- | --- | --- | --- | --- | --- |
| `F7-FF01-E01` | Public Edition AI / ORIN status | The user can see whether AI assistance is locally available, degraded, disabled, or provider-blocked. | Visible ORIN / AI status in the Public Edition desktop surface. | Must not imply provider/model execution, prompt acceptance, network use, memory, or private setup. | UI/status proof plus provider-state contract proof. |
| `F7-FF01-E02` | Local assisted desktop action | The user can click a local action that is useful even without a provider. | Action control tied to the AI / ORIN status surface. | Reads public-safe local app state only; no prompt send, provider call, download, memory write, or external dependency. | Action-click result proof plus no-provider/no-egress checks. |
| `F7-FF01-E03` | Deterministic no-provider result flow | The user gets truthful local guidance instead of a broken or vague AI-disabled message. | Result panel or equivalent local response state. | Result must say provider execution is unavailable or disabled and provider-visible data is `none` when no provider path ran. | Deterministic result fixture, provider-visible-data proof, no hidden network proof. |
| `F7-FF01-E04` | Capability-pack eligibility with blocked install intent | The user can understand what capability packs could add without accidentally installing anything. | Eligibility summary and disabled or blocked install intent state. | Actual download, install, update, uninstall, model asset fetch, or capability execution remains future-gated. | Static/fixture proof that install intent is blocked and FAM-008 install authority is preserved. |
| `F7-FF01-E05` | Public / Developer / Owner lane boundary display | The user can distinguish public-safe behavior from future Developer and Owner capabilities. | Boundary labels or explanatory copy in the Public Edition surface. | No private repository, private root, private remote, private prompt, private memory, private log, or private asset exposure. | Public leak-prevention proof and branch-vision copy review. |
| `F7-FF01-E06` | Provider, download, memory, cache, and network enforcement proof | The product proves the public-safe path is not secretly executing gated AI behavior. | Validator, fixture, and branch-plan proof surface; visible copy where useful. | Provider/model execution, prompt send, downloads, network/external calls, runtime cache behavior, memory, learning, indexing, personalization, and real Owner agents remain blocked. | Provider-state validation, public leak-prevention validation, and no-egress/no-persistence checks. |

## Deferred Feature Carryforward

Deferred elements below are durable planning facts. They are not active branch status and do not approve future implementation.

| Deferred Element ID | Deferred Element | Reason | Gate / Trigger | Owner | Return Path | Required Proof | Tracking Location |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `F7-FF01-E07` | Real provider/model execution | Provider execution changes data egress, cost/privacy posture, consent, rollback, and runtime trust. | `USER-ACTION-FAM007-PROVIDER-MODEL-EXECUTION` approval. | FAM-007 provider execution branch under AI runtime/trust architecture. | Later Branch Readiness, BP1/BP2/BP3, Workstream, Hardening, and Live Validation. | Provider-visible data proof, consent proof, no hidden external calls, rollback/disable proof, direct runtime proof. | This FFV plus future FAM-007 branch plan. |
| `F7-FF01-E08` | Actual capability-pack install, download, update, uninstall, or execution | Capability-pack execution crosses storage, network, integrity, licensing, update, removal, and FAM-008 setup boundaries. | USER approves pack source, license, storage, integrity, setup UX, and execution scope. | FAM-007 capability-pack owner plus FAM-008 packaging/install owner. | Later capability-pack/setup carrier. | No hidden download, source/integrity proof, uninstall/reset proof, storage and network disclosure proof. | This FFV plus FAM-008 family vision and future branch plan. |
| `F7-FF01-E09` | Persistent memory, indexing, learning, personalization, or real Owner memory | Memory is durable user-personal state and is separate from operational cache. | `USER-ACTION-FAM007-MEMORY-LEARNING-PERSONALIZATION` approval. | FAM-007 memory/personalization branch under AI runtime/trust architecture. | Later memory-specific Branch Readiness path. | Consent, storage boundary, reset/delete/export, no hidden indexing, edition separation, no unapproved training. | This FFV plus AI runtime/trust architecture and future branch plan. |
| `F7-FF01-E10` | Private Developer or Owner setup | Private roots, repos, remotes, prompts, memory, logs, evals, and assets must not enter public source truth by inertia. | `USER-ACTION-FAM007-DEV-PRIVATE-REPO-CREATE`, `USER-ACTION-FAM007-OWNER-PRIVATE-REPO-CREATE`, or related private setup approval. | FAM-007 edition-boundary/private setup owner. | Separate private setup carrier after USER action gate. | Private origin/public-upstream proof, secret scan posture, protected asset exclusion, no Owner inheritance into Developer or Public. | Edition trust-boundary plan plus future private setup branch plan. |
| `F7-FF01-E11` | Shortcut, installer, packaging, and edition identity execution | Packaging and install behavior belongs to FAM-008 and changes public release/user setup expectations. | `USER-ACTION-FAM007-PACKAGING-EDITION-IDENTITY` or FAM-008 packaging approval. | FAM-008 packaging/install owner with FAM-007 edition-boundary input. | Later FAM-008 Branch Readiness path. | Installer/shortcut/source proof, distinct data-root proof, update-channel proof, public build exclusion proof. | FAM-008 family vision plus future packaging branch plan. |

## Cross-FAM Dependency Candidate

Cross-FAM Dependency Map: FAM-007 public-safe assisted desktop AI needs future FAM-008 packaging/install lifecycle visibility before actual shortcut, installer, package identity, update, or capability-pack install execution can be planned, but this FFV records dependency ownership only and does not create FAM-008 implementation authority.

Dependency ID: F7-XFAM-D01

Originating FAM: FAM-007

Originating FFV / Element: F7-FF01-E04 capability eligibility with blocked install intent; F7-FF01-E11 deferred shortcut, installer, packaging, and edition identity execution.

Affected FAMs: FAM-008 Packaging and Install Experience.

Affected FFV / Element or Not Created: Not Created.

Dependency Scope Class: Priority Carry-In

Carry-In / Deferral / Transfer Decision: FAM-008 must evaluate the packaging/install lifecycle dependency at its next Branch Readiness pass and group it into the relevant packaging/install FFV or branch package when created; FAM-007 does not create the FAM-008 FFV in this record.

Required Contract / Capability: FAM-008 needs a future installer/package/update lifecycle contract that can expose whether capability-pack setup, repair, shortcut identity, restart continuity, and lane-specific packaging behavior are safe for Public, Developer, and Owner lanes.

Suggested Grouping: Group with the eventual FAM-008 packaging/install lifecycle FFV rather than creating a dependency-only branch.

Proof Expectation: FAM-008 BR1/BR2 must show whether this dependency is a compatibility default, platform contract, or transferred FAM work before installer/package or capability-pack install execution begins.

Durable Disposition: Future Carry-In

Affected FAM Receipt / Fold-Down Target: Fold down to the FAM-008 Family Vision or future FAM-008 FFV dependency candidate section after USER approves the owning FAM-008 content file.

Worktree-To-Worktree Mutation: None; direct mutation of another active worktree is blocked and this FFV records durable dependency context only.

## BP1 Selection Guidance

For a public-safe no-provider assisted desktop action route, BP1 may select:

- `F7-FF01-E01`
- `F7-FF01-E02`
- `F7-FF01-E03`
- `F7-FF01-E04`
- `F7-FF01-E05`
- `F7-FF01-E06`

BP1 should defer:

- `F7-FF01-E07`
- `F7-FF01-E08`
- `F7-FF01-E09`
- `F7-FF01-E10`
- `F7-FF01-E11`

BP1 must state the selected/deferred FFV element matrix explicitly. BP2 and BP3 must map every selected FFV element to branch-local Slice/SLC/seam planning, affected surfaces, proof outputs, rollback/safety posture, and future-gated boundaries before Workstream implementation can be requested.

## Design Options

Option A - Status-only AI surface:
This improves visibility, but it can still feel inert because the user cannot do anything useful inside the no-provider boundary.

Option B - Provider setup path:
This is too broad for this category's first public-safe branch route because provider/model execution, prompt send, data egress, credentials, downloads, and cost/privacy posture require later USER gates.

Option C - Public-safe local assisted interaction:
This is the preferred direction for the selected branch route. It creates useful, clickable, deterministic no-provider behavior while preserving provider, private edition, memory, download, and packaging gates.

## Explicit Non-Goals

- Provider SDK integration.
- Provider account setup or API key creation.
- Model execution.
- Prompt acceptance or prompt send.
- Model or capability-pack download.
- Capability-pack install, update, uninstall, or execution.
- External API calls or hidden network behavior.
- Runtime cache behavior.
- Persistent memory, indexing, learning, personalization, or real Owner memory.
- Real Owner agents.
- Private Developer or Owner repositories, roots, remotes, prompts, logs, memory, evals, or assets.
- GitHub Desktop private binding.
- Public-to-Developer import.
- Backup or recovery execution.
- Voice/Core runtime sync.
- Shortcut, installer, packaging identity, or release artifact work.
- AI Product Contract import.
- Private Dev ORIN import.
- Issue mutation, PR creation, merge, release, or v1.8.0 execution.

## Proof Expectations

- The Public Edition AI / ORIN status surface is visible when implementation later begins.
- The local assisted action is clickable and produces a deterministic result.
- The result includes local capability, provider unavailable or disabled posture, provider-visible data `none`, and safe next actions.
- Capability-pack eligibility and blocked install intent appear without executing installation.
- Developer lane and Owner lane labels do not expose private content or private setup behavior.
- Provider/model execution remains disabled.
- Prompt acceptance and prompt send remain disabled.
- Downloads, installs, external calls, runtime cache behavior, memory writes, real Owner memory, and real agents remain blocked.
- Validation includes static contract proof plus UI/result-flow proof once implementation begins.

## Feature Vision Sufficiency

Feature Vision Sufficiency Check: `PASS after BR2 repair`

Sufficiency Basis: `This FFV now records a compact FFV ID, category-level scope, parent FAM basis, durable element IDs, durable user value, boundaries/gates, proof expectations, deferred feature carryforward, branch-route relationship, and BP1/BP2/BP3 consumption guidance without owning active branch state or implementation approval.`

## Fold-Down Notes

Reusable product standards accepted through later USER review should fold into this file or the owning broad FAM-007 vision when they outgrow branch-local planning.

Branch-specific implementation details, Slice/SLC/seam status, live validation evidence, review packet state, ZIP metadata, active phase state, and worktree assignment belong to the external branch plan, USER review packet, branch receipt, workstream evidence, helper output, or Git/GitHub-derived proof as routed by source truth.
