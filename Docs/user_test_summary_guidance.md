# User Test Summary Guidance

## Purpose

This document defines how Nexus Desktop AI uses User Test Summary (`UTS`) handoff.

`UTS` is a Live Validation validation-contract layer.
Formal User Test Summary export and returned-results digestion are exclusive to Live Validation Stage 1.
User Test Summary is exclusive to Live Validation Stage 1.
Live Validation Stage 1 cannot enter Live Validation Stage 2 until User Test Summary results are `PASS` or `WAIVED`, Codex has digested the result into source truth, and blockers have been reevaluated.
Live Validation Stage 1 cannot enter Stage 2 until User Test Summary results are `PASS` or `WAIVED`, Codex has digested the result into source truth, and blockers have been reevaluated.

`UTS` is not:

- a backlog field
- a roadmap field
- a separate tracking system

## Ownership Model

Use this ownership split:

- workstream doc = why later user validation matters, how it fits the lane, and the `User Test Summary Strategy` / Live Validation readiness expectations for that workstream
- `Docs/user_test_summary_guidance.md` = the structure and handling rules for the handoff
- response-level `## User Test Summary` = Live Validation Stage 1 user-facing handoff copy, not Workstream or Hardening completion evidence
- returned `UTS` evidence = user validation input that must be digested before recommending the next move

Docs-only passes that do not require user-run validation normally do not need a `UTS`.

When a Workstream task changes user-visible behavior or another operator-facing path, Codex must keep a `User Test Summary Strategy` or later Live Validation readiness note current unless manual testing is not materially relevant.
Workstream and Hardening must not create, refresh, digest, or treat the formal desktop `User Test Summary.txt` export as phase evidence.
The formal `## User Test Summary` handoff and returned-results gate belong to `Live Validation Stage 1` after the user-facing shortcut or equivalent entrypoint gate is ready.

## Canonical Repo Artifact Rule

For active desktop workstreams, the default canonical repo-level UTS planning surface before Live Validation is:

- the `## User Test Summary Strategy` section inside the relevant canonical workstream doc under `Docs/workstreams/`

The exact formal `## User Test Summary` artifact is created or refreshed only during Live Validation Stage 1 unless USER explicitly grants a waiver or a different Live Validation handoff path.

When a Workstream slice changes user-visible behavior or another operator-facing desktop path, Codex must normally keep later UTS needs current without treating returned user results as a Workstream gate:

- include a detailed `User Test Summary Strategy` or Live Validation readiness plan in the response or output when manual validation will be relevant later
- update the canonical repo-level UTS strategy for the active workstream in the same branch
- defer the final worktree-specific local USER hub UTS handoff export until `Live Validation Stage 1`

Response-only UTS strategy text is not sufficient when the canonical repo artifact exists and the supporting docs for that workstream are in scope.
The formal returned-results blocker must not be listed while the current phase is `Workstream`.

If the canonical repo artifact is not updated, Codex must say explicitly why. The normal allowed reasons are:

- no meaningful manual test exists for the slice
- no canonical workstream doc exists yet, so there is no active repo-level `UTS` owner to update
- the user explicitly restricted the pass so the supporting workstream doc or declared repo artifact could not be changed
- the relevant workstream doc already says that no separate ongoing `UTS` artifact remains for that closed lane
- the desktop export is not relevant because the slice is not a desktop or user-facing manual-validation path

## When A User Test Summary Is Needed

Plan a `UTS` when the active workstream needs later user-run validation, especially for:

- launch or relaunch flows
- UI or visual confirmation
- user-visible interaction or UX changes
- startup, first-run, or reopen behavior
- prompts, inline messaging, or operator-facing guidance changes
- voice behavior
- create, edit, recovery, or other manual operator-facing workflows
- Dev Toolkit helpers
- repaired runtime paths
- bounded regression checks after an approved slice

## Output Requirement For Codex Responses

When manual validation is relevant, `## User Test Summary` in a Codex response must be a true manual test checklist, not a recap.

The default checklist must include:

- setup or prerequisites
- exact user actions
- expected visible behavior
- failure signs to watch for
- branch-specific or slice-specific validation focus

If the work changes multiple user-visible paths, the checklist should separate those paths explicitly enough that the user can run them one by one.

If no meaningful manual test exists, Codex must still include `## User Test Summary` and say explicitly:

- that no meaningful manual test is required for this slice
- why manual validation is not materially relevant
- what was validated instead

## Required Structure

When a `UTS` is needed, structure it around:

- `Test Purpose`
- `Scenario / Entry Point`
- `Steps To Execute`
- `Expected Behavior`
- `Failure Conditions / Edge Cases`
- `Validation Evidence Expectations`

Keep the steps concrete and action-oriented.
Make the expected outcome specific enough that the user can tell what passed or failed.

A recap-style behavior summary is not sufficient when the user needs to run or verify anything manually.

## Local USER Hub File Rule

When a durable USER-facing copy is needed during Live Validation Stage 1, use a worktree-specific file in the local USER hub:

- `C:\Nexus USER\UTS - <worktree-label>.txt`

That worktree-specific local USER hub file is the required user-facing exported copy for relevant desktop Live Validation Stage 1 runs.
It is not Workstream or Hardening evidence. It prevents multiple active worktrees from overwriting, stale-reading, or returning another worktree's UTS evidence.

The global local USER hub file is template-only:

- `C:\Nexus USER\User Test Summary.txt`

When present or generated, the global file must clearly state `TEMPLATE ONLY` and must not be used for active returned results. Active UTS handoff, USER return, and digestion must name the worktree-specific file, such as `C:\Nexus USER\UTS - FAM-006.txt`.

Create or refresh the worktree-specific file by default when:

- Live Validation Stage 1 is admitted for a desktop user-visible behavior or another desktop operator-facing path
- the user is likely to test outside the chat window
- the validation flow is long enough that a durable copy helps
- Dev Toolkit launch metadata must be preserved exactly

If the slice is not a relevant desktop manual-validation path, Codex may skip the local USER hub export only if it says so explicitly and explains why.

Helpers and validators that generate or check active UTS handoffs must fail if the active export path equals `C:\Nexus USER\User Test Summary.txt`. Generated active UTS content must identify the worktree label, branch, and active FAM/workstream identity before it can be returned to USER.

## Required USER Hub File Sections

When the local USER hub file is created or refreshed, prefer this structure:

- `Workstream`
- `What This Test Is Checking`
- `Expected Outcome`
- `Test Steps`
- `Observed Results`
- `New Ideas / Requests Raised During Testing`
- `Questions / Confusions Raised During Testing`
- `Regression Notes`

If a step expects user feedback, include an explicit response slot directly under that step.

## Dev Toolkit Metadata Rule

For Dev Toolkit runs, copy these fields exactly as shown in the UI:

- `Launch Mode`
- `Purpose`
- `Test / Helper`
- `Delay`

Do not paraphrase or shorten those labels.

## Digest Rule After Submission

When the user returns a filled `UTS`, Codex must digest it before recommending the next move.

That digest should separate:

- what passed
- what failed
- what remained unclear
- what new ideas or requests appeared
- what belongs to the current workstream
- what should be deferred

## User Test Summary Results Blocker

Named blocker:

- `User Test Summary Results Pending`

Definition:

- Live Validation Stage 1 must not enter Live Validation Stage 2 while a relevant user-facing workstream has a required `UTS` handoff outstanding and returned results have not been submitted and digested.
- Live Validation green requires an exact `## User Test Summary` state before final green.
- Every Live Validation digest must include an exact `## User Test Summary` section. If User Test Summary is waived, the digest section must still declare `User Test Summary Results: WAIVED` and `User Test Summary Waiver Reason:`.
- Workstream must not use `User Test Summary Results Pending` as its completion blocker; it must continue implementation, internal sandbox validation, or named implementation repair until Workstream completion is otherwise green or legally blocked.
- PR Readiness may verify the previously digested Live Validation UTS state, but it must not create, refresh, or digest UTS as its own phase artifact.

Required authority-record marker:

- `User Test Summary Results: PENDING`
- `User Test Summary Results: PASS`
- `User Test Summary Results: FAIL`
- `User Test Summary Results: WAIVED`

While results are pending, Codex must report:

- Automated validators and live helper evidence: GREEN.
- User Test Summary Results: PENDING.
- Final phase advancement is BLOCKED until the filled User Test Summary is submitted and digested.

Lift condition:

- the filled `UTS` is submitted or a documented waiver exists
- the returned results or waiver are digested into the active authority record
- blockers are reevaluated after digestion

Routing after digestion:

- if returned results pass, clear `User Test Summary Results Pending` and allow forward progression only if all other gates pass
- if returned results expose mismatch, regression, unclear behavior, cleanup failure, or scope drift, route back to `Workstream` or `Hardening` as appropriate
- if returned results raise new ideas or requests, keep them out of current scope until carry-forward is explicitly approved

If Live Validation, USER-gated Live Validation, or returned UTS evidence finds defects after a prior Hardening pass, returned USER validation cannot certify the stale pre-repair Hardening state. The next USER-facing handoff or digest must show the final post-repair LV proof, the post-LV-repair Hardening rerun, and any required LV reconfirmation before it can ask USER to accept final green. If any piece is missing, keep USER validation pending or blocked rather than treating helper/validator green as acceptance.

The desktop export is not considered returned evidence by itself. It is the Live Validation handoff artifact; the blocker remains active only in phases where formal UTS results are required until filled results come back or a waiver is documented.

## User-Facing Shortcut Live Validation Gate

For relevant desktop user-facing workstreams, User Test Summary handoff is downstream of final Live Validation through the user's actual desktop entrypoint.
Validators, live helpers, synthetic harnesses, and direct runtime launches may build supporting evidence, but they do not replace this final shortcut gate when the shortcut path is feasible.

Before User Test Summary handoff, the active authority record must declare:

- `User-Facing Shortcut Path:`
- `User-Facing Shortcut Validation: PENDING`
- `User-Facing Shortcut Validation: PASS`
- `User-Facing Shortcut Validation: FAIL`
- `User-Facing Shortcut Validation: WAIVED`

Named blockers:

- `User-Facing Shortcut Validation Pending`
- `Exact USER Desktop Launcher Proof Missing`
- `Launcher Parity Proof Missing`

The expected default path for Nexus Desktop AI desktop work is:

- `C:\Users\anden\OneDrive\Desktop\Nexus Desktop Launcher.lnk`

The active authority record may instead declare a worktree-local normal runtime launcher when the branch needs LV proof for an active worktree and that launcher is created, repaired, and validated under the normal worktree launcher rule below.

The gate is green only when the declared exact normal USER desktop runtime launcher launches the active branch, reaches ready state, exposes the relevant user-visible surface, and leaves cleanup/persisted-state evidence consistent with the workstream validation contract before User Test Summary handoff.
For desktop user-facing branches, the exact normal USER desktop runtime launcher path is mandatory unless USER explicitly waives it. A troubleshooting launcher or documented equivalent entrypoint may satisfy this gate only when the authority record and proof manifest record USER consent plus `Launcher Parity Proof: PASS`, including tray/menu/window behavior, or when USER explicitly waives the exact launcher requirement.
If the branch's declared worktree-local normal runtime launcher is missing, Live Validation may create or repair that launcher before User Test Summary handoff. The launcher must target the active branch's normal product runtime entrypoint and working directory, must not enable troubleshooting mode, must not target a validation helper or diagnostic-only entrypoint, and must not create installer, startup-registration, packaging, update, or persistent OS integration behavior. The authority record must declare `Normal Worktree Launcher Creation: CREATED`, `Normal Worktree Launcher Path:`, `Normal Worktree Launcher Target:`, `Normal Worktree Launcher Arguments:`, and `Normal Worktree Launcher Validation: PASS` before that launcher can clear the gate.
Compatibility wording: the legacy phrase `actual desktop shortcut path is mandatory when feasible` means the exact normal USER desktop runtime launcher path is mandatory unless USER explicitly waives it or an approved launcher parity proof makes an alternate launcher legal for the exact claim.
For desktop UI Live Validation, a sandbox/offscreen/direct-runtime/WebView/helper path is never the primary UTS path. Those paths may supply supporting coverage only; the LV1 handoff must identify the exact normal USER desktop runtime launcher evidence as the USER-facing path unless USER waiver or launcher parity proof makes an alternate launcher legal for that exact claim.
Shortcut equivalence must not be inferred from helper success alone. Static proof, sandbox proof, fake/offscreen model proof, callback-only proof, active-client screenshot proof, and real user-operated tray proof are separate proof classes and must be labeled separately when the UTS asks the USER to test real tray or desktop operations.
When Live Validation or UTS asks the USER to validate a claim that Codex cannot objectively prove, the handoff must label the claim instead of burying the limitation. Each such row must include `Claim:`, `Claim Class:`, `Minimum Proof Strength:`, `Evidence Provided:`, `Known Limitation:`, and either `Manual USER Validation Required`, `USER Waiver Required`, or a named blocker. Subjective UX, visual-quality, trust/comfort, private-boundary confidence, or unphotographable behavior claims cannot be marked green by helper PASS, marker PASS, screenshot path, manifest path, or Codex confidence wording alone.
UTS handoff for branches with a `Vision-To-Proof Matrix` must present or reference the matrix rows that still need USER attention. If Codex objectively adjudicated a row, the handoff must name the evidence and verdict. If Codex could not objectively adjudicate a row, the handoff must name the accepted requirement, what proof was gathered, why it is insufficient for final acceptance, and the exact USER validation or waiver being requested. USER acceptance is not implied by the matrix existing, by a ZIP being generated, or by helper/validator PASS output.
Before a Live Validation Stage 1 UTS handoff can be marked green for a desktop UI step, Codex must record a per-step precheck manifest using `Codex Precheck: PASS`, `Codex Precheck: FAIL`, `Codex Precheck: NOT TESTED`, or `Codex Precheck: WAIVED`. If Codex did not test the step through the same USER-facing path or a proven/waived equivalent, the UTS step must say `Codex Precheck: NOT TESTED` and LV1 cannot claim a green handoff without explicit USER waiver.
If the gate is `PENDING`, keep `User-Facing Shortcut Validation Pending` active.
If the gate is `FAIL`, route back to `Workstream` or `Hardening` before exporting final-green `UTS` posture.
If the gate is `WAIVED`, the waiver must state why the branch is not desktop/user-facing or why the shortcut path is explicitly unavailable.

## Codex Live Client Self-QA Gate

For relevant desktop user-facing workstreams, User Test Summary handoff is also downstream of Codex's own live-client self-QA.
Validators, markers, screenshots, synthetic harnesses, and helper launches may support the evidence trail, but Codex must still inspect the launched UI like a user before asking the USER to run formal acceptance.

Before User Test Summary handoff, the active authority record must declare:

- `Codex Live Client Self-QA: PENDING`
- `Codex Live Client Self-QA: PASS`
- `Codex Live Client Self-QA: FAIL`
- `Codex Live Client Self-QA: WAIVED`
- `Visual Quality:`
- `Codex Visual Adjudication:`
- `Visual Artifact Review Scope:`
- `Product Vision Alignment:`
- `Per-Element Visual Verdicts:`
- `Helper Marker Limitation:`
- `Unacceptable UI Findings:`
- `LV1 Handoff Disposition:`
- `Live Interaction Evidence:`
- `Usability Check:`
- `Platform Uniformity Check:`

Named blocker:

- `Codex Live Client Self-QA Pending`

The gate is green only when Codex records a live-client review of readability, placement, visual quality, NDAI uniformity, interaction posture, naming cleanliness, cleanup, evidence quality, and product-vision alignment from the launched user-facing path or an explicitly equivalent path.
Screenshot-only or marker-only proof is not enough. Codex must exercise the same visible user-facing interactions it would ask the USER to test, record `Live Interaction Evidence:`, and include an interaction manifest or equivalent evidence when the work adds an interactive UI surface.
For desktop UI, Codex must also perform a failure-seeking visual adjudication pass over the focused proof artifacts before UTS handoff. That pass must compare every acceptance-critical screenshot or frame sequence against the Product Definition Plan, Runtime Branch Engineering Contract, latest USER vision/UTS feedback, package-level UI/UX intent, and any applicable Future-Proof Implementation Review, then record per-element `PASS`, `REPAIR`, `STOP`, or `WAIVED_WITH_REASON` verdicts. Helper PASS, marker PASS, screenshot existence, and manifest existence cannot clear visual acceptability by themselves.
If Codex can see clipped text, unclear workflow hierarchy, weak hover/click affordance, missing open/disabled/danger/empty/error proof, native/basic controls where Nexus styling is required, unreadable density, confusing window flow, or package-vision mismatch, LV1 must route back to Workstream or Hardening before asking the USER to accept the handoff.
If the UTS asks the USER to right-click a tray icon, open or close a window through a tray menu, confirm shutdown, move/resize a visible window, or verify a visible state transition, Codex must precheck that same user-facing operation through the exact normal USER desktop runtime launcher path or an approved parity/waiver path. Fake windows, hidden clients, direct callbacks, and offscreen model assertions can support implementation confidence but cannot be recorded as the sole PASS for the same USER-facing step.
For desktop UI, the Live Validation helper must offer an active foreground/user-observable mode; a fast hidden or blink-through run may support automation evidence but does not satisfy USER-visible active-client validation.
For desktop UI with tray/menu/window operations, app-side precheck code that calls tray handlers directly is not a human-client pass. A green LV1 handoff requires a human-client manifest or explicit USER waiver. The manifest must show visible desktop shortcut launch, visible tray/menu selection, mouse/cursor or UIAutomation-backed click evidence, visible window state evidence, screenshot or frame-sequence artifacts, and Codex inspection of visual/UI quality for every issue-grounded UTS item. If this evidence is missing, the UTS must not be exported as green and the branch routes back to Workstream or Hardening.
For desktop UI Live Validation, screenshots plus short video proof are mandatory for every acceptance-critical interactive or transient state. The short video may be an MP4 evidence reel generated from ordered focused screenshots or a live frame sequence, but it must be a durable media artifact referenced by the manifest. Screenshot existence alone, manifest text alone, or a single final static state cannot satisfy this gate. If a helper cannot create or cite short video/frame-sequence proof for a relevant UI path, the LV1 handoff is `FAIL` / `REPAIR`, not waiverable by Codex.
For desktop UI Live Validation, every acceptance-critical element/state also needs a detailed focused screenshot copied to `C:\Users\anden\OneDrive\Pictures\Screenshots\Nexus Desktop AI\<validation-lane>\<timestamp>\focused_element_screenshots\`. Each PNG filename must include the element label/name and the state or action, for example `element_overlay_profile_settings_window_profile_dropdown_open_hover.png`. Full-desktop screenshots are locator/context evidence only; they do not satisfy the per-element screenshot requirement.
The LV1 manifest must list the USER-inspectable per-element screenshot folder and each per-element image path. If proof exists only in `dev\logs`, if filenames do not identify the element, if only full-desktop screenshots are present, or if an issue-grounded element has no focused screenshot, the handoff is `REPAIR` before USER testing.
The LV1 manifest must include a proof-class summary for short video or frame-sequence evidence. The required minimum is: the declared user-facing shortcut/human-client proof has screenshot artifacts and short video/frame-sequence proof; the Codex live-client self-QA proof has focused screenshots and short video/frame-sequence proof; every issue-grounded UTS item that depends on hover, open menu, click, scroll, resize, flicker, clipping, transition, confirmation, or dirty-guard movement is represented by at least one screenshot and at least one ordered frame/video proof artifact.
For broad or multi-issue UTS repair, the handoff must include or reference the active `Scope Coverage Manifest`. USER language such as all text, every button, the whole window, all dropdowns, multiple issues, or a numbered issue set expands the proof scope. Codex must show the atomic targets or element groups, proof reviewed for each, and final disposition before returning a green UTS handoff.
If UTS review, screenshot/video proof, or Codex live-client adjudication exposes drift against a newly merged Project Vision, FAM-002, UIREF, Family Vision, FFV, proof, packet, or helper/validator standard that could affect existing branch work beyond the immediate LV defect, the branch must route through the `Rebaseline Adoption & Reconciliation Phase` before claiming renewed LV/UTS green. The RAR packet or active external ledger must identify affected owned surfaces, code-to-visual trace rows, accepted-reference comparison, current-branch repair candidates, previous/historical issue candidates, and the USER packet path when USER decisions are needed. LV may continue after the RAR trigger is resolved, waived, or routed to approved issue candidates; it must not silently narrow broad visible drift to one repaired control.

RAR-triggered LV review must use non-circular visual proof. Helper green, validator green, marker files, manifest existence, attractive screenshots, or prior branch acceptance cannot by themselves prove adoption of a newly merged UIREF, Project Vision, FAM-002, proof, or packet standard. The RAR/LV handoff must compare rendered screenshots, video, or ordered frames against the applicable shared primitive, implementation template, or accepted reference set; code-to-visual trace; backend/state ownership; Vision-To-Proof Matrix; the NDAI Product Experience Contract; and USER visual judgment where required. It must not claim template usage or shared primitive consumption unless the actual approved template or primitive source is named. If no template or primitive exists, the handoff must classify the work as reference-derived and prove comparative synthesis against accepted references. If an owned surface is `UNPROVEN`, `PARTIAL`, `NONCONFORMING`, `REFERENCE GAP`, `TEMPLATE GAP`, `SHARED PRIMITIVE GAP`, or `SOURCE-TRUTH GAP`, the UTS handoff remains blocked or routes to an explicit USER decision instead of returning green.
If RAR/LV/UTS evidence proposes, consumes, supersedes, or depends on a same-class Reference Standard candidate, the handoff must name the `Reference Candidate Sync Review` result. External candidate records, aggregate sync reports, or collision reports are evidence only; they are not promoted source truth, USER visual acceptance, implementation-template authority, shared-primitive authority, FAM adoption proof, or issue-creation authority. An unresolved same-class collision, candidate treated as canon, or promoted reference moved outside repo source truth blocks final-green LV/UTS handoff until routed through Workstream, Hardening, RAR, or explicit USER decision.
When a UTS or LV handoff claims a user-facing surface is acceptable, the digest must name the applicable deterministic, intuitive, immersive, predictable, reliable, and consistent expectations or state that a quality is not applicable with reason. A final statement such as "looks good" or "validation passed" is not enough for a surface governed by the NDAI Product Experience Contract unless the proof maps the visible result and backend/state truth to the accepted contract.

When a UTS or LV handoff claims a user-facing surface is future-proof enough for the current branch, the digest must identify the current feature, foreseeable same-class additions, derivation rule, extension boundary, future-gated items, and proof evidence. A default screenshot, one-state proof, or hand-tuned pixel adjustment cannot satisfy this claim unless the branch records why that value is stable, source-owned, and proven across relevant states. If the proof exposes a template, shared primitive, reference, source-truth, implementation, or reference-effectiveness gap, LV/UTS must route back to Workstream, Hardening, RAR, or USER decision rather than asking USER to accept final green by implication.

UTS final acceptance language must not stop at `looks good`, `seems fine`, `appears okay`, `validator passed`, or `screenshot exists`. Those statements are observations only until mapped to accepted vision, element group, focused screenshot/video or manual USER validation, known limitation, and disposition.
If the gate is `PENDING`, keep `Codex Live Client Self-QA Pending` active.
If the gate is `FAIL`, route back to `Workstream` or `Hardening` before exporting final-green `UTS` posture.
If the gate is `WAIVED`, the waiver must state why the branch is not user-facing or why the live client path is explicitly unavailable.

## Carry-Forward Approval Rule

Ideas surfaced through a returned `UTS` must not be silently added to:

- `Docs/feature_backlog.md`
- roadmap sequencing
- canonical planning docs

until Codex provides:

- a concise evidence digest
- extracted ideas
- any recommended refinement
- a clear recommendation for where the idea belongs

and the user explicitly approves the carry-forward.

## Self-Validation Before Handoff

Before giving the user a manual `UTS` handoff for a runtime or UI path, Codex must run the exact normal USER desktop runtime path when the branch is desktop/user-facing, or record the explicit waiver, approved launcher parity proof, or blocker that keeps that path from being formal proof.

For relevant desktop or operator-facing slices, if the implemented path can be launched and exercised through a real desktop session in the current environment, Codex must treat that interactive OS-level session as the default self-validation gate before recommending normal continuation.

If that is not possible, Codex must say:

- what was self-validated
- what was helper-validated only
- what still requires user-only validation
- why the gap could not be closed locally

When the current validation surface is too thin to support that self-validation, Codex must add or create the smallest reliable supporting validation artifacts on-branch first when feasible.

Examples include:

- new or extended validators
- harnesses or scripted helpers
- fixtures or reproducible sample inputs
- runtime logs, traces, or screenshots
- other durable evidence artifacts needed to prove what was actually exercised

Codex must preserve an evidence trail for that self-validation and distinguish clearly between:

- validator results
- synthetic or headless validation results
- simulated reasoning or code-inspection findings
- interactive OS-level executed-path results
- user-only manual handoff that still remains

## Workstream Internal Validation Rule

For runtime, UI, startup, prompt, voice, or other operator-facing implementation slices, the required validator suite is only one layer of validation.

Codex must also perform deeper branch-local internal validation before claiming Workstream completion or continuing past a risky user-facing seam. That pass should:

- inspect the implemented path for likely failure modes and integration regressions
- add or create the smallest reliable validation infrastructure when meaningful blind spots remain
- use supporting validation artifacts when needed, such as harnesses, fixtures, scripted helpers, runtime logs, traces, screenshots, or reproducible sample inputs
- use synthetic or headless validators and harnesses as supporting proof rather than the final continuation gate when a real desktop session is feasible
- launch and exercise the exact normal USER desktop runtime path through an interactive OS-level session when applicable, or record the explicit waiver/blocker that keeps it from being formal proof, rather than stopping at simulated reasoning or headless proof
- preserve evidence of what was run, what passed or failed, and where the supporting artifacts live
- produce an explicit judgment about whether the next move is:
  - continue implementation
  - pause for hardening or internal validation
  - or make a corrective fix first

Green validators plus simulated reasoning, response-level summary text, and synthetic/headless harness results are not enough when the implemented path can still be exercised through a real interactive desktop session.

If that interactive path is not feasible, Codex must explain why, use the strongest available non-interactive evidence, and state that the continuation judgment is limited by the missing interactive validation.
