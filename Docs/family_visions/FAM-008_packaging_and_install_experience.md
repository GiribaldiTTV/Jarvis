# FAM-008 Packaging And Install Experience Vision

## Purpose

This family vision records durable product direction for installer, shortcuts, packaged app experience, model/capability-pack install boundaries, update flow, and user-facing setup lifecycle.

## Vision Summary

Packaging and install work should make Nexus easier to install, launch, update, repair, and understand without silently changing system startup, provider, model, or capability-pack state.

## Accepted Direction

- Installer and shortcut behavior must be explicit, reversible, and validation-backed.
- Capability-pack installation should stay separate from the base app unless USER accepts a package boundary.
- Public, Dev, and Owner edition install identities, data roots, update channels, and GitHub Desktop/source-root setup should follow the edition trust-boundary plan before packaging work creates real artifacts.
- Setup should explain trust, privacy, provider, and disk/network implications before enabling heavier capabilities.
- Cache-root and clear-cache UX belongs here only as setup/install/user-education direction for approved cache owners; it must not imply provider/model execution, memory, or hidden capability-pack downloads.
- First-run AI orientation should explain local-only, no-provider, provider-assisted, disabled, and privacy-blocked states before asking for sensitive capability consent.
- Capability-pack setup should make storage, network, hardware, license, integrity, update, removal, and cache/index implications visible before installation.
- Clear-cache UX should explain what operational cache is cleared, what is not cleared, and which cache categories may rebuild later; it must not claim to delete memory, Trust Journal entries, logs, backups, or separately governed records.
- Update and migration behavior should preserve user data and make repair paths clear.

## Implementation Boundaries

- This vision does not admit installer creation, shortcut mutation, model/capability-pack downloads, update execution, or release artifact work.
- Active packaging work requires Branch Readiness approval and packaging/install-specific validation proof.

## Canonical Pointers

- Project vision: `Docs/nexus_vision.md`
- AI runtime and trust architecture: `Docs/ai_runtime_and_trust_architecture.md`
- Edition capability / trust boundary release plan: `Docs/family_visions/FAM-007_ai_edition_capability_trust_boundary_release_plan.md`
- Backlog registry: `Docs/feature_backlog.md`
- Roadmap posture: `Docs/prebeta_roadmap.md`
