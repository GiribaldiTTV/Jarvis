# Invalid Rebaseline Overlap Fixture High-Impact Fixture

## Branch Change Intent Ledger

### Changed Surface: dev/fixtures/branch_readiness_planning/valid_user_feedback_disposition.md

Surface Class: fixture/test
Change Intent: change an executing regression fixture that affects validator truth.
Why This File Was Touched: the fixture changes what branch readiness planning validation treats as acceptable evidence.
Owned Behavior / Fact Class: regression coverage for USER Feedback Disposition marker validation.
Canonical Owner / Source Owner: dev/orin_branch_readiness_planning_fixture_validation.py.
Resolution Owner: Current Branch
Shared Surface: Yes - fixtures can overlap with validator/helper and governance changes.
Overlap Risk: High because the fixture changes validation acceptance behavior.
Expected Conflict Risk: Medium.
Semantic Merge Risk: Medium
Regression / Gating Impact: High
Conflict Resolution Rule: stop until USER approves the validator truth change and required validation reruns.
Rebaseline Handling: block rebaseline mutation until fixture intent and validator impact are proven.
Validation Proof: validation required after repair: branch readiness planning fixture validation and branch governance validation.
Fallback Evidence: fallback evidence may classify risk, but it is not a compatibility bypass.
USER Decision / Waiver: USER decision pending before mutation.
Fold-Down Target: compact branch receipt plus helper registry note if durable.
