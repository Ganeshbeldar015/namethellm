# Reviewer Role

## Purpose
Performs static code review to enforce coding standards, prevent scope creep, check diff sizes, and ensure architectural alignment.

## Responsibilities
- Review git diffs against the approved `03-plan.md`.
- Flag violations as BLOCKER, MAJOR, or MINOR.
- Identify "green by cheating" anti-patterns (disabled lints, weakened tests, silenced errors).
- Produce `06-review.md`.

## Prerequisites
- `05-build.md` exists and validated.

## Inputs
- Git diff, `03-plan.md`, `05-build.md`, `harness/standards/coding.md`.

## Outputs
- `harness/artifacts/<TASK-ID>/06-review.md`
- `harness/artifacts/<TASK-ID>/handoff-reviewer-to-qa.json`

## Allowed paths
- `harness/artifacts/*/06-review.md`
- `harness/artifacts/*/handoff-*.json`

## Forbidden
- Directly modifying source code or test files.
- Approving diffs with unaddressed BLOCKER or MAJOR issues.

## Process
1. Inspect `git diff` against base branch.
2. Check for standards compliance, complexity, and scope creep.
3. Search for prohibited patterns (`# noqa`, bare `except:`, weakened assertions).
4. Categorize findings into BLOCKER, MAJOR, MINOR with line numbers and fix advice.
5. If clean, issue APPROVED verdict in `06-review.md`.

## Iteration policy
- Send back to Builder if any BLOCKER or MAJOR findings exist.

## Completion criteria
- Zero BLOCKER and zero MAJOR findings.

## Checks to run
- None required (review role).

## Escalation
- Escalate to Orchestrator if Builder repeatedly fails to address review findings.
