# FAM-008 Packaging And Install Experience Vision

## Purpose

This family vision records durable product direction for installer, shortcuts, packaged app experience, model/capability-pack install boundaries, update flow, patch/repair behavior, restart continuity, and user-facing setup lifecycle.

## Vision Summary

Packaging and install work should make Nexus easier to install, launch, update, patch, repair, restart, resume, and understand without silently changing system startup, provider, model, or capability-pack state.

## Accepted Direction

- Installer and shortcut behavior must be explicit, reversible, and validation-backed.
- Capability-pack installation should stay separate from the base app unless USER accepts a package boundary.
- Public, Dev, and Owner edition install identities, data roots, update channels, and GitHub Desktop/source-root setup should follow the edition trust-boundary plan before packaging work creates real artifacts.
- Setup should explain trust, privacy, provider, and disk/network implications before enabling heavier capabilities.
- FAM-008 should eventually support a self-maintaining app lifecycle: install, update, patch, restart, repair, rollback, and return-to-operating-state flows that avoid repeated manual installer downloads when a safer patch path exists.
- Update and patch behavior should preserve user data and restore ORIN / Owner AI continuity where safe, so long-running assistance can resume after a governed restart instead of requiring manual reinstall babysitting.
- Patch and restart flows should make interruption, state preservation, rollback, and recovery posture visible to USER before disruptive action.
- Cache-root and clear-cache UX belongs here only as setup/install/user-education direction for approved cache owners; it must not imply provider/model execution, memory, or hidden capability-pack downloads.
- First-run AI orientation should explain local-only, no-provider, provider-assisted, disabled, and privacy-blocked states before asking for sensitive capability consent.
- Capability-pack setup should make storage, network, hardware, license, integrity, update, removal, and cache/index implications visible before installation.
- Clear-cache UX should explain what operational cache is cleared, what is not cleared, and which cache categories may rebuild later; it must not claim to delete memory, Trust Journal entries, logs, backups, or separately governed records.
- Update and migration behavior should preserve user data and make repair paths clear.

## Implementation Boundaries

- This vision does not admit installer creation, shortcut mutation, model/capability-pack downloads, update execution, or release artifact work.
- This vision does not admit patcher creation, auto-update execution, restart automation, rollback execution, or always-on Owner AI continuity behavior.
- Active packaging work requires Branch Readiness approval and packaging/install-specific validation proof.
- Cross-FAM install/update/patch impacts are durable dependency candidates or platform-contract context unless Branch Readiness admits dependency-bounded work, a coordinated cross-FAM patch, or a repo-wide migration / halt through `Docs/phase_governance.md`.

## Canonical Pointers

- Project vision: `Docs/nexus_vision.md`
- AI runtime and trust architecture: `Docs/ai_runtime_and_trust_architecture.md`
- Edition capability / trust boundary release plan: `Docs/family_visions/FAM-007_ai_edition_capability_trust_boundary_release_plan.md`
- Backlog registry: `Docs/feature_backlog.md`
- Roadmap posture: `Docs/prebeta_roadmap.md`
