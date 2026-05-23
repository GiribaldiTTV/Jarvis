# Valid Rebaseline Overlap Intent Fixture

## Branch Change Intent Ledger

### Changed Surface: dev/orin_branch_governance_validation.py

Surface Class: validator/helper
Change Intent: preserve the compact source-truth validation model while adding marker-first overlap-intent regression checks for future rebaseline operations.
Why This File Was Touched: the validator owns machine-checkable governance marker enforcement and must prevent future branches from treating overlapping validator changes as safe without intent evidence.
Owned Behavior / Fact Class: marker-first validation for branch planning, source-truth reform, UFD, Vision Contract, and Rebaseline Overlap Intent Gate evidence.
Canonical Owner / Source Owner: Docs/validation_helper_registry.md and dev/orin_branch_governance_validation.py.
Resolution Owner: Current Branch
Shared Surface: Yes - future governance and runtime branches can both touch validator/helper surfaces.
Overlap Risk: Medium because incoming validator changes can merge cleanly while weakening a branch-local safety rule.
Expected Conflict Risk: Medium text conflict risk when sibling branches edit the same marker lists or validation gates.
Semantic Merge Risk: Medium
Conflict Resolution Rule: compare incoming validator intent against this branch ledger before accepting either side, preserve stricter safety when the two rules are compatible, and stop for USER decision when behavior changes.
Rebaseline Handling: re-run the overlap gate, branch governance validation, governance efficiency validation, fixture validation, and compile proof before requesting rebaseline mutation.
Validation Proof: validation required after any overlap-intent repair: branch governance validation, governance efficiency validation, fixture validation, and compileall.
Fallback Evidence: fallback evidence may classify risk through commit messages, branch record, helper registry, and fixtures, but it is not a compatibility bypass.
USER Decision / Waiver: USER approval required before rebaseline mutation when this validator overlaps incoming main changes.
Fold-Down Target: compact branch receipt plus helper registry note when durable overlap evidence remains useful.

### Changed Surface: Docs/codex_user_guide.md

Surface Class: documentation/reference
Change Intent: keep human-facing guidance aligned with canonical phase and naming standards without making the guide a live-state owner.
Why This File Was Touched: the user guide may need compact pointer language when governance terms change.
Owned Behavior / Fact Class: user-facing explanatory reference for Codex workflow terms.
Canonical Owner / Source Owner: Docs/codex_user_guide.md.
Resolution Owner: Current Branch
Shared Surface: Yes - multiple planning branches can clarify guide wording.
Overlap Risk: Low because the guide is reference-only when it does not redefine source-truth policy.
Expected Conflict Risk: Low text conflict risk.
Semantic Merge Risk: Low
Conflict Resolution Rule: preserve canonical term pointers and reject any wording that contradicts Docs/phase_governance.md.
Rebaseline Handling: review the overlap packet and continue only after USER approval for the exact rebaseline operation.
Validation Proof: validation required after wording repair: branch governance validation and governance efficiency validation.
Fallback Evidence: fallback evidence may include Docs/Main.md and Docs/phase_governance.md ownership lookup; it is not a compatibility bypass.
USER Decision / Waiver: USER decision pending until the overlap packet is reviewed.
Fold-Down Target: no durable fold-down beyond compact branch receipt unless the wording becomes a reusable guide standard.
