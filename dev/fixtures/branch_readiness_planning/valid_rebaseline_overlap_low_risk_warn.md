# Valid Rebaseline Overlap Low-Risk WARN Fixture

## Branch Change Intent Ledger

### Changed Surface: Docs/incident_patterns.md

Surface Class: documentation/reference
Change Intent: clarify reference-only incident wording without changing source-truth ownership, phase rules, prompt templates, validators, or runtime behavior.
Why This File Was Touched: the branch reviewed a reference doc overlap and preserved it as a low-risk user-visible recommendation surface.
Owned Behavior / Fact Class: reference-only incident pattern guidance.
Canonical Owner / Source Owner: Docs/incident_patterns.md.
Resolution Owner: USER Decision
Shared Surface: Yes - reference documentation can be touched by multiple governance or runtime lanes.
Overlap Risk: Low because the file is not a source-truth owner, prompt/template owner, validator/helper owner, branch record, branch plan, roadmap/backlog owner, or governance policy owner.
Expected Conflict Risk: Low text conflict risk.
Semantic Merge Risk: Low
Regression / Gating Impact: None
Conflict Resolution Rule: classify as WARN, present the recommendation to USER, and do not mutate until the USER approves the exact rebaseline operation.
Rebaseline Handling: report WARN in the overlap packet and continue only after USER approval.
Validation Proof: validation required after repair: branch governance validation and governance efficiency validation.
Fallback Evidence: fallback evidence from source-truth owner lookup and commit messages may support WARN classification; it is not a compatibility bypass and cannot produce PASS without branch-owned intent evidence.
USER Decision / Waiver: USER approval required before rebaseline mutation.
Fold-Down Target: compact branch receipt only if the warning affects durable branch history.
