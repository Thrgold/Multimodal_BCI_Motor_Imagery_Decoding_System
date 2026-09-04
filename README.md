# Multimodal BCI Motor Imagery Toolkit

Research utilities for EEG/fNIRS preprocessing, stimulus presentation and an EEG CNN–bidirectional-LSTM model. **This checkout is a partial research prototype, not a complete real-time rehabilitation system.**

## Included components

| Path | Purpose |
|---|---|
| `code/data_reader.py` | Dataset readers and file-stream simulation |
| `code/preprocess_eeg.py` | Explicit-configuration EEG preprocessing prototype |
| `code/preprocess_fnirs.py` | Interactive fNIRS processing/export prototype |
| `code/bdf_to_csv.py`, `code/extract_eeg.py` | Explicit-path BDF export |
| `code/evt2csv.py` | Annotation export |
| `code/inspect_snirf.py` | First stimulus-group inspection |
| `code/run_paradigm.py` | Local stimulus video and click-time interface |
| `code/models/cnn_lstm.py` | Included EEG classifier architecture |
| `paper/`, `paradigm/`, `figures/` | Local materials, excluded pending privacy/rights review |
| `result/` | Local outputs; not validated benchmark scores |

## Setup and limited verification

Use a Python environment with Tk support for interactive tools. Dependency versions are not a tested portable lockfile.

```bash
python -m pip install -r requirements.txt
python code/check_project.py
python code/bdf_to_csv.py --help
python code/evt2csv.py --help
python code/inspect_snirf.py --help
```

The check runs on synthetic zeros and verifies model output shape and finite values. It does not establish accuracy, training convergence, hardware compatibility or biological validity. Supply your own legally obtained recordings to the utilities. BDF export uses MNE SI units (EEG volts); check units before passing CSVs into legacy preprocessing.

## Scientific limitations

No verified decoding accuracy is provided in this checkout. The existing output.csv is a local signal export, not performance evidence, and is excluded from publication. No EEG/fNIRS fusion model or synchronized multimodal training pipeline is present. No frontend/backend service, trained weights or real-device acquisition integration is included. File streaming is not hardware streaming. Legacy preprocessing thresholds and residual-power ratios require dataset-specific validation and do not demonstrate clinical efficacy. Use trusted local NPZ files only; the legacy reader allows pickle loading.

The old Windows real-time launcher has been disabled because its target services are absent; it no longer kills port owners. This repository is not a medical device or treatment recommendation.

## Publication and rights

See [release review](RELEASE_REVIEW.md). Original participant forms, schedules, images and office documents remain locally but are ignored and untracked from the current index. The main branch was rebuilt as a single audited initial commit. Earlier artifacts are no longer in its history, but old commit URLs, caches, forks and clones may retain copies. Ignoring files does not remove previous public copies. No license is assigned to unverified third-party materials. Confirm authorship and third-party permissions before adding an open-source license.

The paradigm prototype expects separately supplied right_hand.mp4 and left_hand.mp4 videos in the working directory. These files are not included; GUI timing has not been validated for stimulus synchronization.

## Final scientific review

See [FINAL_REVIEW.md](FINAL_REVIEW.md). EEG preprocessing now requires an explicit annotation-to-label mapping, EEG channel list and voltage unit. It no longer infers left/right hand labels from event order or drops the final CSV channel. Original annotation durations are preserved, so protocol-specific duration correction remains the caller's responsibility. Sampling frequency and montage must match the recording; defaults are not validated device settings.

ICA still uses heuristic rejection thresholds and a bounding task interval that includes intervening rest. Its retained/residual ratios are not ground-truth SNR. No subject-level train/test split, accuracy table or multimodal-fusion validation is provided. Do not use this preprocessing prototype as evidence of a validated decoding pipeline.
