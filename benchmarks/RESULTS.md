# F56 Held-Out Reproducibility Results

Gold Standard validation was executed from a clean GitHub Actions checkout.

- Evidence run: `32557108987`
- Head: `6f5832dfeccd39c315ee8cde4edc477c739ef0f4`
- Python: 3.10, 3.11, 3.12 all green
- Held-out radiology workflow scenarios: 8/8 passed
- Pass rate: 1.0
- Artifact: `f56-heldout-results`
- Artifact digest: `sha256:2af70f1abb34d5c0d85b9a08b2da85132f25a7a62a0012cfb634d40280d7ccf3`

The suite validates patient identity, acquisition completeness, critical-result acknowledgment, uncertainty requiring second read, privacy, conflict handling, and mandatory qualified human sign-off. L3 does not imply autonomous diagnosis, autonomous report finalization, or replacement of radiologist judgment.
