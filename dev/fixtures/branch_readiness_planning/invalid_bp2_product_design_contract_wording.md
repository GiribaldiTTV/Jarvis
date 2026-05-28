# Invalid BP2 Product Design Contract Wording Fixture

USER Branch Plan Review: Required
Accepted Branch Vision Summary: BP1 accepted - USER accepted the Branch Vision before this BP2 plan review.
Implementation Package Summary: This fixture otherwise describes an engineering implementation package.
Branch Scope Size Test: The package is intended to be coherent and reviewable as one feature-focused branch.
SLC / Seam Plan: Seam 1 validates helper wording and packet output.
Affected Surfaces: USER packet helper, fixture validator, and Branch Planning docs.
Likely Files: dev/orin_user_review_bundle.py and branch-readiness planning fixtures.
Validators / Helpers: Branch Readiness planning fixture validation and USER review bundle helper validation.
Proof Requirements: The validator must reject stale BP1 product/design wording inside BP2.
Element-to-Phase Proof Matrix: BP2 plan review maps to BP3 before Workstream implementation.
H1 Expectations: H1 verifies implementation against accepted plan only after BP3 is green.
LV / UTS Expectations: Live Validation remains separate and not part of BP2.
Rollback / Safety Plan: Revert helper wording and fixture changes if validation fails.
Future-Gated Boundaries: PR creation, merge, release, runtime, private, provider, cache, memory, and artifact-model changes remain pending.
Plan Acceptance Checklist: BP2 is green only when it is engineering-plan-first and traces to accepted or waived BP1.
Exact BP3 Approval Text: BP3 approval may be requested only after BP1 and BP2 are accepted or waived and orchestration validation is green.

This file is a required user-facing product/design planning gate. It should help USER answer: Do I actually like what Codex is about to build?
