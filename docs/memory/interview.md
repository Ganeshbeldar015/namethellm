# Interview & Architecture Decisions Log (/grill-me)

## Session: 2026-10-16 / 2026-10-17

### 1. Modeling Strategy & Execution Architecture
- **Decision**: Hybrid approach.
- **Rationale**: Local modular development for rapid CV experiments on stylometry, n-grams, and tree/linear models; package heavy pretrained LLM embeddings and LoRA heads in the Kaggle submission notebook.

### 2. Feature Engineering & Stylometry
- **Decision**: Combined Structural Stylometry + Subword/Word N-Grams.
- **Rationale**: Character n-grams (3-5) capture morphological and stylistic phrasing; word n-grams (1-3) capture functional vocabulary; structural statistics (punctuation frequencies, casing, sentence/word length distributions) provide topic-invariant signals.

### 3. Metric Post-Processing (Balanced Accuracy)
- **Decision**: Adaptive Centering & Probability Calibration.
- **Rationale**: The test set has unequal class distributions differing from train. Calibrated probabilities combined with test-time adaptive centering (centering predicted logits/probabilities per passage or prompt cluster) prevent majority bias and directly maximize per-class recall.

### 4. Classifier Blending Strategy
- **Decision**: Multi-Model Log-Probability Blend.
- **Rationale**: Linear models (calibrated LinearSVC / LogisticRegression) excel on sparse high-dimensional n-grams; LightGBM excels on dense non-linear stylometric features; blending their log-probabilities creates a robust, low-variance ensemble.

### 5. Packaging & Kaggle Code Submission
- **Decision**: Standalone Self-Contained Notebook Exporter.
- **Rationale**: Maintain cleanly tested Python modules locally in `src/namethellm/`, and provide an exporter script (`scripts/export_kaggle_notebook.py`) that bundles the verified pipeline into a single, offline-runnable notebook submitted via Kaggle CLI / Kaggle MCP.
