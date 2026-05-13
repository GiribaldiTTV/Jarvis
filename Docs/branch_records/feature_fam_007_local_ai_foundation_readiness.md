# Branch Authority Record: feature/fam-007-local-ai-foundation-readiness

## Branch Identity

- Branch: `feature/fam-007-local-ai-foundation-readiness`
- Workstream: `FAM-007 Local AI Foundation Readiness`
- Branch Class: `implementation`
- Backlog Record State: `Registry-only`
- Package ID: `PKG-007`
- Package Name: `Local AI and Capability Packs`

## Purpose / Why It Exists

This branch is the USER-approved Branch Readiness Stage 2 planning/source-truth carrier for FAM-007 Local AI and Capability Packs.

It exists because `v1.7.0-prebeta` is published, PR #121 merged the workspace/thread identity governance foundation, and updated `origin/main` is validated at `88c11d53845f67bbf2490b8e4ce2b224bd62437b`.

The branch digests the USER-provided `Nexus AI Product Contract v0.6.2` as planning evidence only. It records public-safe FAM-007 package shape, candidate/planned slices, blockers, proof gates, acceptance criteria, and current-vs-future boundaries before any package admission or implementation can begin.

This branch does not admit FAM-007 implementation, does not mark any package or slice as `Admitted`, does not import the full AI Product Contract, and does not mutate the parked `codex/ai-llm-lab` branch.

## Current Phase

- Phase: `Branch Readiness`

## Phase Status

- `Active Branch`: `feature/fam-007-local-ai-foundation-readiness`
- Branch Readiness Stage 1: `Complete - recommended FAM-007 planning/source-truth setup before any local AI implementation`
- Branch Readiness Stage 2 USER Approval: `Granted for branch/worktree creation, AI Product Contract v0.6.2 evidence digestion, public-safe source-truth planning updates, validation, commit, and push only`
- Branch Creation: `Created at D:\Nexus Worktrees\Nexus Desktop AI FAM-007 from origin/main commit 88c11d53845f67bbf2490b8e4ce2b224bd62437b`
- Package Admission: `Not granted`
- Slice Admission: `Not granted`
- Implementation: `Blocked`
- AI Product Contract Full Import: `Blocked`
- Old C Folder Mutation: `Blocked`
- codex/ai-llm-lab Mutation: `Blocked`

## Branch Class

- `implementation`

Implementation Delta Class: `docs-only`

## Planning-Loop Guardrail

Implementation Delta Class: `docs-only`
Docs-Only Workstream: `Yes`
Planning-Loop Bypass User Approval: `APPROVED`
Planning-Loop Bypass Reason: `USER approved Branch Readiness Stage 2 source-truth planning only, with package admission, implementation, PR creation, release work, issue creation, and AI Product Contract full import blocked.`

## Slice Continuation Policy

Slice Continuation Default: `Same-branch backlog completion`
Backlog-Split User Approval: `None`
Backlog-Split Reason: `None`

## Blockers

- `FAM-007 Package Admission Missing`: `Active - PKG-007 remains candidate/planned only`
- `FAM-007 Implementation Admission Missing`: `Active - no local model/provider/runtime code work is authorized`
- `AI Product Contract Full Import Approval Missing`: `Active - the Desktop contract is planning evidence only`
- `Admission State Granted Missing`: `Active - no package or slice may be marked Admitted on this Stage 2 pass`
- `Branch Readiness Planning Incomplete`: `Active until a later Stage 1 revalidates the finalized planning packet or USER grants an explicit waiver`
- `Feature Element Breakdown Pending Revalidation`: `Active until the candidate/planned element breakdown is revalidated after this Stage 2 source-truth update`
- `Acceptance Criteria Pending Revalidation`: `Active until a later Stage 1 confirms current-package acceptance criteria are sufficient`
- `User-Facing Proof Standard Pending Revalidation`: `Active until a later Stage 1 confirms proof expectations before Workstream`
- `Current Branch vs Future Package Boundary Pending Revalidation`: `Active until a later Stage 1 confirms what belongs in the first package versus future packages`
- `GitHub Issue Creation Approval Missing`: `Active`
- `Release Execution Approval Missing`: `Active`
- `PR Creation Approval Missing`: `Active`

## Entry Basis

- `origin/main` is validated at `88c11d53845f67bbf2490b8e4ce2b224bd62437b`.
- `D:\Nexus Repos\Nexus Desktop AI Main` is the D-drive main/consolidator clone.
- `D:\Nexus Worktrees\` is the approved active worktree root.
- `D:\Nexus Worktrees\Nexus Desktop AI FAM-007` is the approved FAM-007 worktree path for this branch.
- `C:\Nexus Desktop AI` on `codex/ai-llm-lab` remains parked lab/planning context only and must not be used as the FAM-007 implementation or governance carrier.
- The USER-provided `Nexus AI Product Contract v0.6.2` exists on the Desktop as planning evidence only. It is not repo source truth and does not authorize implementation or full import.

## Exit Criteria

- Source truth records FAM-007 public-safe product direction without importing private/internal-only planning wholesale.
- `PKG-007` is represented as candidate/planned only, not admitted.
- FAM-007 candidate/planned slices are concrete enough for later Stage 1 revalidation.
- Source truth records provider, privacy, hardware, power/performance, model/capability-pack, memory/context, action-safety, Windows, and validation boundaries as planning truth.
- Source truth records blockers that keep implementation and package admission blocked.
- Validation passes.
- Changes are committed and pushed.

## Rollback Target

- `Branch Readiness`

Rollback Commit: main at `88c11d53845f67bbf2490b8e4ce2b224bd62437b`

Rollback Path: abandon branch `feature/fam-007-local-ai-foundation-readiness` before merge; remove the worktree if needed; do not mutate old `C:\` folders or the parked `codex/ai-llm-lab` branch.

## Next Legal Phase

- `Branch Readiness`

Next Legal Seam: `Branch Readiness Stage 1 - FAM-007 Local AI Foundation Planning Revalidation`

Next Legal Phase Gate: `After this Stage 2 planning/source-truth pass is committed and pushed, a later USER-approved Branch Readiness Stage 1 must revalidate whether the candidate package is ready for package admission, branch continuation, or further planning. Workstream, implementation, package admission, PR creation, issue creation, release work, AI Product Contract full import, and codex/ai-llm-lab mutation remain blocked without later USER approval.`

## Branch Objective

Turn the USER-approved FAM-007 planning direction into public-safe repo source truth while preserving a strict boundary between planning, package admission, and implementation.

## Target End-State

- FAM-007 has a concrete candidate/planned package structure.
- `PKG-007` remains pending and not admitted.
- No slice has `Admission State: Admitted`.
- The first likely implementation package is framed as a foundation package rather than "full ORIN AI."
- The branch is ready for a later Stage 1 revalidation decision.

## Product Definition Plan

Product Vision: local-first, Windows-first ORIN/ARIA AI foundation with optional capability packs, visible provider/privacy mode, hardware safety, power-state awareness, and useful no-provider behavior.
User-Facing Goal: Nexus should feel like the same local assistant shell whether the user has no model, a local model, a LAN provider, or a user-provided external API, while clearly protecting privacy, performance, and Windows compatibility.
USER Vision Questions: no open USER questions are required for this Stage 2 source-truth setup; later Branch Readiness Stage 1 may ask package-admission questions before any implementation.
Codex Product Interpretation: the first FAM-007 package should define the local AI foundation and safety boundaries before attempting full ORIN intelligence, model downloads, memory/indexing, voice/Core sync, or Dev ORIN tooling.
Codex Implementation Recommendation: do not implement in this branch; later work should begin with hardware safety, provider boundary, privacy/provider state, Assisted Desktop Mode, and capability-pack planning before model/runtime work.
USER/ChatGPT Review Checkpoint: USER and ChatGPT accepted the AI Product Contract v0.6.2 as a stable planning baseline; this branch records a public-safe digest only and does not import the contract wholesale.
Full Feature Element Breakdown: candidate/planned elements are local AI shell/no-provider behavior, provider boundary, privacy/provider state, hardware/power routing, model/capability-pack lifecycle, data/memory/context/consent/audit/secrets, Windows resilience, ORIN/ARIA persona shell/progress presence/Core-voice sync planning, and validation/eval/abuse proof gates.
Current Branch vs Future Package Boundaries: current branch records source-truth planning, blockers, proof gates, acceptance criteria, and candidate/planned slice shape only; future admitted packages may implement providers, model loading, memory/indexing, setup, voice/Core sync, beta learning, or Dev ORIN surfaces.
Affected Surfaces: `Docs/feature_backlog.md`, `Docs/prebeta_roadmap.md`, `Docs/orin_vision.md`, `Docs/branch_records/index.md`, and this branch authority record; future runtime surfaces are planning references only.
Data/Control Model: candidate architecture separates ORIN/ARIA shell, provider router, local/LAN/external/test providers, context manager, memory manager, safety gate, capability-pack manager, and Windows/hardware profiler responsibilities.
Branch Reach / Package-Size Review: candidate `PKG-007` is intentionally multi-slice because provider choice, hardware safety, privacy state, model lifecycle, memory/context, Windows resilience, and proof gates are coupled foundation decisions.
Why Branch Is Large Enough: a single narrow slice would either overpromise AI behavior without safety/provider boundaries or create a model connector before privacy, hardware, update, and no-provider rules exist.
Why Not Split Into Tiny Branches: splitting the foundation before boundaries are settled would increase drift between provider mode, hardware gating, capability packs, privacy claims, and validation expectations.
Acceptance Criteria: Stage 2 acceptance is planning/source-truth only: public-safe direction, candidate/planned package and slice shape, blockers, proof gates, current-vs-future boundaries, validation green, commit, and push.
Validation Proof Requirements: governance validator, release-body validator, compileall, diff checks, source-truth searches, and explicit evidence that no package/slice is admitted and no implementation scope was entered.
Screenshot / Live / User Test Summary Proof Requirements: no screenshot/live/UTS proof is required for this planning-only branch; future user-facing AI surfaces must define UTS and screenshot/live proof during admitted implementation phases.
Implementation Sequence Proposal: later sequence should revalidate planning, admit package/slices only with USER approval, then proceed through provider boundary/test stub, hardware safety, privacy/provider state, Assisted Desktop Mode, model/capability-pack lifecycle, context/memory, persona/Core/voice planning, and validation gates as separately admitted work.
Planning Blockers: FAM-007 package admission missing; implementation admission missing; AI Product Contract full import approval missing; feature element breakdown, acceptance criteria, user-facing proof standard, and current-vs-future boundary require later Stage 1 revalidation.
USER Decisions Needed: later USER approval is required for package admission, slice admission, implementation, full AI Product Contract import, PR creation, GitHub issue creation, release work, Dev ORIN/private material import, or `codex/ai-llm-lab` mutation.
Planning Packet Status: Complete
Planning Revalidation Status: Complete
User Test Summary Strategy: no User Test Summary is generated by this branch; future user-facing AI surfaces require UTS planning and acceptance or explicit waiver.
Planning Completion Waiver: None

## Backlog Completion Strategy

This branch does not complete or admit a backlog package. It records a public-safe Branch Readiness planning foundation for `FAM-007` and leaves package admission, implementation, PR creation, issue creation, release work, and full AI Product Contract import blocked for later USER-approved phases.

Branch Completion Goal: source-truth planning is durable enough for a later Branch Readiness Stage 1 revalidation to decide whether `PKG-007` is ready for package admission, further planning, or deferral.
Known Future-Dependent Blockers: FAM-007 package admission, FAM-007 implementation, AI Product Contract full import, GitHub issue creation, release execution, and `codex/ai-llm-lab` mutation remain future approval gates.
Branch Closure Rule: this branch may only close as planning/source-truth readiness; it does not satisfy package completion, slice completion, or implementation completion.

## Expected Seam Families And Risk Classes

- Branch Readiness Stage 2 source-truth planning setup.
- Local AI foundation and capability-pack package planning.
- Provider/privacy/hardware/power/model/memory/action-safety/Windows proof-gate planning.
- Public-safe AI Product Contract evidence digestion.
- Current-vs-future package boundary definition.

Risk Classes: accidental package admission, accidental implementation start, private-material import, provider/privacy overpromise, hardware-capability overpromise, weak Windows support wording, AI lab branch repurpose, and stale source-truth sequencing.

## Product Vision Alignment

FAM-007 should preserve these product principles:

- Nexus remains Windows-first and local-first where practical.
- Base Nexus remains useful without a local LLM.
- ORIN/ARIA remain the user-facing assistant layer even when local, LAN, or external API providers are used.
- Provider selection must be visible and revocable.
- External API support may be available without a Nexus connection fee, while third-party provider charges remain the user's responsibility.
- Local AI work must respect hardware limits, power state, thermals, privacy, and user consent.
- Heavy local AI should remain optional capability-pack work, not default installer bloat.
- Boot-facing and secure sign-in work remains future/high-risk and does not ride the first local AI package.
- Internal Dev ORIN/private prompt/eval/beta-feedback tooling remains private/off-repo unless intentionally sanitized and approved later.

## Candidate Package Shape

Candidate First Package:

`Local AI Foundation, Hardware Safety, Provider Boundary, Privacy State, Assisted Desktop Mode, Degraded Mode, and Capability-Pack Planning`

Package Status: `Candidate / Planned`

Package Admission State: `Pending USER approval / no active package admission`

Package Completion State: `Pending`

Single-Slice Package User Approval: `Not required - no active single-slice package is admitted; the candidate package intentionally contains multiple planned slices`

## Candidate / Planned Slice Structure

| Slice ID | Package ID | FAM ID | Slice Name | Admission State | Slice Status | Completion State | Stage 2 Boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SLC-017` | `PKG-007` | `FAM-007` | Local AI shell, Assisted Desktop Mode, and no-provider behavior | Candidate / Planned | Planning only | Pending | Define how Nexus stays useful with no local model, no LAN provider, and no API provider |
| `SLC-018` | `PKG-007` | `FAM-007` | Provider boundary and visible privacy/provider state | Candidate / Planned | Planning only | Pending | Define local, LAN, external API, and test-stub provider boundaries without binding to one vendor/runtime |
| `SLC-031` | `PKG-007` | `FAM-007` | Hardware safety, power state, and capability routing | Candidate / Planned | Planning only | Pending | Define hardware tiering, power/battery behavior, GPU/CPU fallback posture, and task deferral rules |
| `SLC-032` | `PKG-007` | `FAM-007` | Model and capability-pack lifecycle | Candidate / Planned | Planning only | Pending | Define optional model/capability-pack install, license gate, integrity checks, update migration, and disk/runtime preflight |
| `SLC-033` | `PKG-007` | `FAM-007` | Data classification, memory, context, consent, audit, and secrets | Candidate / Planned | Planning only | Pending | Define privacy, memory, source packing, action consent, audit log, secure storage, and trust reset boundaries |
| `SLC-034` | `PKG-007` | `FAM-007` | Windows compatibility, resilience, and installer/platform posture | Candidate / Planned | Planning only | Pending | Define Windows 11 primary support, limited Windows 10 posture, unsupported legacy OS stance, Defender/update/runtime repair paths |
| `SLC-035` | `PKG-007` | `FAM-007` | ORIN/ARIA persona shell, progress presence, and core/voice sync planning | Candidate / Planned | Planning only | Pending | Define provider-independent persona behavior, progress pacing, and future Core/voice sync boundary without implementing it |
| `SLC-036` | `PKG-007` | `FAM-007` | Validation, evaluation, abuse testing, and release proof gates | Candidate / Planned | Planning only | Pending | Define proof expectations for local-only behavior, provider outages, hardware downgrades, privacy, safe actions, and cost/rate awareness |

No row above is admitted. Each row is candidate/planned source truth for later revalidation only.

## Element Coverage Review

- User-facing surface: candidate provider/privacy status, Assisted Desktop Mode, no-provider/degraded explanations, and future ORIN/Core visible state.
- Runtime/backend behavior: candidate provider boundary, router, local/LAN/API/test provider abstractions, and task deferral logic.
- Fail-safe/recovery: candidate no-provider state, provider outage states, hardware downgrade/block behavior, emergency stop, trust reset, repair flows.
- Security/privacy: candidate data classification, Local Only proof, secrets handling, audit log redaction, consent profiles, network boundary, memory portability.
- Voice/audio: future ORIN/ARIA voice and Core sync planning only; implementation requires later voice/audio and interface proof.
- External integration: external API and LAN provider modes remain opt-in, visible, revocable, and cost/privacy-aware.
- Local AI/capability packs: optional model/capability-pack lifecycle, license gate, model integrity, and update/migration planning.
- Packaging/install: lean base install, optional heavy downloads, Windows support warnings, and installer/platform compatibility planning.
- Monitoring/HUD: candidate hardware and power-state reuse may touch monitoring concepts, but no FAM-006 HUD implementation is reopened.
- Validation: provider visibility, Local Only no-external-call proof, hardware downgrade/block proof, model download integrity, data classification, and safe action confirmations.
- Release impact: planning-only branch; no release/tag/artifact work is authorized.

## Current Branch vs Future Package Boundaries

Current branch may:

- digest public-safe AI planning evidence into repo truth
- define candidate/planned package and slice structure
- record blockers, acceptance criteria, proof gates, and validation expectations
- keep private/internal-only material out of public repo truth

Current branch must not:

- implement local models, provider runtime code, APIs, memory, indexing, voice/core sync, setup wizard, or hardware profiler
- admit `PKG-007` or any slice
- mark any `Admission State` as `Admitted`
- import the full AI Product Contract
- mutate `codex/ai-llm-lab`
- create issues, PRs, releases, tags, GitHub Releases, or artifacts

Future packages may later admit:

- hardware profiler implementation
- provider interface and test stub
- no-provider/Assisted Desktop Mode runtime behavior
- privacy/provider status UI
- local model connector
- model/capability-pack manager
- memory/indexing
- voice/Core sync
- beta feedback pipeline
- Dev Toolkit AI surface
- internal Dev ORIN private tooling

## Interface Release Boundary

Interface Release Boundary: `Candidate only / not admitted`

Candidate Primary Interface Release Surface: `Provider/privacy status and Assisted Desktop Mode setup/status surfaces`

Interface Bundle User Approval: `Not granted`

Fallback Point: `Assisted Desktop Mode with No AI Provider`

Interface Acceptance Path: `Future Workstream/Live Validation must prove the primary interface with screenshot/live proof and a User Test Summary or explicit waiver. This Stage 2 pass records planning only.`

## Acceptance Criteria

Planning acceptance for this branch requires:

- public-safe FAM-007 product direction recorded in repo truth
- candidate package and multiple candidate/planned slices recorded without admission
- all implementation, package admission, private import, and external action blockers preserved
- AI Product Contract v0.6.2 referenced only as USER planning evidence
- old `C:\` folders and parked `codex/ai-llm-lab` untouched
- validation green
- commit and push complete

Future implementation acceptance will require separate criteria after package admission.

## Proof Expectations

Future FAM-007 implementation must be able to prove:

- provider/privacy mode is visible and accurate
- Local Only mode performs no external provider calls
- no-provider behavior degrades into Assisted Desktop Mode cleanly
- weak hardware is blocked, downgraded, or routed to safer alternatives
- power/battery/GPU/performance changes require consent or approved automation rules
- external API usage is opt-in, revocable, provider/cost-aware, and does not replace the local ORIN shell
- data classification happens before indexing, logging, storing, sending, or context packing
- secrets are stored securely where practical and never logged
- model/capability-pack downloads verify manifest, source, license record, disk preflight, and checksum/signature where practical
- destructive or system-affecting actions require confirmation
- provider outage states are explicit and recoverable
- Windows dependency, Defender, driver, runtime, startup, and permission failures degrade gracefully
- public Dev Toolkit AI surfaces do not expose private Dev ORIN prompts, evals, beta-feedback pipelines, or private memory

## Validation Plan

Stage 2 validation:

- `git status --short --branch`
- `git fetch origin`
- `git rev-parse HEAD`
- `git rev-parse origin/main`
- `git worktree list`
- `git diff --check`
- `python dev/orin_branch_governance_validation.py`
- `python dev/orin_release_body_validation.py`
- `python -m compileall -q dev desktop Audio main.py`
- targeted source-truth searches for FAM-007, PKG-007, candidate/planned slices, blocked admission, and AI Product Contract evidence-only wording

Future implementation validation:

- provider boundary tests
- no-provider state tests
- Local Only no-network/provider-call tests
- hardware-tier and power-state tests
- model/capability-pack integrity tests
- context/data classification tests
- action-safety confirmation tests
- Windows compatibility and recovery tests
- user-facing screenshot/live/User Test Summary proof when UI exists

## User Test Summary Strategy

No User Test Summary is generated or refreshed by this planning/source-truth branch.

Future user-facing AI surfaces must define a real User Test Summary checklist during Live Validation, including setup, exact actions, visible expected behavior, privacy/provider indicators, failure signs, and acceptance criteria.

## Initial Workstream Seam Sequence

Seam 1: FAM-007 local AI foundation planning/source-truth setup.
Goal: record the public-safe local AI foundation package shape, candidate/planned slice structure, blockers, proof gates, and acceptance criteria.
Scope: `Docs/feature_backlog.md`, `Docs/prebeta_roadmap.md`, `Docs/orin_vision.md`, `Docs/branch_records/index.md`, and this branch authority record.
Non-Includes: package admission, implementation, runtime code edits, local model/provider work, AI Product Contract full import, GitHub issue creation, PR creation, release/tag/artifact work, old `C:\` folder mutation, or `codex/ai-llm-lab` mutation.

## Active Seam

Active seam: `Branch Readiness Stage 2 - FAM-007 local AI foundation planning/source-truth setup`

The active seam is docs-only planning/source-truth setup. Workstream, implementation, package admission, PR creation, release work, and issue creation remain blocked until later USER approval.

## Later-Phase Expectations

A later Branch Readiness Stage 1 should revalidate:

- whether the candidate package is complete enough for package admission
- whether additional USER vision questions are needed
- whether the current branch may continue into package admission or needs another planning loop
- whether `PKG-007` should remain planning-only, be admitted with multiple slices, or be deferred
- whether any candidate/planned slice should split into a future package

Workstream must not begin until package admission is explicit and source truth marks specific slices as `Admitted`.
