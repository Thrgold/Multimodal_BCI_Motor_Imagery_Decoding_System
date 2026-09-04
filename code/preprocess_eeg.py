import pandas as pd
import numpy as np
import mne
from mne.preprocessing import ICA
from scipy.stats import kurtosis

# ------------------------------------------------------------
# 1. 读事件并分类
# ------------------------------------------------------------
def _read_and_classify_events(bdf_path, event_label_map, trial_len_sec=4.0):
    """Use a protocol-verified mapping; never infer hand labels from event order."""
    if not event_label_map:
        raise ValueError('An explicit protocol-verified event_label_map is required.')
    raw_bdf = mne.io.read_raw_bdf(bdf_path, preload=False)
    original = raw_bdf.annotations
    unknown = set(original.description) - set(event_label_map)
    if unknown:
        raise ValueError(f'Unmapped annotation descriptions: {sorted(unknown)}')
    return mne.Annotations(onset=original.onset, duration=original.duration,
        description=[event_label_map[x] for x in original.description],
        orig_time=original.orig_time)


# ------------------------------------------------------------
# 2. 主预处理函数
# ------------------------------------------------------------
def preprocess_eeg_bdf(eeg_csv, bdf_path,
                       sfreq=1000.0, target_sfreq=250.0,
                       ref_channels=('A1','A2'), *, event_label_map=None, eeg_channels=None, voltage_unit=None):
    if not event_label_map or not eeg_channels or voltage_unit not in ('V', 'uV'):
        raise ValueError('Provide verified event_label_map, explicit eeg_channels and voltage_unit V/uV.')
    df = pd.read_csv(eeg_csv)
    ch_names = list(eeg_channels)
    data = df[ch_names].to_numpy(dtype=np.float64).T
    if voltage_unit == 'uV':
        data *= 1e-6
    if not np.isfinite(data).all():
        raise ValueError('Non-finite EEG values.')

    info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types='eeg')
    raw = mne.io.RawArray(data, info)

    # 添加电极位置（标准 10-20）
    montage = mne.channels.make_standard_montage('standard_1020')
    raw.set_montage(montage)

    # 读取事件并写入 raw
    annot = _read_and_classify_events(bdf_path, event_label_map)
    raw.set_annotations(annot)

    # ---------------- 其余步骤与原脚本一致 ----------------
    # 检查坏导
    bads = [ch for ch in ch_names if np.std(raw.get_data(picks=ch)) < 1e-10]
    if bads:
        raw.info['bads'] = bads
        raw.interpolate_bads(reset_bads=True)

    # 降采样
    if target_sfreq < sfreq:
        raw.filter(None, target_sfreq/2, fir_design='firwin')
        raw.resample(target_sfreq)

    # 滤波
    raw.notch_filter(50, fir_design='firwin')
    raw.filter(8, 40, fir_design='firwin')

    try:
        raw.set_eeg_reference(list(ref_channels), projection=False)
    except ValueError:  # 捕获“通道不存在”异常
        raw.set_eeg_reference('average', projection=True)

    # ICA uses the bounding interval spanning task events, including intervening rest.
    # 构造只含任务段的 raw
    event_id = {d: i for i, d in enumerate(np.unique(annot.description))}
    events, _ = mne.events_from_annotations(raw, event_id=event_id)
    picks_task = np.where(np.isin(events[:, 2],
                                  [event_id[k] for k in event_id
                                   if 'attempt' in k or 'imagery' in k]))[0]
    if not len(picks_task):
        raise ValueError('No attempt/imagery labels in verified mapping.')
    raw_task = raw.copy().crop(tmin=max(0., events[picks_task, 0].min() / raw.info['sfreq'] - 1),
                               tmax=min(raw.times[-1], events[picks_task, 0].max() / raw.info['sfreq'] + 5))
    # 训练 ICA
    ica = ICA(n_components=20, random_state=42, max_iter=500)
    ica.fit(raw_task, reject_by_annotation=True)

    # 自动标记伪迹成分（与原脚本一致）
    src = ica.get_sources(raw_task).get_data()
    comp_vars = np.var(ica.get_components(), axis=0)
    comp_kurt = kurtosis(src, axis=1)
    psds, freqs = mne.time_frequency.psd_array_welch(
        src, sfreq=target_sfreq, fmin=0, fmax=50)
    low_p = psds[:, freqs < 1].sum(1)
    high_p = psds[:, freqs > 30].sum(1)

    var_th = np.percentile(comp_vars, 85)
    kurt_th = np.percentile(comp_kurt, 85)
    low_th = np.percentile(low_p, 85)
    high_th = np.percentile(high_p, 85)

    ica.exclude = [
        i for i, (v, k, l, h) in enumerate(zip(comp_vars, comp_kurt, low_p, high_p))
        if v > var_th or k > kurt_th or l > low_th or h > high_th
    ]
    print(f'Excluding ICA components based on task segments: {ica.exclude}')

    # 可以取消注释进行交互检查
    ica.plot_components()
    ica.plot_sources(raw)

    raw_clean = ica.apply(raw.copy())

    # 质量评估
    sig = raw_clean.get_data()
    noise = raw.get_data() - sig
    snr_overall = 10 * np.log10(sig.var() / noise.var())
    psds_sig, _ = mne.time_frequency.psd_array_welch(
        sig, sfreq=target_sfreq, fmin=8, fmax=30)
    psds_noise, _ = mne.time_frequency.psd_array_welch(
        noise, sfreq=target_sfreq, fmin=8, fmax=30)
    snr_mi = 10 * np.log10(psds_sig.var() / psds_noise.var())
    print(f'Heuristic retained/residual variance ratio (not ground-truth SNR): {snr_overall:.2f} dB')
    print(f'Heuristic residual-power ratio (8-30 Hz): {snr_mi:.2f} dB')

    # Return data; saving is an explicit caller decision.
    return raw_clean

if __name__ == '__main__':
    raise SystemExit('Library prototype only: provide protocol-verified mapping, channel list and units to preprocess_eeg_bdf(). See README.md.')
