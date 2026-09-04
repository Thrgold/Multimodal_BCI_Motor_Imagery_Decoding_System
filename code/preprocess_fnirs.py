import os
import numpy as np
import mne
from mne.preprocessing.nirs import optical_density, beer_lambert_law
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


class FNIRSProcessor:
    def __init__(self, fnirs_file_path=None):
        """
        如果调用时不传路径，则在 read_fnirs_data() 里弹窗选择
        """
        self.fnirs_file_path = fnirs_file_path
        self.fnirs_raw = None
        self.fnirs_raw_conc = None
        self.hbo_data = None
        self.hbr_data = None
        self.hbo_channels = None
        self.hbr_channels = None

    # ---------- 1. 选择文件 ----------
    def select_file(self, title="选择 fNIRS 文件", ext=None):
        root = tk.Tk()
        root.withdraw()
        if ext is None:
            filetypes = [("SNIRF/NIRx", "*.snirf *.hdr")]
        else:
            filetypes = [(ext, f"*.{ext}")]
        path = filedialog.askopenfilename(title=title, filetypes=filetypes)
        return path

    def select_directory(self, title="选择 NIRx 数据文件夹"):
        root = tk.Tk()
        root.withdraw()
        return filedialog.askdirectory(title=title)

    # ---------- 2. 读取数据 ----------
    def read_fnirs_data(self):
        """
        如果实例化时未传入路径，会弹窗让用户选择
        """
        if not self.fnirs_file_path:
            # 让用户决定是选文件还是选目录
            choice = input("输入 1 选择 SNIRF 文件，输入 2 选择 NIRx 目录：")
            if choice.strip() == "1":
                self.fnirs_file_path = self.select_file("选择 SNIRF 文件", "snirf")
                if not self.fnirs_file_path:
                    print("未选择文件，终止。")
                    return None
                reader = mne.io.read_raw_snirf
            else:
                self.fnirs_file_path = self.select_directory("选择 NIRx 目录")
                if not self.fnirs_file_path:
                    print("未选择目录，终止。")
                    return None
                reader = mne.io.read_raw_nirx
        else:
            # 根据后缀自动选择读取器
            ext = os.path.splitext(self.fnirs_file_path)[-1].lower()
            reader = mne.io.read_raw_nirx if ext in ['.hdr', ''] else mne.io.read_raw_snirf

        print("读取 fNIRS 数据 ...")
        try:
            self.fnirs_raw = reader(self.fnirs_file_path, preload=True)
            self.fnirs_raw_od = optical_density(self.fnirs_raw)
            self.fnirs_raw_conc = beer_lambert_law(self.fnirs_raw_od)
            self.fnirs_raw_conc.filter(l_freq=0.01, h_freq=0.2)

            # 提取通道
            self.hbo_channels = mne.pick_types(self.fnirs_raw_conc.info, fnirs='hbo')
            self.hbr_channels = mne.pick_types(self.fnirs_raw_conc.info, fnirs='hbr')

            self.hbo_data = self.fnirs_raw_conc.get_data(picks=self.hbo_channels)
            self.hbr_data = self.fnirs_raw_conc.get_data(picks=self.hbr_channels)

            print(f"成功提取 {len(self.hbo_channels)} 个 HbO 通道和 "
                  f"{len(self.hbr_channels)} 个 HbR 通道")
            return self
        except Exception as e:
            print(f"读取失败：{e}")
            return None

    # ---------- 3. 可视化 ----------
    def plot_fnirs(self, duration=30, n_channels=10):
        if self.fnirs_raw_conc is not None:
            self.fnirs_raw_conc.plot(duration=duration, n_channels=n_channels)
            plt.show()

    # ---------- 4. 保存 ----------
    def save_hbo_hbr_separately(self, hbo_save_path=None, hbr_save_path=None):
        if self.hbo_data is None or self.hbr_data is None:
            print("无数据可保存")
            return

        times = self.fnirs_raw_conc.times
        hbo_ch_names = [self.fnirs_raw_conc.ch_names[i] for i in self.hbo_channels]
        hbr_ch_names = [self.fnirs_raw_conc.ch_names[i] for i in self.hbr_channels]

        # 弹窗选择保存路径
        if hbo_save_path is None:
            hbo_save_path = filedialog.asksaveasfilename(
                title="保存 HbO CSV", defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")])
        if hbr_save_path is None:
            hbr_save_path = filedialog.asksaveasfilename(
                title="保存 HbR CSV", defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")])

        if not hbo_save_path or not hbr_save_path:
            print("取消保存")
            return

        # HbO
        hbo_df = pd.DataFrame(self.hbo_data.T, columns=hbo_ch_names)
        hbo_df.insert(0, 'Time', times)
        hbo_df.to_csv(hbo_save_path, index=False)
        print(f"HbO 已保存 → {hbo_save_path}")

        # HbR
        hbr_df = pd.DataFrame(self.hbr_data.T, columns=hbr_ch_names)
        hbr_df.insert(0, 'Time', times)
        hbr_df.to_csv(hbr_save_path, index=False)
        print(f"HbR 已保存 → {hbr_save_path}")


# ---------------- 运行入口 ----------------
if __name__ == '__main__':
    processor = FNIRSProcessor()     # 不传路径，由用户选择
    if processor.read_fnirs_data():
        processor.save_hbo_hbr_separately()
        processor.plot_fnirs()