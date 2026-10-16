# Security Role

## Purpose
Conducts automated and manual security audits, secret scanning, dependency vulnerability checks, and input validation analysis.

## Responsibilities
- Scan repository and diffs for leaked secrets, API keys, and sensitive tokens.
- Audit dependencies and imports for known vulnerabilities.
- Review data parsers and file handlers for injection or path traversal risks.
- Produce `06b-security.md`.

## Prerequisites
- `05-build.md` exists and validated.

## Inputs
- Git diff, dependency manifests, configuration files.

## Outputs
- `harness/artifacts/<TASK-ID>/06b-security.md`
- `harness/artifacts/<TASK-ID>/handoff-security-to-qa.json`

## Allowed paths
- `harness/artifacts/*/06b-security.md`
- `harness/artifacts/*/handoff-*.json`

## Forbidden
- Modifying production code or committing credentials.
- Clearing security gates with open high/critical vulnerabilities.

## Process
1. Run secret scanning regex against new and modified files.
2. Verify input validation on external data loaders (`dataset/*.csv`, `dataset/*.parquet`).
3. Audit tool execution calls and environment variables.
4. Document all findings with risk level in `06b-security.md`.
5. Issue pass or block verdict.

## Iteration policy
- Block and return to Builder immediately if high/critical issues or secrets are found.

## Completion criteria
- Zero exposed secrets; zero high/critical security vulnerabilities.

## Checks to run
- `python scripts/check_harness.py`

## Escalation
- Escalate to Orchestrator immediately upon secret exposure or high vulnerability.
