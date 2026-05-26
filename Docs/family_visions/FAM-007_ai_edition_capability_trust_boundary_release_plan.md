# FAM-007 AI Edition Capability / Trust Boundary Release Plan

NEXUS-SOURCE-OWNER: schema=source-owner-v1; owner=FAM007-AI; ledger=feature-fam-007-local-ai-provider-setup-completion-foundation; surface=ai-edition-capability-trust-boundary-release-plan; status=canonical

## Purpose

This document records the public-safe vision and concrete release plan for the Nexus Desktop AI edition model.

It defines how the project should eventually support:

- `Nexus Desktop AI` as the Public/User product.
- `Nexus Desktop AI Dev` as the contributor/developer edition.
- `Nexus Desktop AI Owner` as the private owner-only edition.

This plan exists so future FAM-007, FAM-008, packaging, privacy, memory, provider, and AI-runtime branches do not drift into one blended product that leaks private owner or developer capability into the public source tree.

## Status

Planning State: `USER-accepted durable planning source truth preserved after PR #210 merged the FAM-007 setup completion carrier; future FAM-007, FAM-008, packaging, privacy, memory, provider, and AI-runtime branches must consult this plan before implementation.`

Implementation State: `Not implemented.`

Release State: `Not released as functional edition behavior.`

Runtime Authorization: `None from this document.`

This plan does not authorize:

- provider SDK integration
- model execution
- model downloads
- external provider/API calls
- memory indexing, retrieval, learning, persistence, or personalization
- voice/Core runtime sync
- shortcut or installer work
- licensing, activation, encryption, or entitlement implementation
- private repository creation
- private artifact publication
- PR creation, merge, tag, GitHub Release, or release artifact work

Those remain separate USER decisions in their owning branches.

## Source-Truth Grounding

This plan is grounded in current public repo truth:

- `Docs/nexus_vision.md` owns the project-wide AI direction and says local AI/capability-pack planning is public-safe intent only.
- `Docs/family_visions/FAM-007_local_ai_and_capability_packs.md` owns local AI, provider setup, provider readiness, capability packs, model lifecycle, provider-visible data, execution gates, and memory/future learning boundaries.
- `Docs/family_visions/FAM-008_packaging_and_install_experience.md` owns installer, shortcuts, packaged app identity, capability-pack install boundaries, update flow, and setup lifecycle.
- `Docs/ai_runtime_and_trust_architecture.md` owns cross-family AI runtime/trust, permission-state, provider-visible data, Local-Only, Trust Journal, privacy-lockdown, and sensitive capability architecture.
- Relevant existing FAM visions own their own family-local privacy, safety, consent, provider-visible data, and data-root implications.
- `desktop/ai_provider_state.py` and `dev/orin_ai_provider_state_validation.py` currently keep provider/model execution, prompt acceptance, network egress, downloads, memory, personalization, and voice/Core sync blocked until later USER-approved work.
- `Docs/branch_records/feature_repo_wide_source_owner_marker_adoption.md` records that dev-only tooling, source-owner markers, and review overlays must not leak into production/public UI.

## Core Model

The project should use an Edition Capability / Trust Boundary model, not three unrelated forks.

The goal is one shared public-safe core with edition-specific capability gates, private overlays, separate data identities, separate update channels, and strict no-leak rules.

| Edition | Product Name | Trust Boundary | Main Purpose | Public Repo Inclusion |
| --- | --- | --- | --- | --- |
| Public | `Nexus Desktop AI` | Least privilege | Normal user-facing product | Public-safe core, docs, validators, and generic gates |
| Dev | `Nexus Desktop AI Dev` | Trusted contributor | Development, validation, repo-aware support | Public-safe hooks only; private Dev intelligence stays outside public repo |
| Owner | `Nexus Desktop AI Owner` | Owner-only highest trust | Private co-developer AI and personal product partner | No private Owner logic, memory, prompts, secrets, evals, or tools |

## Public Repo Rule

The public repository may define the edition model, generic capability gates, safe manifest schema, public-safe test fixtures, and validators.

The public repository must not contain:

- owner-private prompts
- owner-private memory
- owner-private strategy, planning notes, or repo roadmap material not approved for public release
- owner GitHub tokens, API keys, credentials, cookies, sessions, or secrets
- private Dev ORIN content
- private eval logs
- private model weights or proprietary capability packs
- private assistant instructions that would allow someone to clone the Owner or Dev intelligence layer
- hidden provider/model/memory behavior
- dev-only UI markers in production/public UI

The safest rule is simple: if losing the public repo would expose it, it cannot be the thing that makes Owner or Dev special.

## Protected Assets Table

Protected assets are the material that gives Dev or Owner editions private value, private authority, private context, or private access. Future branches and validators should use this table as the public-safe reference for what must be excluded, gated, sanitized, or kept private.

| Asset Class | Examples | Public Repo Allowed | Dev Repo Allowed | Owner Repo Allowed | Public Artifact Allowed | Required Gate |
| --- | --- | --- | --- | --- | --- | --- |
| Owner memory | owner-private accepted feedback, owner-specific memories, long-term preferences, private interaction history, and feedback not approved for public source truth | No | No | Yes, only with owner-approved local/private storage | No | Owner memory consent, local vault/encryption plan, no-export default |
| Owner prompts and instructions | private system prompts, owner-specific Codex handoff rules, private assistant behavior prompts | No | No | Yes | No | Owner-only source root or private repo plus private-to-public sanitization before any excerpt leaves Owner |
| Private strategy and planning | private strategy, private planning material, owner roadmap material not approved for public release, competitive/product timing notes | No | No by default | Yes | No | USER approval and sanitized public-safe summary only |
| Secrets and credentials | GitHub tokens, provider keys, API keys, cookies, sessions, signing keys, vault secrets | No | No tracked storage; only scoped local secret store when approved | No tracked storage; only scoped local/owner vault when approved | No | Secret scan, vault/credential-store plan, no tracked plaintext |
| Private Dev ORIN content | private Dev ORIN prompts, evals, workflows, unpublished developer helper instructions | No | Yes, if contributor-scoped and not owner-private | Only if manually selected by Owner | No | Dev private repo gate and no-owner-private scan |
| Private eval logs and support data | raw eval conversations, debug logs, support bundles, screenshots, crash dumps, imported Public user diagnostics | No unless synthetic/sanitized | Yes only when scoped, redacted, and user-approved | Yes only when owner-approved | No by default | Redaction, provenance, user consent, and no-export review |
| Private model or capability assets | model weights, adapters, private capability packs, proprietary data files, entitlement-gated binaries | No | Yes only in private artifact channel or private repo when licensed | Yes only in private artifact channel or private owner root | No unless public license/distribution is approved | License / redistribution review, artifact provenance, SBOM or manifest review, integrity/signature proof, signed artifact gate, public release approval |
| Private automation | owner automation scripts, unrestricted repo/GitHub actions, private repair loops, private watcher/reporting routes | No | Yes only when dev-scoped and audited | Yes only when owner-approved and reversible | No | Tool permission review, audit log, bounded action contract |
| Imported Public user data | Public settings, consent state, personalization, logs, future memory imported into Dev | No as raw data | Yes only after explicit import consent and no-export default | No by default; sanitized fixtures only | No | Public-to-Dev import consent level and provenance stamp |
| Dev-only UI/tooling metadata | source-owner overlays, branch governance tools, review markers, debug badges, dev launchers | Public-safe docs/validators only | Yes | Yes if owner chooses | No production public UI | Public build exclusion and no-dev-tooling-in-public-UI validation |
| Hidden provider/model/memory behavior | undisclosed prompt send, model execution, memory indexing, background network egress | No | No unless explicitly developer-visible and approved | No unless explicitly owner-approved and audited | No | Provider-visible data, consent, network, memory, and execution gates |

## Public-Safe Fixture Rule

Public-safe fixtures must be synthetic, non-secret, non-owner-specific, non-memory-derived, non-token-derived, and not copied from private logs unless sanitized and USER-approved.

Fixtures in the public repo may demonstrate schemas, state transitions, validation boundaries, and no-leak rules, but they must not contain real Owner memory, real Dev/private content, real user logs, real provider credentials, private strategy, private planning material, private model data, or owner roadmap material not approved for public release.

## Public Review-Bundle Leak-Prevention Rule

Public review bundles must not include Owner/Dev private files, private repo paths, private logs, private prompts, private memory, private automation, private artifact references, private model outputs, private Codex handoff artifacts, or private screenshots unless the material is sanitized and USER-approved for that exact public review bundle.

Review bundles created from the public repo should copy only public repo-relative files or public-safe generated review guides. If a future helper needs private-edition review bundles, it must use a private review root or explicit private-workspace routing and must not mix those files with public FAM review bundles.

## Edition Names

Public Edition name: `Nexus Desktop AI`.

Dev Edition working name: `Nexus Desktop AI Dev`. This is accepted for planning and may be renamed by USER before packaging if desired.

Owner Edition accepted name: `Nexus Desktop AI Owner`.

## Public Edition Vision

Public Edition should eventually provide:

- user-facing assistant behavior
- visible provider state
- visible consent state
- safe local-first defaults
- optional capability packs
- clear no-provider and degraded-mode behavior
- safe setup completion and reset behavior
- no hidden data egress
- no hidden provider/model execution
- no dev-only tooling
- no owner-private context

Public Edition must not include:

- GitHub/repo automation intended for owner or contributor workflows
- source-owner review overlays
- branch governance tools exposed in production UI
- owner-private memory
- owner-private instructions
- developer tokens
- private eval harnesses
- unrestricted local automation

## Dev Edition Vision

Dev Edition should eventually provide:

- issue and PR intake support
- log and support bundle analysis
- repo navigation
- validation guidance
- source-owner review support
- branch/source-truth awareness
- debug assistance
- contributor-scoped GitHub/repo helpers
- Public-to-Dev profile import with explicit USER approval

Dev Edition must not include:

- owner-private memory
- owner GitHub credentials
- owner-only private planning
- unrestricted automation
- production-user data export by default
- hidden provider/model behavior

Dev Edition is trusted, but it is not owner-private.

Formal Dev Boundary Rule: Dev Edition may contain contributor/dev tooling, but it must not inherit Owner memory, Owner prompts, Owner strategy, Owner credentials, Owner automation, Owner private planning, or owner roadmap material not approved for public release by default. Dev is allowed to be powerful for contributor workflows; it is not allowed to become a backdoor copy of Owner.

## Owner Edition Vision

Owner Edition should eventually provide:

- private AI partner behavior
- product vision support
- creative planning support
- repo/GitHub/governance assistance
- Codex handoff support
- validation review
- issue/log intake
- private memory with explicit local consent and safeguards
- owner-specific development workflows
- reversible owner-approved automation

Owner Edition must not ship as the public user product.

Owner Edition must not leak:

- owner memory
- owner prompts
- owner strategy
- private strategy
- private planning material
- owner roadmap material not approved for public release
- owner GitHub credentials
- private logs
- private model or capability-pack assets
- private repo automation

Owner-As-Private-Test-Person Rule: Owner Edition may act as a private test/evaluation persona for Public Edition, including launching, testing, and evaluating the public user experience as the owner, but Owner behavior is not shipped Public Edition behavior. Owner behavior cannot define Public runtime behavior unless a later public-safe branch implements, validates, and releases that behavior through normal public source-truth and validation gates.

Owner Screenshots / Logs / Evals Rule: Owner screenshots, Owner logs, Owner evaluation transcripts, private model outputs, and private Codex handoff artifacts are Owner-private by default. They may become public evidence only after explicit USER approval, sanitization, protected-asset review, and source-truth routing.

## Repository Topology

The recommended long-term topology is:

| Repository | Visibility | Role | Contains |
| --- | --- | --- | --- |
| `Nexus-Desktop-AI` | Public | shared public core | public source, public docs, public validators, public-safe edition gates |
| `Nexus-Desktop-AI-Dev` | Private | developer edition overlay | contributor tools, dev edition prompts/config, private dev helpers, dev-specific docs |
| `Nexus-Desktop-AI-Owner` | Private | owner-only overlay | owner prompts, owner memory adapters, private automation, owner-specific workflows |
| private package/artifact channel | Private | protected binary/model/capability distribution | signed capability packs, private model assets, entitlement-gated artifacts |

Public repo should remain upstream.

Private edition repos should consume public changes.

Private repos should not be treated as sources to bulk-copy back into public.

## Edition Boundary Manifest Planning

Future branches should introduce a public-safe edition boundary manifest concept before edition-specific runtime behavior becomes hard to reason about.

Candidate manifest name: `edition_boundary_manifest.json`.

This plan does not implement the manifest. It records the future schema direction so Breakpoint 1 and Breakpoint 2 can turn the vision into validator-backed configuration.

Public-safe candidate fields:

- `edition`
- `repo_role`
- `data_root`
- `allowed_capability_classes`
- `blocked_capability_classes`
- `protected_asset_policy`
- `provider_execution_allowed`
- `memory_allowed`
- `network_allowed`
- `owner_private_allowed`
- `dev_private_allowed`
- `public_artifact_allowed`

The manifest must not contain secrets, private prompts, private memory, private strategy, model assets, or private capability-pack payloads.

## Sync Direction

Preferred sync model:

1. Public `main` remains the clean upstream.
2. Dev and Owner private repos track public `main` as `public-upstream` or equivalent.
3. Private edition repos merge or rebase public releases into private branches.
4. Private changes flow back to public only through a sanitization gate.
5. Sanitized public-safe improvements are reimplemented or cherry-picked only after review proves no private data, prompts, secrets, memory, or protected capability assets are included.

Private-to-public flow must be exceptional and review-heavy.

Public-to-private flow should be routine.

## Private-To-Public Sanitization Gate

Private-to-public movement is blocked until this gate is `PASS` or the USER grants an explicit waiver that names the source edition, target edition, candidate files, protected assets involved, and residual risk.

Required gate fields:

- Source Edition:
- Target Edition:
- Candidate Files:
- Protected Asset Scan:
- Secret Scan:
- Prompt / Memory Strip:
- Private Path Scan:
- Model / Capability Asset Scan:
- Private Automation Scan:
- Source-Truth Owner Review:
- USER Approval:
- Sanitization Result:

The default result is `BLOCKED` when any candidate file contains Owner memory, Owner prompts, private strategy, private planning material, owner roadmap material not approved for public release, secrets, private Dev ORIN content, private eval logs, private model/capability assets, imported Public user data, or private automation.

Public-safe reimplementation is preferred over direct private-to-public copying when private context influenced the change.

## Local Path Model

Recommended local roots:

| Edition | Suggested Local Source Root | Suggested Data Root |
| --- | --- | --- |
| Public | `C:\Nexus Desktop AI` and governed public worktrees under `C:\Nexus Worktrees\` | `%APPDATA%\Nexus Desktop AI` |
| Dev | `D:\Nexus Private\Nexus Desktop AI Dev` or `D:\Nexus Dev ORIN\Nexus Desktop AI Dev` | `%APPDATA%\Nexus Desktop AI Dev` |
| Owner | `D:\Nexus Private\Nexus Desktop AI Owner` or another owner-only private root | `%APPDATA%\Nexus Desktop AI Owner` |

The exact private paths remain a later USER decision.

The important rule is separation:

- separate repo folders
- separate Git remotes
- separate app IDs
- separate data roots
- separate logs
- separate model/capability-pack caches
- separate update channels
- separate secrets stores

## Off-Boot Backup And Recovery Planning

Nexus Desktop AI must not rely on the OS boot drive as the only copy of personalized AI state, private edition source, private memory, or edition recovery material. This is planning only; it does not create repositories, copy data, enable memory, or implement backup automation.

The preferred future posture is:

- Public user data may remain in the normal Public data root during runtime, but any future backup/recovery feature must offer an off-boot backup target before persistent AI personalization is treated as durable.
- Dev Edition should have a private source root and a separate off-boot backup/recovery root.
- Nexus Desktop AI Owner should have its own private repo when USER approves private hosting, or a local-only Owner skeleton first when USER chooses that posture.
- Nexus Desktop AI Owner must also have a separate off-boot backup/recovery root before owner-private memory, owner strategy, owner prompts, private automation, or owner-specific personalization is treated as durable.
- `D:\Nexus Backups\Nexus Desktop AI`, `D:\Nexus Backups\Nexus Desktop AI Dev`, and `D:\Nexus Backups\Nexus Desktop AI Owner` are acceptable planning examples when `D:\` is not the OS boot drive.
- A same-machine non-boot drive protects against OS-drive failure, but not whole-machine loss; future security planning should recommend an additional encrypted external or private off-device backup when the USER is ready.
- Any backup containing private memory, prompts, logs, transcripts, screenshots, model outputs, credentials, private strategy, private planning material, or private automation is protected material by default.
- Backup roots, restore logs, manifests, and recovery screenshots must not be included in public commits, public review bundles, public artifacts, or public release evidence unless sanitized and USER-approved through `USER-ACTION-FAM007-PRIVATE-TO-PUBLIC-SANITIZATION`.

Future backup/recovery work must prove that a reinstall can restore the approved edition's allowed state without crossing edition boundaries. Public restore must not import Dev or Owner state. Dev restore must not import Owner state. Owner restore must remain owner-private.

## GitHub Desktop Setup Plan

GitHub Desktop should be configured so each edition is visibly separate.

### Public Repo Binding

- Local path: `C:\Nexus Desktop AI` or the governed public worktree path assigned by repo source truth.
- Remote: `GiribaldiTTV/Nexus-Desktop-AI`.
- Use for public-safe branches and PRs only.
- Never use this repository window for Owner or Dev private overlays.

### Dev Repo Binding

- Local path: private Dev source root.
- Remote: private `Nexus-Desktop-AI-Dev` repository.
- Optional extra remote: public upstream, named `public-upstream`.
- Use for contributor/dev edition work only.
- Never publish owner memory, owner prompts, owner strategy, owner credentials, or private Owner tooling from this binding.

### Owner Repo Binding

- Local path: private Owner source root.
- Remote: private `Nexus-Desktop-AI-Owner` repository or local-only until the USER explicitly chooses private GitHub hosting.
- Optional extra remote: public upstream, named `public-upstream`.
- Use for owner-only workflows.
- Never push Owner branches to the public `Nexus-Desktop-AI` remote.

### Private Repo Remote Rules

- Dev and Owner `origin` must be the private repository when those repos are GitHub-hosted.
- Public repo remote in Dev and Owner repos should be named `public-upstream`.
- Public repo remote should be fetch-only unless the USER explicitly approves a different topology.
- Owner may remain local-only until the USER approves private GitHub hosting.
- Public repo remote must never be named `origin` in Dev or Owner repos.
- Private Dev/Owner repos should configure `public-upstream` with no push URL, a disabled push URL, or a pre-push guard before private branch push workflows are trusted.
- GitHub Desktop should show a visibly private repository for Dev and Owner before any push.
- If remote naming is ambiguous, stop before commit or push and return a routing packet.

### GitHub Desktop Safety Checklist

Before committing or pushing in GitHub Desktop:

1. Confirm the selected repository name.
2. Confirm the local path.
3. Confirm the current branch.
4. Confirm the remote target.
5. Confirm changed files contain no secrets, memory, private prompts, private logs, tokens, model assets, or private capability packs.
6. Confirm the branch belongs to the intended edition.
7. If the repository is Public, confirm the change is public-safe.
8. If the repository is Dev, confirm no Owner-only content is included.
9. If the repository is Owner, confirm no remote points to public GitHub except a fetch-only public upstream.

If GitHub Desktop shows `Publish branch` while the selected repository is the public repo, stop and verify that the branch is public-safe.

If GitHub Desktop shows `Push origin` while working in Dev or Owner, stop and verify that `origin` is the private repository, not the public one.

## Codex Setup Plan

Codex should treat each edition as a separate workspace and trust boundary.

Public Codex threads may work in the public repo or public FAM worktrees, update public-safe docs, implement public-safe runtime behavior, run public validators, and prepare public PRs.

Public Codex threads must not inspect private Owner/Dev repos unless the USER explicitly routes that work, import private memory or prompts, copy private logic into public, or create public commits from private roots.

Dev Codex threads may work in the private Dev repo, use Dev-specific instructions, inspect public upstream for sync, build contributor workflows, and test Public-to-Dev migration with sanitized fixtures.

Dev Codex threads must not access Owner memory or Owner secrets, export imported user data into GitHub issues/logs/providers by default, or push Dev private content to public.

Owner Codex threads may work in the private Owner repo, use owner-specific memory and planning, help with private product strategy, and coordinate owner-only automation when approved.

Owner Codex threads must not push Owner content to public, expose owner memory to Dev or Public, or copy private prompts, credentials, logs, or model assets into the public repo.

## Public To Dev Migration Model

Public users may realistically become Dev users.

That path should be supported intentionally.

Default rule: copy, do not move.

Public Edition data should remain intact when a user creates a Dev Edition profile.

### Migration Flow

1. Dev Edition detects a Public Edition profile.
2. Dev Edition offers an explicit import wizard.
3. User chooses what to import.
4. Dev Edition copies selected data into the Dev data root.
5. Dev Edition stamps every imported record with provenance.
6. Dev Edition applies Dev-specific consent and capability gates.
7. Dev Edition keeps imported data local unless the user separately approves a data-sharing path.

### Importable Data Candidates

Potentially importable after explicit user approval:

- user profile preferences
- public assistant settings
- consent records
- provider setup state
- local-only memory or personalization records if future Public Edition supports them
- local capability-pack preferences
- UI preferences
- safe non-secret logs selected by the user

Not importable by default:

- secrets
- tokens
- provider API keys
- raw private logs
- unsupported memory stores
- crash dumps that may contain private data
- anything already marked no-export

### Dev Import Safety Requirements

Dev import must prove:

- user approval was explicit
- imported data was copied, not moved
- public data remains intact
- imported data records their Public source
- Dev profile can reset imported data without damaging Public profile
- GitHub issue/report helpers cannot automatically attach imported private data
- provider-visible data remains explicit
- memory/indexing/learning remains gated until approved

### Public-To-Dev Import Consent Levels

Public-to-Dev import should be explicit and level-based:

| Level | Import Scope | Default |
| --- | --- | --- |
| Level 0 | No import | Safe default |
| Level 1 | Settings only | Recommended first import |
| Level 2 | Settings plus consent state | Allowed with explicit consent-state notice |
| Level 3 | Settings plus local personalization | Allowed only when personalization exists and user approves |
| Level 4 | Manually selected logs/support data | Manual selection only |
| Level 5 | Memory import | Separate explicit approval only |

Secrets, tokens, provider API keys, raw private logs, unsupported memory stores, crash dumps with private data, and no-export data are never imported by default.

## Owner Isolation Model

Public to Owner migration should not be a normal user path.

Owner Edition is owner-only.

Owner Edition may manually import selected sanitized Public fixtures for testing, but the default path should be blocked.

Owner import must be manual, explicit, local-only unless otherwise approved, audited, reversible, and never exposed to public repo commits.

Dev to Owner migration should also be blocked by default. Owner Edition may consume Dev tooling patterns, but it should not automatically inherit Dev profiles, contributor logs, issue data, or imported Public user data.

Owner data must never export automatically. Owner-to-public or Owner-to-Dev flow may occur only through explicit USER selection, sanitization, private-data review, secret scanning, prompt/memory stripping, source-truth review, and public-safe reimplementation or cherry-pick.

The default is no export.

## Data And Secret Boundaries

Each edition should eventually use separate:

- app identity
- install directory
- config directory
- data directory
- cache directory
- model cache
- capability-pack cache
- log directory
- secrets store
- update channel
- telemetry/reporting posture

Secrets should never be stored in plain tracked files.

Future secrets handling should use an OS credential vault, encrypted local vault, or another USER-approved safety/privacy mechanism.

## Public Build Exclusion Requirement

Public builds must fail when Dev/Owner-only files, manifests, prompts, memory adapters, private configs, private capability-pack references, private model references, private automation, protected asset paths, or private repository overlays are included.

This requirement is a future build/validator gate. It is not implemented by this plan, but future packaging, installer, release, and CI branches must treat it as a public release blocker before any real public AI/runtime distribution claims edition-boundary safety.

## Security Model

### Public Edition Security

Public Edition should eventually use:

- code signing
- signed updates
- signed capability packs
- model/capability-pack integrity checks
- no embedded secrets
- least-privilege local storage
- explicit provider-visible data controls
- explicit consent controls
- clear reset and repair paths
- no hidden network egress

Public Edition cannot rely on public source code secrecy.

Its protection must come from not placing private assets in public, using signed distribution, and keeping privileged services, keys, and private capability packs outside public source.

### Dev Edition Security

Dev Edition should eventually use:

- private repository access controls
- contributor entitlements
- scoped GitHub permissions
- scoped local tokens
- signed/dev-channel builds
- clear Dev identity in UI and logs
- audit logs for repo/GitHub actions
- no owner-private memory
- no unrestricted automation
- no automatic export of user-imported Public data

### Owner Edition Security

Owner Edition should eventually use:

- private repository or local-only source root
- owner-only access control
- local owner vault for secrets
- encrypted private memory where appropriate
- explicit tool permissions
- reversible automation
- strong audit logs
- no public remote for owner branches unless used only as a fetch-only public upstream
- no Owner artifacts in public build outputs

## Learning, Memory, And Training Model

Do not describe the AI as "launch it and train itself."

Future learning should be governed by memory, feedback, retrieval, and evaluation boundaries.

Public Edition may eventually support user-controlled personalization only after explicit consent. It must not inherit Dev or Owner knowledge and must not silently train on user data.

Dev Edition may learn from public repo docs, public issues, public logs selected for debugging, validation outputs, and contributor-scoped context. It must not learn from Owner memory, Owner prompts, Owner strategy, or private Owner logs.

Owner Edition may learn from owner-approved private memory, repo history, governance outcomes, validation outcomes, private product strategy, accepted feedback, and owner-specific workflows. Owner learning must be local/private unless the USER explicitly approves otherwise.

## Release Breakpoints

This section records breakpoints that should stop the project from spending years on Public Edition work while forgetting Dev and Owner.

### Breakpoint 0: Public-Safe Edition Plan

Goal: commit the edition vision and release plan into public-safe source truth.

Required before complete:

- edition names recorded
- trust boundaries recorded
- private repo topology recorded
- Public-to-Dev migration direction recorded
- Owner isolation recorded
- GitHub Desktop setup plan recorded
- future implementation exclusions recorded

Expected carrier: current FAM-007 public branch or the next legal FAM-007 planning carrier.

### Breakpoint 1: Public Leak-Prevention Foundation

Goal: make the public repo ready to prove it does not include private Owner/Dev material.

Required before complete:

- public-safe edition manifest schema planned or implemented
- public repo leak checklist created
- Public Build Exclusion Requirement converted into a validator or build-fail gate where source truth supports it
- validator or audit helper can flag forbidden private paths/patterns where source truth supports it
- public build excludes dev/owner overlays by construction
- docs explain what belongs outside public repo

Recommended timing: within the next one or two FAM-007 branches after this plan is accepted.

### Breakpoint 2: Private Dev And Owner Skeleton Creation

Goal: create the private edition skeletons before public functional AI is complete.

Trigger: after Breakpoint 1 is green and before provider/model execution is released publicly.

Do not wait until Public functional AI is complete before creating Dev and Owner skeletons. Do not begin public provider/model execution until edition boundaries are validator-backed.

Expected outputs:

- private `Nexus-Desktop-AI-Dev` repo or local private skeleton
- private `Nexus-Desktop-AI-Owner` repo or local-only owner skeleton
- public-upstream remote strategy
- private `.gitignore` and secret rules
- private edition manifest placeholders
- private remote rules proving `origin` is private and public repo is `public-upstream`
- no private logic copied to public

This is the clearest "the time is now" breakpoint for creating DEV and OWNER versions.

### Breakpoint 2 Readiness Proof Contract

Breakpoint 2 readiness proof is public-safe planning and validation evidence only. It may prove that the Dev and Owner skeleton decisions are ready to ask for later USER action, but it must not create private repositories, create local-only private roots, configure GitHub Desktop private remotes, copy private files, enable provider/model execution, enable memory, or implement backup/restore.

Dev skeleton readiness proof must show:

- `USER-ACTION-FAM007-DEV-PRIVATE-REPO-CREATE` is the controlling gate before any private Dev repository or local-only private Dev skeleton exists.
- Dev remains trusted but not owner-private.
- Dev must not inherit Owner memory, Owner prompts, Owner strategy, Owner credentials, Owner private automation, Owner private planning, private model/capability assets, or owner roadmap material not approved for public release.
- Dev may later use a private `origin` and a fetch-only `public-upstream` only after USER approves the Dev private repo or local-only path.
- Dev readiness proof remains source-truth and validator proof until USER approves actual private Dev setup.

Owner skeleton readiness proof must show:

- `USER-ACTION-FAM007-OWNER-PRIVATE-REPO-CREATE` is the controlling gate before any Nexus Desktop AI Owner repository, local-only owner root, vault, or owner-hosting posture exists.
- Nexus Desktop AI Owner remains owner-only and may choose private GitHub hosting or a local-only Owner skeleton only by later USER approval.
- Owner prompts, owner-private memory, owner strategy, owner logs/evals, private Codex handoff artifacts, private automation, credentials, private model/capability assets, and owner-specific personalization remain protected by default.
- Owner readiness proof does not authorize Dev or Public inheritance of Owner material.
- Owner readiness proof remains source-truth and validator proof until USER approves actual private Owner setup.

Private repo / local-only action-gate proof must show:

- no private Dev repository was created by the public branch;
- no private Owner repository or local-only owner root was created by the public branch;
- no private remote URL, token, credential, private path, prompt, memory payload, private automation, model artifact, capability-pack asset, or private hosting secret is present in public source truth or public review packets;
- any later private repo or local-only setup must record path/remote proof, secret-scan posture, protected-asset exclusion, and USER-approved hosting posture.

GitHub Desktop private remote safety proof must show:

- `USER-ACTION-FAM007-GITHUB-DESKTOP-PRIVATE-REMOTE-SETUP` is the controlling gate before GitHub Desktop is bound to a private Dev or Owner root.
- Dev and Owner hosted repos must use private `origin`.
- The public repository in private Dev/Owner roots must be named `public-upstream`.
- `public-upstream` must have no push URL, a disabled push URL, or a pre-push guard before private push workflows are trusted.
- GitHub Desktop setup remains planning-only until USER approves actual private remote configuration.

## USER Action Gate Registry

This registry gives future Codex runs durable, searchable identifiers for moments where USER must create, approve, configure, or personally perform an action before work can continue. These identifiers are source-truth gates, not implementation. A branch may mention one of these gates only when it also states the trigger, required USER action, allowed scope, blocked scope, validation proof, and exact approval text.

| Gate ID | Trigger | Required USER Action | Allowed Scope After Approval | Blocked Until Separate Approval | Validation / Proof |
| --- | --- | --- | --- | --- | --- |
| `USER-ACTION-FAM007-DEV-PRIVATE-REPO-CREATE` | Breakpoint 1 is green and Dev skeleton setup becomes the next legal branch candidate. | Create or approve the private Dev repository or approve a local-only private Dev skeleton path. | Private Dev skeleton setup, private origin remote, public-upstream fetch-only remote, Dev edition manifest placeholders, and Dev-only `.gitignore` / secret rules. | Owner private material, provider/model execution, memory import, public artifact publication, public-to-dev import implementation, and public repo leakage. | Private repo/local path proof, remote naming proof, no public push path proof, secret scan plan, and source-truth record of private/public separation. |
| `USER-ACTION-FAM007-OWNER-PRIVATE-REPO-CREATE` | Breakpoint 1 is green and Owner skeleton setup becomes the next legal branch candidate. | Create or approve the private Owner repository, or explicitly choose local-only Owner hosting first. | Nexus Desktop AI Owner skeleton setup, private/local owner root, owner vault planning, private origin remote if hosted, and public-upstream fetch-only remote. | Dev/public inheritance of Owner memory, prompts, strategy, private logs, private automation, credentials, or owner-only model/capability assets. | Private/local path proof, no public remote push proof, owner-private asset exclusion proof, and USER-approved hosting posture. |
| `USER-ACTION-FAM007-GITHUB-DESKTOP-PRIVATE-REMOTE-SETUP` | Dev or Owner private repo/skeleton setup is approved. | Bind GitHub Desktop to the correct private Dev/Owner local path and verify remote names before any push. | GitHub Desktop setup for private repo `origin`; public repo as `public-upstream`; push URL disabled or guarded for public-upstream. | Any push from private Dev/Owner roots to the public GitHub repo, or any public repo remote named `origin` inside private roots. | Git remote proof, GitHub Desktop path proof, no-push-url or pre-push guard proof, and screenshot/manual verification where requested. |
| `USER-ACTION-FAM007-PUBLIC-TO-DEV-MIGRATION-CONSENT` | Public-to-Dev migration work is proposed after private Dev boundary proof exists. | Choose import consent level and approve data classes to copy from Public to Dev. | Copy-only import of approved Public settings, consent state, personalization, selected logs/support data, or separately approved memory. | Importing secrets, tokens, API keys, owner-private data, no-export data, raw private logs, or memory without separate explicit approval. | Consent-level receipt, provenance stamps, copy-not-move proof, reset path, and validation that Public data remains intact. |
| `USER-ACTION-FAM007-PRIVATE-TO-PUBLIC-SANITIZATION` | Any private Dev/Owner work is proposed for public repo import, public artifact inclusion, or public release evidence. | Approve the Private-To-Public Sanitization Gate for the exact candidate files/artifacts. | Sanitized public-safe code, docs, fixtures, or generic patterns after protected asset scan, secret scan, prompt/memory strip, private path scan, model/capability asset scan, private automation scan, source-truth review, and USER approval. | Owner/Dev private prompts, memory, strategy, logs, screenshots, model outputs, automation, credentials, private repo paths, private artifacts, and private release evidence. | PASS sanitization gate or explicit USER waiver naming residual risk. |
| `USER-ACTION-FAM007-OWNER-VAULT-OR-PRIVATE-HOSTING` | Owner Edition requires secrets, private memory, private strategy, or private automation beyond source-truth planning. | Choose local-only Owner vault/private root or approve private GitHub hosting and access rules. | Owner-only local vault planning, private storage root, audit log posture, reversible automation rules, and private backup/hosting posture. | Public repo storage, Dev inheritance of owner-private state, external calls, model execution, or persistent memory runtime until separately approved. | Owner path/hosting proof, access-boundary proof, encryption/vault plan where needed, and no public artifact proof. |
| `USER-ACTION-FAM007-AI-DATA-BACKUP-RECOVERY` | Public, Dev, or Owner AI personalization, memory, private state, or edition recovery work is proposed beyond source-truth planning. | Choose approved off-boot backup/recovery root(s), decide whether Owner also uses private GitHub hosting or local-only backup first, and approve restore-proof expectations. | Planning or implementation for the exact approved backup/recovery seam, including off-boot local backup path, restore test, edition separation proof, and protected-material handling. | Relying only on the OS boot drive, copying private state to the public repo, cross-edition restore, unencrypted secret backup, hidden memory backup, provider/model execution, or private repo creation beyond the approved seam. | Off-boot path proof, restore drill or fixture proof, no public artifact proof, edition-separation proof, encryption/vault plan where private material is present, and USER-approved recovery posture. |
| `USER-ACTION-FAM007-PROVIDER-MODEL-EXECUTION` | A future branch proposes any provider SDK integration, model execution, prompt acceptance, downloads, network calls, or `canAcceptPrompts=true`. | Approve provider/model execution scope, provider-visible data boundary, cost/privacy posture, model/download source, and rollback/disable path. | The exact approved provider/model execution seam only. | Memory/learning, voice/Core sync, installer/shortcut work, private editions, external calls beyond the approved provider path, and public release claims. | Provider-state validation, consent validation, no hidden external calls, provider-visible data proof, and direct runtime proof. |
| `USER-ACTION-FAM007-MEMORY-LEARNING-PERSONALIZATION` | Any branch proposes persistent memory, indexing, retrieval, learning, personalization, or memory import. | Approve memory/data scope, retention/reset/export rules, public/private edition separation, and whether any external training is allowed. | The exact approved memory/indexing/retrieval/personalization seam. | Owner-private memory in Dev/Public, unapproved training, hidden persistence, network egress, provider execution, or public-to-dev memory import without separate approval. | Consent proof, storage-boundary proof, reset/delete/export proof, no hidden indexing, and edition-separation validation. |
| `USER-ACTION-FAM007-PACKAGING-EDITION-IDENTITY` | FAM-008 packaging/install work is ready to name or ship separate Public, Dev, or Owner identities. | Approve app names, install paths, icons, data roots, update channels, signing/channel posture, and GitHub Desktop local path guidance. | Packaging identity planning or implementation for the approved edition/channel only. | Runtime provider/model execution, private repo creation, memory, public artifact publication, release/tag execution, or edition functionality claims outside approved packaging scope. | Installer/shortcut/source proof, distinct data-root proof, signed/update-channel plan, public build exclusion proof, and safety/privacy validation where applicable. |

The first future USER-created private assets are expected to be gated by `USER-ACTION-FAM007-DEV-PRIVATE-REPO-CREATE`, `USER-ACTION-FAM007-OWNER-PRIVATE-REPO-CREATE`, and `USER-ACTION-FAM007-GITHUB-DESKTOP-PRIVATE-REMOTE-SETUP`. Public functional AI must not proceed past provider/model execution gates until these action gates are either completed, explicitly deferred, or waived by USER with recorded risk.

### Breakpoint 3: Public-To-Dev Migration Contract

Goal: define how Public users become Dev users without losing their personalized Public data or accidentally exporting it.

Required before complete:

- separate Public and Dev data roots
- import wizard contract
- copy-not-move rule
- provenance stamping
- no-export defaults
- reset path
- validation plan for imported profiles

### Breakpoint 4: Dev Edition Minimum Viable Runtime

Goal: produce the first useful Dev Edition without owner-private content.

Minimum Dev Edition capabilities:

- separate app identity
- separate data root
- dev-mode source/repo awareness
- issue/log intake with redaction
- validation guidance
- branch/source-truth navigation
- public-upstream sync proof
- no owner-private memory

### Breakpoint 5: Owner Edition Minimum Viable Runtime

Goal: produce the first private Owner Edition after Dev skeleton and Public/Dev boundaries are proven.

Minimum Owner Edition capabilities:

- separate owner app identity
- private owner repo/root
- private memory boundary
- local owner vault/secrets plan
- owner-only Codex handoff support
- private repo/GitHub planning support
- no public export path by default

### Breakpoint 6: Edition Packaging Identity

Goal: coordinate with FAM-008 before real installers or shortcuts exist.

Required before complete:

- install names
- icons
- app IDs
- data roots
- update channels
- signed update model
- private artifact strategy
- GitHub Desktop local path guidance

### Breakpoint 7: v1.8.0-Prebeta Functional AI Gate

Goal: do not jump to `v1.8.0-prebeta` until public AI is functional and edition boundaries are not loose.

Required before complete:

- Public Edition provider setup and consent path is truthful
- provider-visible data boundary is explicit
- `canAcceptPrompts` changes only when approved and validated
- prompt/model execution has direct validator proof
- network/download/memory/voice gates are explicit
- Dev and Owner skeleton strategy exists and is not forgotten
- public release notes do not imply Owner/Dev private functionality is public

## Concrete Branch / Package Sequence

Recommended sequence from this planning point:

1. Public-safe edition plan and PR-gate source-truth repair.
2. Public leak-prevention foundation branch.
3. Private Dev and Owner skeleton setup decision.
4. Public-to-Dev migration contract branch.
5. Public provider execution foundation branch only after setup/consent/data boundaries are ready.
6. Dev Edition MVP private branch.
7. Owner Edition MVP private branch.
8. Packaging/install identity branch through FAM-008.
9. Safety/privacy hardening inside the owning implementation family where secrets, vaults, encryption, and egress controls need implementation.
10. `v1.8.0-prebeta` release readiness only after functional AI and edition boundaries both pass validation.

## Version And Release Channel Direction

Public releases should continue on the public prerelease line until the project is ready for a functional AI version jump.

Private Dev and Owner releases may use private channels and private tags, but those tags must not be treated as public release truth.

Private release notes, private tags, private builds, private capability packs, private model assets, and private artifacts must not be cited as public release evidence or public readiness proof.

| Channel | Audience | Example Naming |
| --- | --- | --- |
| Public prebeta | public users | `v1.7.x-prebeta`, later `v1.8.0-prebeta` |
| Dev private | trusted contributors | private Dev build numbers or private tags |
| Owner private | owner only | private Owner build numbers or local/private tags |

Public release notes should mention only public-safe capability.

Private release notes must stay in private repos or private artifacts.

## Theft And Corruption Prevention Model

The strongest protection is exclusion.

Do not put Owner or Dev private intelligence in public files.

Commercial and technical protections can reduce copying, but a public repo cannot protect private prompts, model assets, secrets, or memory if those are committed.

Protection layers:

1. Keep private material out of public source.
2. Keep private material out of public artifacts.
3. Use private repos for Dev and Owner.
4. Use separate data roots.
5. Use secret scanning before any private-to-public flow.
6. Use signed updates and signed capability packs.
7. Use entitlement checks for private channels.
8. Use local encrypted storage for sensitive memory or secrets.
9. Keep audit logs for automation and private tool use.
10. Use sanitizer gates before any cherry-pick or reimplementation from private to public.

## Validation Direction

Future branches should add validators only when implementation or source truth supports them.

Recommended future validator categories:

- public repo private-material leak audit
- edition manifest schema validation
- data-root separation validation
- Public-to-Dev import fixture validation
- no-owner-export validation
- no-dev-tooling-in-public-UI validation
- provider-visible data boundary validation
- private repo remote sanity checks for Codex/GitHub Desktop handoff packets

This document does not require those validators immediately.

It records them as concrete future proof needs.

## Review Checklist

Before a future branch claims edition-boundary progress, it should answer:

- Which edition is this for?
- Which repo owns it?
- Which data root owns it?
- Which update channel owns it?
- Does it change public runtime behavior?
- Does it expose private prompts, memory, logs, secrets, model assets, or strategy?
- Does it allow Public-to-Dev import?
- Does it keep Owner isolated?
- Does it preserve provider-visible data boundaries?
- Does it preserve consent boundaries?
- Does it require FAM-008 packaging work?
- Does it require safety/privacy hardening in the owning implementation family?
- Does it need a USER review bundle?
- Does it need a new validator?

## Current Pending Decisions

Still pending USER decisions:

- create private Dev repo
- create private Owner repo
- choose exact private local paths
- choose whether Owner repo is private GitHub-hosted or local-only first
- choose off-boot backup/recovery roots for Public, Dev, and Owner AI state
- define restore-proof expectations before persistent AI personalization is treated as durable
- define Dev edition final name before packaging
- implement edition manifests
- extend leak-prevention validators for future private skeleton, backup/recovery, or packaging gates as needed
- implement Public-to-Dev import wizard
- implement memory/personalization
- implement provider/model execution
- implement packaging/installer identity
- implement licensing/activation/security/encryption
- publish any private artifacts
- execute `v1.8.0-prebeta`

## Next Legal Use

Use this plan during future Branch Readiness and Workstream Entry when a branch touches:

- FAM-007 provider/model/memory/capability-pack behavior
- FAM-008 packaging, install, shortcut, update, or data-root identity
- privacy, safety, secret, consent, memory, or egress behavior in the owning implementation family
- GitHub Desktop setup for edition work
- Codex setup for public/private repo separation
- off-boot backup/recovery planning for AI personalization, private state, or reinstall continuity
- Public-to-Dev migration
- Owner-only AI runtime or private memory

This plan should be reviewed before any branch claims that the AI is ready for a public version jump.
