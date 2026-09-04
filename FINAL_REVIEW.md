# Final release review

## Findings and changes

1. Academic scope: EEG and fNIRS utilities coexist, but synchronized fusion, trained decoding evaluation and hardware/backend integration are absent. README now limits its claims accordingly.
2. Label validity: removed sequential left/right label invention and silent event truncation. Explicit protocol-verified mapping is mandatory and unmapped annotations cause an error.
3. Signal validity: replaced silent final-column dropping with explicit channel selection and explicit volts/microvolts conversion. Defaults for sampling rate/montage still require user verification.
4. Interpretation: ICA fits a bounding interval, not exclusively concatenated task segments. Residual variance is not known noise; ratios are not certified SNR or clinical outcomes.
5. Safety: saving cleaned data is caller-controlled; old launcher cannot kill unrelated processes. Binary documents, schedules and images are excluded from the current tree, and the main branch history has been rebuilt; old cached or third-party copies are not guaranteed erased.
6. Reproducibility: synthetic model forward checks and preprocessing input-guard tests are provided. No raw-data rerun, GUI synchronization test, training or accuracy reproduction is certified.
7. Authenticity: no supported empirical accuracy result is available in this checkout. Local output.csv is not published as a benchmark. This review cannot certify the truth of excluded office documents or historical images.
8. PI judgement: suitable as a clearly scoped prototype/code portfolio, not evidence of a complete validated multimodal system. No authorship, dataset license or clinical approval is inferred from files. No blanket open-source license is assigned pending rights confirmation.

With explicit owner authorization, the remote main branch was replaced by a single initial commit containing this audited snapshot. This does not guarantee deletion of GitHub cached commits or third-party copies.
