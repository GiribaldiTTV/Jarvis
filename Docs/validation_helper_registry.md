# Nexus Validation Helper Registry

## Purpose

`Docs/validation_helper_registry.md` is the repo-wide registry for validation helpers, live-validation scripts, audit helpers, harnesses, and shared validation support that live under `dev/`.

Its job is to:

- make helper ownership easy for future developers to discover
- prevent one helper per feature or seam by inertia
- standardize helper names and release-readiness expectations
- require reuse, parameterization, or consolidation before new helper creation
- preserve workstream-specific helper exceptions only when they are explicit and temporary or intentionally scoped

`Docs/phase_governance.md` owns the policy.
This registry owns the helper inventory and naming classification.
Canonical workstream docs own the evidence produced by helpers for a specific branch.

## Helper Status Values

Every durable helper or validator under root `dev/` must fit one of these statuses:

- Helper Status: Reusable
- Helper Status: Workstream-scoped
- Helper Status: Temporary probe
- Helper Status: Historical

Definitions:

- `Reusable` means future work should extend or parameterize this helper before creating a new one.
- `Workstream-scoped` means the helper exists for one active workstream because reuse would currently blur proof or behavior boundaries; it must name an owner and consolidation target.
- `Temporary probe` means the file is exploratory only, must stay under an ignored evidence root such as `dev/logs/...`, and must not be committed as closeout-grade tooling.
- `Historical` means the helper is preserved for prior evidence or legacy workflows and is not the default extension point unless explicitly selected.

## Naming Standard

Use these names for new durable validation assets:

- repo-side validator: `dev/orin_<domain>_<capability>_validation.py`
- live desktop helper: `dev/orin_<domain>_<capability>_live_validation.ps1`
- interactive suite: `dev/orin_<domain>_<capability>_interactive_validation.ps1`
- audit helper: `dev/orin_<domain>_<capability>_audit.ps1`
- reusable harness: `dev/orin_<domain>_<capability>_harness.py`
- shared helper module: `dev/orin_<domain>_<capability>_helper.py`

Workstream-scoped exception:

- `dev/orin_<workstream_id>_<bounded_capability>_validation.ps1`
- `dev/orin_<workstream_id>_<bounded_capability>_live_validation.ps1`

Workstream-scoped names must prefer capability words over seam numbers.
Seam-number names are allowed only as a short-lived bridge when the helper was created during a live seam and must carry an explicit consolidation target before PR Readiness.

## Reuse Decision Order

Before creating a new helper, Codex must record or be able to report this decision order:

1. registry lookup by domain and capability
2. use an existing `Reusable` helper unchanged when it already covers the path
3. parameterize or extend the nearest reusable helper in the same helper family
4. extract shared support when two or more helpers need the same watchdog, progress, cleanup, UIAutomation, runtime startup, source snapshot, or artifact-writing behavior
5. create a `Workstream-scoped` helper only when reuse would contaminate proof ownership, blur branch truth, or make validation less reliable
6. use a `Temporary probe` only under ignored evidence roots and delete or promote it before closeout-grade proof

## Required Workstream-Scoped Markers

Every `Workstream-scoped` durable helper must record:

- Helper Status: Workstream-scoped
- Owner Workstream:
- Reason Reusable Helper Was Not Extended:
- Consolidation Target:
- Promotion Decision Point:

Before PR Readiness, each workstream-scoped helper must be resolved in one of three ways:

- folded into an existing `Reusable` helper
- promoted to `Reusable` with this registry updated
- kept as `Workstream-scoped` only with an explicit reason that the helper should remain branch-family-specific after merge

## Registered Root Dev Helpers

### Repo-Wide Governance

| Path | Helper Status | Family | Reuse / Consolidation |
| --- | --- | --- | --- |
| `dev/orin_branch_governance_validation.py` | Helper Status: Reusable | governance validator | Extend when repo-wide source-of-truth, phase, branch, release, helper registry, prompt-contract, Source-Truth Placement Preflight, Element Validation Ledger placement, Element Validation Ledger drift, PR Readiness post-merge source truth, Release Readiness Health Pass rules, `Release Readiness Candidate Anchor` rules, `Release Window Aggregation Ownership` rules, `Origin/Main Freshness Check` rules, `Standing Governance Intake Branch` rules, or `Assigned Worktree Confinement` rules become machine-checkable. It owns `--standing-governance-intake-gate` for `feature/release-readiness-source-truth-intake`, `Release Readiness digest` intake only, `RRI-YYYYMMDD-NNN`, `One Active Cycle`, the pre-intake `Sync Rule`, `Bootstrap Exception Limit`, `Waiting For Governance Intake` / `Waiting For Updated Main`, the required `Return Digest`, `Return Digest Identity Guard`, `Return Digest Origin Identity Missing`, the standing-lane allowance for registered release-readiness validators such as `dev/orin_release_body_validation.py`, and the merged-main `No Active Branch` exception that allows only this standing governance authority record while rejecting all active runtime/implementation/release/repair carriers; it also owns `--worktree-confinement-gate` for `Expected Worktree Root:`, `Actual Worktree Root:`, `No Cross-Worktree Mutation`, `GitHub Desktop-bound worktree`, `Worktree Escape User Waiver Missing`, and `Worktree Escape User Waiver: Granted` validation, `--release-readiness-health-gate` for `Release Candidate Anchor Projection:` and `Release Window Contributor Inventory:`, and `--pr-readiness-gate` for PR Readiness `Branch Creation Base:`, `Current origin/main:`, `Origin/Main Advanced Since Branch Creation:`, `Reconciliation File List:`, `Reconciliation Recommendation:`, and no file fixes during Stage 1. |
| `dev/orin_pr_body_quality_audit.py` | Helper Status: Reusable | GitHub PR body audit helper | Reuse for live GitHub PR body quality audits before creating another PR-body normalizer. It preserves exactly `## Summary`, `## Branch Evidence`, and `## Validation`, removes repeated Summary/Purpose/Overview text from Branch Evidence, rejects phase-digest/operator PR body firewall markers, keeps concise branch-specific boundaries in Branch Evidence, keeps Validation proof-only, writes local before/after backups outside the repo, and can apply normalized bodies through `gh pr edit` when USER-approved. |
| `dev/orin_release_body_validation.py` | Helper Status: Reusable | release body validator | Reuse for GitHub Release body format checks before creating another release-note validator. It validates every published Nexus pre-Beta release body has a concise `Pre-Beta v<major>.<minor>.<patch>` title, starts with `Release Summary` / `Release Overview`, carries rich user-facing sections before generated `What's Changed` and `Full Changelog` content, and excludes internal automation/tooling brand tokens or generated branch-prefix noise from public release notes. |

### Desktop Runtime And Launcher

| Path | Helper Status | Family | Reuse / Consolidation |
| --- | --- | --- | --- |
| `dev/orin_ai_provider_state_validation.py` | Helper Status: Reusable | FAM-007 provider state validator | Reuse for static FAM-007 no-provider/provider-privacy, provider-selection/consent-boundary, disabled Assisted Desktop no-provider interaction, local provider registry/configuration state, provider-visible-data disclosure, hardware/capability planning, capability-pack lifecycle planning, data/memory/consent/audit/secrets planning, Windows resilience planning, persona/Core/voice boundary, validation proof-gate, and no-provider fallback state checks before creating another local-AI/provider-state validator. It now covers local-only/no-provider fallback semantics, visible provider/privacy/selection/consent/registry/configuration/foundation-readiness state, disabled prompt/interaction affordance, no configured or available providers before consent, no hidden external calls, prompt-acceptance gating, no memory persistence/indexing, no model workload execution, blocked capability-pack downloads, disabled voice runtime, and future consent-boundary extension points when later seams are admitted. |
| `dev/orin_desktop_entrypoint_validation.py` | Helper Status: Reusable | desktop startup and entrypoint validator | Extend for non-live startup, tray, overlay-entry, VBS/launcher/runtime launch-chain fallback proof, plain `main.py` direct-launch handoff proof, launch-chain preflight and cleanup isolation, PATH-based Python fallback validation, runtime marker coverage, actual desktop shortcut equivalence proof, generated current-worktree shortcut proof when the real desktop shortcut points at a different governed worktree, `NEXUS_DESKTOP_VALIDATION_SHORTCUT_PATH` override handling, shortcut target/working-directory reporting, real user-operated tray action proof where feasible, tray Exit confirmation/timing proof, active-owner PID identity/stale-reused PID relaunch proof, and per-step Codex precheck manifest support. Fake/callback/offscreen proof must be labeled separately from real-client proof, and generated-equivalent shortcut proof must not be described as true real desktop shortcut proof unless the actual shortcut is aligned or USER waives the mismatch. |
| `dev/orin_desktop_launcher_healthy_validation.py` | Helper Status: Reusable | launcher healthy-path validator | Extend for launcher healthy startup regression coverage. |
| `dev/orin_desktop_launcher_regression_harness.py` | Helper Status: Reusable | launcher regression harness | Repair-gated reusable: current file still references absent legacy `nexus_*` launcher/target paths; repair to current `orin_*` paths or explicitly bypass before using it as launcher regression proof. After repair, extend for launcher scenario regression coverage before creating another launcher harness. |
| `dev/orin_launcher_live_window_audit.ps1` | Helper Status: Reusable | live window audit helper | Extend or parameterize for launcher/window live validation before creating another launcher live audit helper. |
| `dev/orin_overlay_input_capture_helper.py` | Helper Status: Reusable | overlay input helper | Reuse for overlay input-capture support instead of duplicating low-level input helpers. |

### Monitoring And HUD

| Path | Helper Status | Family | Reuse / Consolidation |
| --- | --- | --- | --- |
| `dev/orin_monitoring_hud_surface_validation.py` | Helper Status: Reusable | monitoring HUD surface validator | Reuse for static Monitoring/HUD visual-surface markers, desktop-mode activation, runtime telemetry-boundary markers, renderer-owned placement markers, controls-visibility markers, fail-safe/no-data/degraded-status behavior markers, slice-boundary copy, no-hardware-polling/no-settings-persistence/no-fake-hardware-values/no-recovery-claims/no-voice boundary checks, no expanded retired legacy user-facing identity, Stage 2-R13 Dashboard-first Workstream handoff source-truth markers, Stage 2-R12 Dashboard-first Interface Release Boundary source-truth markers, WS31 Dashboard-only acceptance baseline markers, WS32 Dashboard standalone movement/clipping/Core-Overlay decoupling markers, WS33 Dashboard settings/control content and monitor-group clarity markers, WS34 provider/setup/no-data/degraded truth and warning posture controls markers, WS35 dashboard-specific proof refresh and Live Validation UTS boundary markers, H1 Dashboard-first hardening source-truth markers, Dashboard-specific acceptance/proof separation, Stage 2-R11 dashboard-versus-minimal-HUD architecture expectations, WS18/WS30 Core desktop-layer/non-blocking ownership markers, WorkerW coordinate-rebase proof, no Core topmost foreground ownership, WS19-WS35 historical/supporting markers, and Overlay/display deferred/non-gating proof classification before creating another HUD surface validator. |
| `dev/orin_monitoring_hud_live_validation.ps1` | Helper Status: Reusable | monitoring HUD live desktop validator | Workstream/Hardening/Live Validation helper for FAM-006 Monitoring HUD proof. Reuse for Dashboard-first WS31+ live proof, WS32 dashboard standalone travel/clipping/decoupling proof, WS33 dashboard settings/control content and monitor-management clarity proof, WS34 provider/setup/no-data/degraded truth and warning posture controls proof, WS35 dashboard-specific full virtual-desktop screenshot proof plus Live Validation UTS boundary proof, H1 Dashboard-first hardening pressure-test proof, LV1 Stage 1 active-client proof plus formal UTS handoff, launched-desktop marker proof, Core desktop-layer/non-interference runtime markers, Dashboard/Overlay/Core independence evidence, raw PNG evidence copies under `C:\Users\anden\OneDrive\Pictures\Screenshots\Nexus Desktop AI\fam_006_monitoring_hud_live_validation\<stamp>\`, `-RunInteractionSelfQA` live HUD control exercise, `-ActiveUserFacingClient` foreground/user-observable validation, interaction manifest output, no-progress watchdog, millisecond artifact-root uniqueness, cleanup verification, Dashboard-first self-QA that does not require Overlay/display unanchor/card-drag/card-resize acceptance, real-client proof-class separation, per-step Codex Precheck PASS/FAIL/NOT TESTED/WAIVED output in manifests/source truth, compact USER-questionnaire UTS generation, and future Overlay/display proof only when that interface is re-admitted or USER grants explicit interface-bundle approval. Formal `C:\Users\anden\OneDrive\Desktop\User Test Summary.txt` export is exclusive to Live Validation Stage 1 and requires `-PrepareLiveValidationUserTestSummary`; it must stay a short step-based questionnaire with closing additions, while issue ledgers, proof-class detail, helper internals, and broad traceability digests stay in manifests/source truth. Workstream and Hardening proof runs must not refresh or digest UTS. Helper success, fake/offscreen state, callback proof, screenshots, marker proof, and generated-equivalent shortcuts must not be collapsed into real user-operated tray proof or true actual-desktop-shortcut proof unless the actual shortcut targets the active worktree or USER explicitly waives the mismatch. Remaining gaps before package-complete claims: returned UTS acceptance or waiver digestion, PR Readiness, and final package closeout. |
| `dev/orin_monitoring_hud_human_client_validation.ps1` | Helper Status: Active / Required before FAM-006 LV1 handoff | monitoring HUD human-client desktop validator | WS48/WS49+ helper for the actual USER-like path. Launches the canonical red FAM-006 desktop shortcut `C:\Users\anden\OneDrive\Desktop\FAM-006 RED - Nexus Desktop AI Launcher.lnk` by default or a governed `NEXUS_DESKTOP_VALIDATION_SHORTCUT_PATH` equivalent when USER approves an override, resolves the shortcut target and working directory before launch, records `shortcutResolution`, and requires `shortcut_targets_active_worktree=PASS` so the helper fails fast if the shortcut is not rooted in the active FAM-006 worktree at `C:\Nexus Worktrees\FAM-006`. It uses visible Windows tray/menu actions, exact native tray menu item rectangles by label, broadened tray icon resolution, mouse/cursor click/drag evidence, Dashboard open/close/move/resize checks, real-shortcut first-open screenshot-sequence proof for #123 recurrence with visual-continuity analysis, Dashboard IA-card Settings open/Done close proof, Settings double-click native-maximize guard proof, window-level Dashboard Close hide/reopen proof, Dashboard rounded-corner native-mask proof by placing a white validation backdrop behind the Dashboard and sampling the native window corner exterior pixels to catch black rectangular corner bleed, rounded-mask-clipped resize hit-test proof so transparent clipped corners cannot be over-credited as usable resize rails, normal-speed Dashboard move-fluidity proof with native GetWindowRect position sampling, pre-click Windows resize-cursor discovery with user-like mouse-move stimulation before cursor sampling, central 50 percent rounded-corner diagonal resize-zone proof, native GetWindowRect high-cadence resize sampling, cursor-to-window tracking-lag thresholds, high-refresh cadence proof, NCP tray icon left-click open/close proof, tray menu Open/Close Command Overlay state proof, Command Overlay closeout before resize proof, Dashboard repositioning away from the lower-right tray menu cleanup zone after intentional resize enlargement, NCP Create Custom Task/Create Custom Group/Manage Custom Tasks/Manage Custom Groups clicks while Dashboard is visible/moved, tray Create Custom Task duplicate-dialog guard proof, visible shutdown-confirmation check, timeout/cancel/accept proof, virtual-desktop screenshot-frame artifacts, fallback cleanup for non-UIA dialogs, and a JSON manifest at `dev/logs/fam_006_human_client_validation/latest_manifest.json`. Tray menu actions must resolve inside the native tray popup or exact native menu-coordinate fallback so in-app buttons cannot be over-credited as tray proof; issue #140 requires the helper to prove NCP tray icon toggle and tray Open/Close state before PR Readiness. This helper is Workstream/Hardening proof infrastructure only; it must not generate or digest the formal UTS. The Live Validation helper must not export a green UTS unless this human-client manifest is PASS with shortcut/worktree alignment, Settings/window-level Close/rounded-corner mask/first-open visual-continuity/normal-speed movement/high-refresh resize-fluidity proof, NCP tray toggle/state proof, or USER explicitly waives the missing proof. |
| `dev/orin_dashboard_rounded_corner_mask_probe.py` | Helper Status: Active / Called by FAM-006 human-client validation | Dashboard rounded native-window mask probe | Subhelper for issue #137 and later Dashboard rounded-corner regressions. It receives the live Dashboard HWND from the real red-shortcut human-client validation path, places a temporary white backdrop behind the Dashboard, brings the Dashboard forward, captures a virtual-desktop bitmap artifact, samples native window corner-exterior pixels and visible Dashboard interior pixels, and fails if corner samples are dark/opaque rather than showing the white backdrop. This exists so CSS-rounded marker proof cannot over-credit a still-rectangular native window. |
| `dev/orin_monitoring_hud_internal_sandbox_validation.py` | Helper Status: Reusable | monitoring HUD internal sandbox validator | Use for FAM-006 internal product proof. Validates Dashboard-first Workstream handoff posture, WS31 Dashboard-only acceptance baseline posture, WS32 Dashboard standalone movement/clipping/Core-Overlay decoupling posture, WS33 Dashboard settings/control content and monitor-group clarity posture, WS34 provider/setup/no-data/degraded truth and warning posture controls, WS35 dashboard-specific proof refresh and Live Validation UTS boundary, H1 Dashboard-first hardening pressure-test posture, LV1 Stage 1 handoff posture, LV2 explicit USER waiver digestion posture, the standalone HUD shell/module files, ORIN Core render-file isolation, dashboard-specific settings/control behavior, provider-truthful telemetry contracts, 1s polling floor, visual warning posture, no fake GPU/thermal values, retired-name sterilization, and Overlay/display deferred/non-gating classification without treating User Test Summary results as a Workstream or Hardening gate. Historical WS18-WS30 markers remain supporting repair evidence, not current Dashboard acceptance by themselves. Remaining gaps before package-complete claims: PR Readiness and final package closeout. |

### Shared Action, Interaction, And Saved Actions

| Path | Helper Status | Family | Reuse / Consolidation |
| --- | --- | --- | --- |
| `dev/orin_shared_action_baseline_validation.py` | Helper Status: Reusable | shared action baseline validator | Extend for shared action catalog and resolution baseline checks. |
| `dev/orin_interaction_baseline_validation.py` | Helper Status: Reusable | interaction baseline validator | Extend for typed-first overlay, confirm/result, and command interaction baseline checks. |
| `dev/orin_saved_action_source_validation.py` | Helper Status: Reusable | saved-action source validator | Extend for saved-action source loading, corruption, and source safety checks. |
| `dev/orin_saved_action_authoring_validation.py` | Helper Status: Reusable | saved-action authoring validator | Extend for non-UI saved-action authoring and validation behavior. |
| `dev/orin_saved_action_authoring_ui_validation.py` | Helper Status: Reusable | saved-action authoring UI validator | Extend for Qt/dialog authoring behavior that can be proven without a full live desktop session. |
| `dev/orin_saved_action_authoring_live_validation.py` | Helper Status: Reusable | saved-action authoring live validator | Extend for saved-action authoring live proof that does not require the larger interactive PowerShell suite. |
| `dev/orin_saved_action_authoring_interactive_validation.ps1` | Helper Status: Reusable | saved-action authoring interactive suite | Extend for full saved-action authoring interactive desktop coverage before creating another authoring live suite. |
| `dev/orin_saved_action_authoring_interactive_runtime.py` | Helper Status: Reusable | saved-action authoring interactive runtime support | Reuse as support for the interactive authoring suite. |
| `dev/orin_callable_group_execution_validation.py` | Helper Status: Reusable | callable-group validator | Extend for deterministic callable-group execution checks. |
| `dev/orin_callable_group_execution_interactive_validation.ps1` | Helper Status: Reusable | callable-group interactive suite | Extend for callable-group interactive proof before creating another callable-group live helper. |

### External Trigger Intake

| Path | Helper Status | Family | Reuse / Consolidation |
| --- | --- | --- | --- |
| `dev/orin_external_trigger_intake_validation.py` | Helper Status: Reusable | external trigger intake validator | Extend for FB-039 trigger intake, registration, lifecycle state transitions, decision evidence snapshots, boundary state snapshots, readiness inspections, registry readiness sweeps, registry readiness summaries, registry readiness detail snapshots, bounded invocation follow-through, malformed-input pressure tests, blocked-category precedence, duplicate non-mutation, result immutability, and negative-path checks before creating another external-trigger helper. |

### Toolkits, Boot, Diagnostics, Support, And Voice

| Path | Helper Status | Family | Reuse / Consolidation |
| --- | --- | --- | --- |
| `dev/orin_boot_monitor_preflight.py` | Helper Status: Reusable | boot preflight | Extend for boot monitor preflight checks. |
| `dev/orin_boot_toolkit_validation.py` | Helper Status: Reusable | boot toolkit validator | Extend for boot toolkit validation. |
| `dev/orin_boot_transition_capture.py` | Helper Status: Reusable | boot transition capture | Extend for boot transition capture rather than creating duplicate capture helpers. |
| `dev/orin_boot_transition_verification.py` | Helper Status: Reusable | boot transition verification | Extend for boot transition verification. |
| `dev/orin_desktop_toolkit_validation.py` | Helper Status: Reusable | desktop toolkit validator | Extend for desktop toolkit validation. |
| `dev/orin_dev_toolkit_smoke_validation.py` | Helper Status: Reusable | dev toolkit smoke validator | Extend for dev toolkit smoke checks. |
| `dev/orin_diagnostics_report_issue_validation.py` | Helper Status: Reusable | diagnostics issue validator | Repair-gated reusable: current file still references legacy `nexus_diagnostics.pyw`; repair to current `orin_diagnostics.pyw` or explicitly bypass before using it as diagnostics issue/report proof. After repair, extend for diagnostics issue/report validation. |
| `dev/orin_recoverable_launch_failed_validation.py` | Helper Status: Reusable | recoverable diagnostics validator | Extend for bounded recoverable launch-failed diagnostics. |
| `dev/orin_startup_snapshot_harness_validation.py` | Helper Status: Reusable | startup snapshot validator | Extend for startup snapshot harness validation. |
| `dev/orin_support_bundle_triage_toolkit_validation.py` | Helper Status: Reusable | support triage toolkit validator | Extend for support bundle triage toolkit validation. |
| `dev/orin_support_bundle_triage.py` | Helper Status: Reusable | support triage helper | Reuse for support bundle triage logic. |
| `dev/orin_support_bundle_triage_harness.py` | Helper Status: Reusable | support triage harness | Extend for support bundle triage harness coverage. |
| `dev/orin_voice_regression_harness.py` | Helper Status: Reusable | voice regression harness | Extend for voice-path regression coverage. |

### Utilities And Manual Support

| Path | Helper Status | Family | Reuse / Consolidation |
| --- | --- | --- | --- |
| `dev/orin_seeded_saved_action_review.ps1` | Helper Status: Reusable | saved-action seeded review | Reuse for seeded saved-action review support. |

### Active Workstream-Scoped Helpers

| Path | Helper Status | Owner Workstream | Reason Reusable Helper Was Not Extended | Consolidation Target | Promotion Decision Point |
| --- | --- | --- | --- | --- | --- |
| `dev/orin_fb038_seam2_validation.ps1` | Helper Status: Workstream-scoped | FB-038 | Created as a deterministic seam runner while Python/PySide6 path availability was failing; it coordinates existing reusable validators rather than replacing them. | Retained as FB-038 release/PR evidence only. If a later branch needs deterministic validator orchestration, fold the runner semantics into documented validator invocation guidance or a reusable validation runner before creating another seam runner. | PR Readiness decision: keep Workstream-scoped after merge because it preserves FB-038 evidence without becoming the default reusable validation entrypoint. |
| `dev/orin_fb038_seam2_live_validation.ps1` | Helper Status: Workstream-scoped | FB-038 | Created to prove tray-origin Create Custom Task dialog-open/no-write behavior without overloading the broader FB-036 interactive suite mid-Workstream. | Retained as FB-038 tray/Create Custom Task evidence. Future tray-origin authoring work must first consolidate this flow into a reusable tray live validation helper or into `dev/orin_saved_action_authoring_interactive_validation.ps1`. | PR Readiness decision: keep Workstream-scoped after merge; do not promote until a second branch needs the same tray-origin authoring proof. |
| `dev/orin_fb038_seam3_live_validation.ps1` | Helper Status: Workstream-scoped | FB-038 | Created to prove tray-origin create completion, catalog reload, exact-match re-resolution, and cleanup while keeping Seam 3 separate from Seam 2 no-write proof. | Retained as FB-038 tray-origin create-completion evidence. Future create-completion work must consolidate with the Seam 2 helper into a reusable tray/Create Custom Task live helper or fold the scenario into the saved-action interactive suite. | PR Readiness decision: keep Workstream-scoped after merge; do not promote until future branches prove the flow is reusable beyond FB-038. |

## Admitted Future Helper Families

These reservations do not register files that do not yet exist. They record the reuse order and expected names for already-admitted future work so a later implementation branch does not invent helper families ad hoc.

### Sensor HUD Beta

- Reuse order first: extend `dev/orin_desktop_entrypoint_validation.py` for tray and overlay entry coverage before creating a new Sensor HUD entry validator.
- Reuse order second: extend `dev/orin_interaction_baseline_validation.py` for command-overlay Sensor HUD intents before creating a new interaction-path helper.
- If a future implementation branch still needs new durable helpers after that reuse check, use `dev/orin_sensor_provider_validation.py` for provider contract, merge and dedup, stale-state, fallback, pause and resume, polling, and effective-rate proof.
- If a future implementation branch still needs new durable helpers after that reuse check, use `dev/orin_sensor_hud_layout_validation.py` for layout persistence, rematch, unresolved-placeholder behavior, search, pinning, categorization, and serialized card state proof.
- If a future implementation branch still needs new durable helpers after that reuse check, use `dev/orin_sensor_hud_live_validation.ps1` for tray actions, Sensor HUD open and edit behavior, pause and resume, lock and edit interaction, and live desktop proof.
- Provider-specific probes remain `Temporary probe` assets unless and until they are promoted through this registry with an explicit status and reuse story.

## Release / PR Standard

Before a branch reports PR Readiness green:

- all new root `dev/` validation helpers must be registered here
- workstream-scoped helpers must carry the required markers above
- temporary probes must be deleted or promoted
- any helper that is kept after merge must have a clear status and reuse/consolidation story
- release notes or closeout text must reference reusable helper families by capability, not by ad hoc seam-only names, unless the seam helper is intentionally preserved as workstream-scoped evidence
- `dev/orin_branch_governance_validation.py --release-readiness-health-gate` must prove post-merge source truth through the `Release Readiness Health Pass` before PR creation or merge approval; the owning record must include `Post-Merge Branch Authority Projection:`, `Stale Active Branch Wording Scan:`, `Stale PR Creation / PR Readiness Pending Wording Scan:`, `Merged-Unreleased Scope Posture:`, `Release Execution Gate:`, `Watcher / Live PR State Projection:`, `Branch Cleanup Plan:`, `Branch Cleanup Execution Gate:`, `FAM Overlap Routing:`, `Release Candidate Anchor Projection:`, `Release Window Contributor Inventory:`, and `Projected Post-Merge Validation:` after any Stage 2 or bot-review source-truth repair. `Branch Cleanup Execution Gate:` keeps stale/old branch cleanup, worktree removal, branch switching, and GitHub Desktop-bound worktree cleanup out of Release Readiness; cleanup belongs to `Branch Readiness Stage 2 - Execution Gate` after `Stale Branch Cleanup Plan:`, branch/worktree creation or validation, `git worktree list`, and replacement target proof show no repository will lose its valid branch target. Release Readiness itself must declare `Release Candidate Anchor:`, `Release Candidate Anchor Source:`, `Target Commit:`, `Historical Endpoint Handling:`, `Candidate Includes Later Governance Repairs:`, `Release Ownership Model:`, `Release Window Contributors:`, `Merged-Unreleased Scope Inventory:`, `Last Runtime PR:`, `Post-Runtime Governance Repairs:`, and `FAM Contributor Routing:` and must stop on `Release Candidate Anchor Missing` or `Release Window Contributor Inventory Missing` when those values are absent or ambiguous.
- `dev/orin_branch_governance_validation.py --standing-governance-intake-gate` must prove the single `Standing Governance Intake Branch` is on the correct branch/worktree contract, has clean tracked state, uses a `Release Readiness digest` intake only, carries at most `One Active Cycle` with `RRI-YYYYMMDD-NNN`, satisfies the pre-intake `Sync Rule`, preserves `Waiting For Governance Intake` / `Waiting For Updated Main`, restricts changed files to governance/source-truth/validator scope, permits the standing authority record as the only active-record exception under merged-main `No Active Branch`, requires the post-merge `Return Digest`, and enforces `Return Digest Identity Guard` / `Return Digest Origin Identity Missing` so the returned originating-lane prompt cannot default to the wrong worktree or branch
- `dev/orin_branch_governance_validation.py --worktree-confinement-gate` must prove `Assigned Worktree Confinement` for the active branch record by comparing `Expected Worktree Root:` to `Actual Worktree Root:`, preserving `No Cross-Worktree Mutation`, proving the `GitHub Desktop-bound worktree`, and failing on `Worktree Escape User Waiver Missing` unless USER has explicitly recorded `Worktree Escape User Waiver: Granted` with scope, expiration, validation, and return path.
- `dev/orin_branch_governance_validation.py --pr-readiness-gate` must require PR Readiness Stage 1 `Origin/Main Freshness Check` source truth with `Branch Creation Base:`, `Current origin/main:`, `Origin/Main Advanced Since Branch Creation:`, `Origin/Main Changed Files:`, `Branch Changed Files:`, `Reconciliation Required:`, `Reconciliation File List:`, `Reconciliation Recommendation:`, and `Reconciliation Mutation Status:`; when upstream changes require review, `Origin Main Reconciliation Packet Required` blocks Stage 2 and PR creation until Stage 1 outputs the complete reconciliation data and recommendation with no file fixes during Stage 1.
- `dev/orin_branch_governance_validation.py` source-checks the Branch Readiness `Carrier Lifecycle Decision` contract across governance docs. The packet must include `Carrier Lifecycle Classification:`, `Remote Branch State:`, `Unique Branch Diff:`, `Origin/Main Ancestry:`, `Origin/Main Advanced Since Branch Creation:`, `Open PR State:`, `Worktree Checkout State:`, `Recommended Stage 2 Carrier Action:`, `Stale Branch Cleanup Plan:`, `Branch Cleanup Execution Gate:`, `Recreate From Current origin/main:`, and `No Unique Commit Loss Proof:`, and the classification vocabulary is limited to `Fresh current branch`, `Stale empty local branch`, `Stale branch with unique commits`, `Historical merged branch`, `Wrong carrier/worktree`, and `Active remote/open PR branch`.
