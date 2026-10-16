# Decisions Log

| Timestamp | Decision ID | Topic | Decision | Approved By | Notes |
|---|---|---|---|---|---|
| 2026-10-16T22:59:30+05:30 | DEC-001 | Project Profile | Configured profile as ML competition pipeline with solo team mode and disabled Designer role | Orchestrator | Derived from docs/raw.md |
| 2026-10-16T23:05:56+05:30 | DEC-002 | Harness Plan Approval | Approved docs/harness.md detailed plan; transition to Mode C Sprint 0 | User | Approved via user prompt |
| 2026-10-16T23:29:09+05:30 | DEC-003 | Package Install & Sprint 0 Commit | Approved pip install pytest pyarrow and Sprint 0 scaffold commit | User | Approved via user prompt |
| 2026-10-17T00:05:15+05:30 | DEC-004 | Modeling Architecture | Adopted Hybrid approach: modular local stylometry/trees + heavy LLM in submission notebook | User | /grill-me interview |
| 2026-10-17T00:08:34+05:30 | DEC-005 | Feature Engineering | Combined structural stylometry with character (3-5) and word (1-3) TF-IDF n-grams | User | /grill-me interview |
| 2026-10-17T00:15:01+05:30 | DEC-006 | Metric Post-Processing | Implement adaptive centering and probability calibration for Balanced Accuracy | User | /grill-me interview |
| 2026-10-17T00:20:01+05:30 | DEC-007 | Classifier Strategy | Multi-model log-prob blend: calibrated linear models + LightGBM on dense stylometrics | User | /grill-me interview |
| 2026-10-17T00:20:19+05:30 | DEC-008 | Submission Packaging | Standalone self-contained notebook exporter deployable via Kaggle CLI / MCP | User | /grill-me interview |


