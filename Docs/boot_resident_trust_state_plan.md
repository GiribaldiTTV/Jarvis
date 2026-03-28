# Jarvis Resident Trust-State Surfacing Plan

## Purpose

This document defines the next planning slice for Jarvis trust and recovery behavior after desktop entry on a consumer Windows machine.

This is a planning artifact only.
It does not choose tray implementation, backend logic, auth storage behavior, shell integration, renderer wiring, diagnostics presentation behavior, or notification-system implementation.

Its purpose is to define:

- what resident trust-state surfacing is for after login
- what trust states should conceptually exist after desktop entry
- how those trust states should feel and appear at product level
- how recovery-needed state should be visible without becoming intrusive
- how recovery entry should remain reachable after login
- how the resident Jarvis layer should act as a trust and recovery anchor after boot entry is complete

## Relationship To Prior Boot Planning

This planning slice builds directly on:

- `FB-015 rev1a` phase-boundary clarification
- `FB-004 rev1a` boot entry-chain and handoff-topology planning
- `FB-004 rev1b` boot login, fallback, recovery, and resident-presence planning
- `FB-004 rev1c` trust-model planning
- `FB-004 rev1d` auth-factor planning
- `FB-004 rev1e` routine auth UX planning
- `FB-004 rev1f` stronger-path planning

It carries forward these rules:

- Jarvis owns presentation
- real authentication owns trust
- typed input remains the certainty path
- voice may support presence but never replace trust or recovery completion
- Windows-safe fallback must always exist
- post-bypass recovery should feel supportive, not punitive
- the resident layer is distinct from the boot-time login flow

This slice narrows only the post-login surfacing of trust state and recovery entry.

## Product-Level Objective

After desktop entry, Jarvis should remain visibly present as the user’s trust and recovery anchor without behaving like a constant warning system.

The resident trust-state layer should feel:

- calm during normal operation
- visible when trust continuity is degraded
- clear when recovery is needed
- supportive when action is required
- distinctly Jarvis in tone and framing
- low-friction for everyday consumer Windows use

It should not feel:

- punitive
- enterprise-administrative
- noisy
- alarmist by default
- like a second login screen that never ends

## Why Resident Trust-State Surfacing Exists

Boot-time login is the entry moment.
Resident trust-state surfacing is the continuity layer after entry.

Its job is to ensure that Jarvis trust and recovery state remain understandable after the user reaches the desktop, especially when:

- normal trust continuity is intact
- trust continuity has degraded
- recovery entry is available or recommended
- Jarvis needs to guide the user back toward a healthy trust state

This resident layer should answer a simple product question:

"After I am in Windows, how does Jarvis keep me informed about my access and recovery state without becoming disruptive?"

## Resident Layer Role After Desktop Entry

At planning level, the resident Jarvis layer should be treated as:

- the persistent trust-state anchor after login
- the home for trust and recovery status visibility
- the place where recovery entry remains available
- the post-login continuation of Jarvis presence
- the place where degraded or recovery-needed state can be surfaced without forcing immediate interruption

This role is conceptually distinct from:

- boot-time login presentation
- boot-time trust completion
- launcher-owned desktop startup control
- diagnostics presentation behavior

## Core Resident Trust States

At planning level, the resident layer should recognize these post-login trust states:

- normal trust state
- degraded trust state
- recovery-needed state

These states exist to communicate trust continuity and recovery posture, not to add hidden control authority over the desktop.

## Normal Trust State

Normal trust state means:

- the user completed normal Jarvis access successfully
- trust continuity still feels intact
- no immediate recovery action is needed
- Jarvis can remain present without asking for attention

Normal trust state should feel:

- calm
- reassuring
- ambient rather than attention-seeking
- available if the user wants to inspect status

The user should be able to infer:

- Jarvis access is healthy
- no recovery action is currently needed
- Jarvis remains available as a trusted resident presence

## Degraded Trust State

Degraded trust state means the system no longer considers the current Jarvis trust posture fully normal, but the situation does not yet need to behave like an emergency.

At planning level, degraded trust state conceptually includes situations where:

- normal trust continuity was interrupted
- recent access used a fallback or bypass path
- a recovery-relevant condition exists even though desktop entry is already available
- the system should not behave as if everything is fully normal

Degraded trust state should feel:

- noticeable
- more explicit than normal background presence
- informative rather than alarming
- action-oriented without becoming hostile

The user should be able to infer:

- something about Jarvis trust continuity needs attention
- desktop use may continue
- recovery entry is available and should be easy to reach

## Recovery-Needed State

Recovery-needed state is the clearest action-requiring resident trust state.

At planning level, recovery-needed state means:

- Jarvis should actively surface that trust restoration is needed
- the user should not have to hunt through settings to find the recovery path
- the system should make recovery entry obvious without turning it into punishment

Recovery-needed state should feel:

- clear
- finite
- guided
- supportive
- meaningfully different from normal state

It should not feel:

- accusatory
- shaming
- panic-oriented
- like the machine is broken beyond use

## What The User Should Be Able To See In Each State

### Normal Trust State

The user should be able to see or access:

- that Jarvis is present
- that trust state is healthy if they inspect it
- a path into settings or status surfaces later

Normal state should not demand active attention by default.

### Degraded Trust State

The user should be able to see or access:

- that the current trust posture is not fully normal
- a clear explanation at product level that trust continuity needs attention
- a visible recovery entry path
- a way to defer immediate action without losing the ability to recover later

### Recovery-Needed State

The user should be able to see or access:

- that recovery is recommended or required for Jarvis trust restoration
- a clear recovery entry point
- supportive language about restoring access
- a stable path back into recovery later if they do not act immediately

## Recovery Entry After Login

Recovery entry should remain reachable after desktop entry through the resident Jarvis presence.

At planning level, this means:

- recovery entry must remain discoverable after login
- recovery entry must not depend on remembering a boot-only path
- recovery entry must not depend on voice alone
- recovery entry should feel like part of Jarvis care and continuity rather than punishment

The resident layer should conceptually support both:

- proactive recovery surfacing when trust is degraded
- user-initiated recovery entry when the user chooses to address it later

## How Recovery Should Be Surfaced

Recovery-needed state should be surfaced in a way that is:

- visible enough to notice
- easy to return to later
- supportive in tone
- bounded in urgency

It should avoid:

- aggressive interruption
- hostile warning language
- guilt framing
- persistent harassment during ordinary desktop use

At planning level, the product direction should be:

- make recovery obvious
- make recovery reachable
- make recovery understandable
- do not make recovery oppressive

## Typed And Voice Relationship In The Resident Layer

Typed input remains the certainty path in the resident trust-state layer.

Typed interaction must always remain sufficient for:

- checking trust-related status
- entering recovery from the resident layer
- completing recovery-oriented actions that depend on resident access surfaces
- navigating trust or recovery-related control surfaces after login

Voice may support:

- explanatory framing
- presence
- supportive guidance
- optional reminders

Voice must not:

- be required to access recovery entry
- be required to understand current trust state
- replace trust-restoration actions
- become the only path into resident trust or recovery surfaces

## How Resident Trust-State Surfacing Differs From Boot Login

The boot flow is about entry.
The resident layer is about continuity after entry.

The resident trust-state layer should therefore differ from boot-time login in these ways:

- it is persistent rather than entrance-focused
- it is status-aware rather than ceremony-driven
- it supports recovery entry without behaving like a fresh login screen
- it should be lighter during normal use
- it should become more visible only when trust continuity is degraded or recovery is needed

This resident layer should not recreate the emotional posture of boot-time authentication every time the user is already inside Windows.

## Normal Background Presence Versus Degraded Presence

Normal background trust presence should be:

- low-noise
- calm
- inspectable
- non-demanding

Degraded presence should be:

- more visible than normal
- clearer about what needs attention
- still bounded and non-punitive

The key distinction is:

- normal state reassures
- degraded state informs
- recovery-needed state guides

## In-Bounds Resident Trust-State Patterns

The following are in-bounds at planning level:

- calm normal-state surfacing
- clearly visible degraded-state surfacing
- guided recovery-needed surfacing
- resident recovery entry that remains reachable after login
- typed-sufficient status and recovery access
- Jarvis-framed supportive language
- a resident trust/control anchor that stays distinct from the boot login flow

## Out-Of-Bounds Resident Trust-State Patterns

The following should be treated as out-of-bounds for this planning slice:

- constant warning posture during normal use
- punitive or shaming recovery language
- voice-only recovery entry
- forcing the resident layer to behave like a repeated login ceremony
- hiding recovery entry behind deep settings hunting
- turning post-login trust surfacing into enterprise-style compliance monitoring
- using resident trust-state surfacing to introduce new launcher or shell authority

## Explicit Deferrals For Later Revisions

This slice intentionally defers:

- tray implementation details
- exact resident UI mechanics
- backend trust-state logic
- auth storage behavior
- shell integration
- renderer wiring
- notification-system implementation
- diagnostics presentation behavior
- exact recovery timing rules
- exact recovery-prompt persistence rules
- implementation of post-bypass detection

## Risks And Blockers

### Trust Risks

- making degraded state too subtle for users to notice
- making recovery-needed state too soft to act on
- blurring normal and degraded trust posture together

### UX Risks

- making post-login trust surfacing too noisy
- making recovery feel like punishment
- making normal use feel monitored instead of supported

### Planning Risks

- mixing resident-state planning with tray implementation too early
- mixing resident trust surfacing with diagnostics redesign
- collapsing post-login trust status and boot-time login back into one oversized flow

## What Success Looks Like

A successful resident trust-state plan would make the user feel:

- Jarvis is still present after I enter the desktop
- normal access feels calm and unobtrusive
- if trust continuity degrades, I can tell without feeling attacked
- if recovery is needed, I know where to go
- I can recover through Jarvis after login without hunting for it
- Jarvis is helping me restore trust, not punishing me

## Recommended Next Planning Step After This Slice

After this resident trust-state baseline, the next coherent planning revision should narrow one of:

- resident recovery-entry persistence and deferral behavior
- resident control-center or settings-anchor responsibility planning
- consumer environment/setup preference surfacing after install and first run
