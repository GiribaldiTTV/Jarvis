# Invalid Rebaseline Overlap Intent Fixture

## Branch Change Intent Ledger

### Changed Surface: dev/orin_branch_governance_validation.py

Surface Class: validator/helper
Change Intent: update validator behavior for a future rebaseline.
Why This File Was Touched: this is a high-risk validator overlap.
Owned Behavior / Fact Class: validator behavior.
Canonical Owner / Source Owner: dev/orin_branch_governance_validation.py.
Resolution Owner: Current Branch
Shared Surface: Yes.
Overlap Risk: High.
Expected Conflict Risk: Medium.
Semantic Merge Risk: Unknown
Regression / Gating Impact: Low
Conflict Resolution Rule: accept if the merge is text-clean.
Rebaseline Handling: continue after fallback evidence.
Validation Proof: validation required after repair.
Fallback Evidence: commit message fallback evidence only, not a bypass.
USER Decision / Waiver: USER decision pending.
Fold-Down Target: branch receipt.
