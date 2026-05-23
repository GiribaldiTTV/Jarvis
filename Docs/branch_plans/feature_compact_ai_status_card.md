# Compact-AI Status Card Branch Engineering Plan

## Branch Runtime Engineering Plan

Plan Identity: `feature_compact_ai_status_card`

Owning Branch: `feature/compact-ai-status-card`

Worktree Path: `C:\Nexus Worktrees\Compact-AI-Status-Card`

Branch Authority Record Pointer: `Not present before salvage; this branch plan owns active rebaseline intent evidence for the Compact-AI salvage PR path.`

Current Phase: `Rebaseline Overlap Intent Gate repair before PR creation`

Branch Runtime Engineering Plan: `Accepted Compact-AI salvage plan for preserving the compact Core provider-status card behavior and desktop-mode suppression while reconciling against updated origin/main.`

Engineering Plan Status: `Accepted`

Current Runtime Baseline: `The branch started before the Governance/FAM fold-down baseline and carries Core visual CSS plus provider-state validator changes that overlap current origin/main runtime and validator surfaces.`

Branch Purpose: `Preserve the two unique Compact-AI commits by carrying their compact provider-status-card and desktop suppression behavior into the current main baseline through a reviewed PR.`

Planned Runtime Delta: `Keep the Core visual provider-status card compact, bounded, overflow-safe, validation-owned for detailed provider posture, and hidden in desktop mode through CSS while preserving the fail-closed provider gates.`

User-Facing Delta: `Core visual mode keeps a smaller provider status card instead of exposing the full detailed card; desktop mode hides that card so the desktop shell is not cluttered by provider readiness internals.`

Source-Truth Delta: `This plan records branch-owned overlap intent for the Compact-AI branch because current origin/main introduced the Rebaseline Overlap Intent Gate after the branch was created. It also folds the older Compact-AI protected unique-commit receipt forward so source truth no longer treats the salvaged commits as still waiting outside main after this PR.`

State / Config / Schema Delta: `No state, config, or schema changes are planned; provider setup, activation, consent, execution, network, memory, model, and release gates remain unchanged and disabled where current source truth requires them.`

Validator / Helper Delta: `The provider-state validator should prove the compact/hide CSS contract so the UI remains compact while detailed provider state remains represented in validation instead of expanded desktop UI. Source-owner marker validation wording should preserve Compact-AI protection as historical evidence and recognize this salvage/fold-down path.`

Expected Changed Files / Surfaces: `dev/orin_ai_provider_state_validation.py; nexus_visual/orin_core.css; nexus_visual/orin_core_desktop.css; Docs/branch_records/feature_repo_wide_source_owner_marker_adoption.md; Docs/validation_helper_registry.md; dev/orin_source_owner_marker_validation.py; dev/orin_validation_suite.py; this branch plan evidence file.`

Workstream / Seam Map: `Single Compact-AI salvage seam: reconcile the compact provider status card and desktop-card suppression with current origin/main after overlap evidence is recorded.`

Per-Seam Implementation Checklist: `Inspect overlap; record Branch Change Intent Ledger; merge current origin/main; resolve CSS and validator conflicts by preserving compact-card behavior plus current provider-state validation requirements; fold down the old Compact-AI protected-unique-commit receipt into a salvage/fold-down receipt; validate; PR; merge after review.`

Per-Seam Validation Checklist: `Run rebaseline audit with this plan path, git diff checks, provider-state validation, branch governance validation, governance efficiency validation, source-owner marker validation, release-body validation, AI provider-state validation, and compileall as applicable after reconciliation.`

Per-Seam User-Facing Proof Checklist: `Static CSS/validator proof is acceptable because this salvage keeps the provider status surface compact or hidden and does not add new runtime execution behavior.`

Future-Gated Items: `Provider setup, provider activation, consent collection, model execution, external calls, memory/indexing, broad Core visual redesign, release work, issue mutation, branch cleanup, and successor branch creation remain separate USER decisions.`

Approval-Boundary Audit: `USER approved fixing the two unique Compact-AI commits and getting them PR'ed and merged. This plan does not authorize release work, provider/model/runtime execution, or unrelated file cleanup.`

FAM / Shared-Surface Overlap Forecast: `Overlap exists with current origin/main in provider-state validator and Core visual CSS surfaces; this plan records intent before rebaseline mutation and keeps FAM-006/FAM-007/Governance work separate.`

Open Questions: `None blocking; conflicts during rebaseline must preserve current provider gates and compact desktop posture.`

USER Planning Decisions: `USER approved carrying the two unique Compact-AI commits forward, PR creation, and merge after validation/reviewable proof.`

Plan Revision History: `2026-05-22 - admitted branch-owned overlap intent evidence after the rebaseline audit reported missing Branch Change Intent Ledger evidence for the preserved Compact-AI branch.`

Plan-To-Implementation Traceability Table: `Compact status card -> nexus_visual/orin_core.css and nexus_visual/orin_core_desktop.css -> provider-state validator proof -> Compact-AI protected receipt fold-down -> source-owner marker validator wording -> PR review and merge.`

Hardening Comparison Checklist: `Confirm compact status card does not imply functional AI readiness, provider execution, consent, setup, or external calls; confirm desktop mode hides the card; confirm validation still proves provider gates.`

Live Validation Proof Or Waiver Checklist: `Static proof waiver accepted for this salvage path unless a visual run is requested; no provider/model execution is introduced.`

PR Readiness Fold-Down / Retention Checklist: `PR body and final digest should preserve the two original commit subjects, changed files, validation proof, old protected posture, folded salvage posture, and this plan path as temporary overlap evidence.`

Release Readiness Public-Scope Translation Checklist: `No release execution in this branch; if later released, public wording should describe compact provider-status visual cleanup only, not functional AI readiness.`

USER Planning Review: `Accepted by USER instruction to fix the two unique Compact-AI commits and get them PR'ed and merged.`

PR Fold-Down Packet: `Pending PR creation and merge; preserve compact branch receipt in PR body and merge digest.`

Runtime Implementation Approval: `Approved for the bounded Compact-AI status-card salvage only.`

## Branch Change Intent Ledger

### Changed Surface: dev/orin_ai_provider_state_validation.py

- Surface Class: `validator/helper`
- Change Intent: `Add validator proof that the compact Core provider-status card and desktop-mode status-card suppression remain intentional while provider setup and execution stay gated.`
- Why This File Was Touched: `The branch adds validator assertions for the CSS contract so compacting/hiding the provider card remains checked instead of becoming an unproven visual tweak.`
- Owned Behavior / Fact Class: `Provider-state visual contract validation and fail-closed provider readiness proof.`
- Canonical Owner / Source Owner: `dev/orin_ai_provider_state_validation.py`
- Resolution Owner: `Current Branch`
- Shared Surface: `Yes - current origin/main also changed this validator during FAM-007/Governance provider-state hardening.`
- Overlap Risk: `High because validator/helper overlap can change release gating and provider-state proof.`
- Expected Conflict Risk: `Medium because current origin/main added provider-state validations after this branch forked.`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `High`
- Conflict Resolution Rule: `Preserve current origin/main provider-state coverage and add only the compact-card/desktop-hide assertions needed for this branch.`
- Rebaseline Handling: `Merge current origin/main after this ledger is committed, resolve conflicts manually if present, and rerun provider-state and governance validation.`
- Validation Proof: `Validation not run before rebaseline mutation; required validation includes python dev\orin_ai_provider_state_validation.py plus governance validators after reconciliation.`
- Fallback Evidence: `Original Compact-AI commits ac16ca37 and 2f2354db plus current diff; fallback evidence is classification support and not a compatibility bypass.`
- USER Decision / Waiver: `USER approved fixing the two unique Compact-AI commits and getting them PR'ed and merged.`
- Fold-Down Target: `PR body and final merge digest compact receipt.`

### Changed Surface: nexus_visual/orin_core.css

- Surface Class: `runtime`
- Change Intent: `Compact the Core visual provider-status card so detailed provider readiness stays validator-backed without dominating the visible Core surface.`
- Why This File Was Touched: `The branch narrows and bounds the provider status card, hides most detailed rows, adds overflow protection, and leaves a compact validation-held-details note.`
- Owned Behavior / Fact Class: `Core visual provider-status presentation contract.`
- Canonical Owner / Source Owner: `nexus_visual/orin_core.css`
- Resolution Owner: `Current Branch`
- Shared Surface: `Yes - current origin/main also changed Core visual provider-state surfaces.`
- Overlap Risk: `High because runtime CSS overlap can produce text-clean but visually wrong behavior.`
- Expected Conflict Risk: `Medium because current origin/main changed adjacent provider visual rules.`
- Semantic Merge Risk: `Medium`
- Regression / Gating Impact: `Low`
- Conflict Resolution Rule: `Preserve current origin/main provider-state selectors and add compact-card constraints without weakening provider setup/execution gate copy.`
- Rebaseline Handling: `Merge current origin/main after this ledger is committed, preserve compact-card selectors, and rerun provider-state validation.`
- Validation Proof: `Validation not run before rebaseline mutation; required validation includes CSS diff inspection and python dev\orin_ai_provider_state_validation.py after reconciliation.`
- Fallback Evidence: `Original Compact-AI commits ac16ca37 and 2f2354db plus current diff; fallback evidence is classification support and not a compatibility bypass.`
- USER Decision / Waiver: `USER approved fixing the two unique Compact-AI commits and getting them PR'ed and merged.`
- Fold-Down Target: `PR body and final merge digest compact receipt.`

### Changed Surface: nexus_visual/orin_core_desktop.css

- Surface Class: `runtime`
- Change Intent: `Hide the provider-status card in desktop mode so provider readiness internals do not clutter the desktop shell.`
- Why This File Was Touched: `The branch adds the desktop-mode suppression rule where desktop-specific Core CSS can own the desktop presentation override.`
- Owned Behavior / Fact Class: `Desktop-mode Core visual provider-status visibility contract.`
- Canonical Owner / Source Owner: `nexus_visual/orin_core_desktop.css`
- Resolution Owner: `Current Branch`
- Shared Surface: `Yes - current origin/main also changed desktop Core visual provider surfaces.`
- Overlap Risk: `High because desktop-mode CSS overlap can silently reintroduce hidden provider status UI.`
- Expected Conflict Risk: `Low because the intended selector is small and desktop-specific.`
- Semantic Merge Risk: `Low`
- Regression / Gating Impact: `Low`
- Conflict Resolution Rule: `Preserve current origin/main desktop CSS and add only the desktop-mode provider-status suppression rule.`
- Rebaseline Handling: `Merge current origin/main after this ledger is committed and verify desktop CSS retains the suppression selector.`
- Validation Proof: `Validation not run before rebaseline mutation; required validation includes python dev\orin_ai_provider_state_validation.py after reconciliation.`
- Fallback Evidence: `Original Compact-AI commits ac16ca37 and 2f2354db plus current diff; fallback evidence is classification support and not a compatibility bypass.`
- USER Decision / Waiver: `USER approved fixing the two unique Compact-AI commits and getting them PR'ed and merged.`
- Fold-Down Target: `PR body and final merge digest compact receipt.`
