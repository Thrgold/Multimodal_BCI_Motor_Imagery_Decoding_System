import tkinter as tk
import cv2
import numpy as np
from PIL import Image, ImageTk
import time
import os

class VideoPlayer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')
        self.video_window = None
        self.video_label = None
        self.video_capture = None
        self.start_button = tk.Button(self.root, text="Start", command=self.start_playback)
        self.start_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.is_paused = False  # 新增暂停状态标志
        self.play_count = 0
        self.max_plays = 50
        self.video_index = 0
        self.video_files = ["right_hand.mp4", "left_hand.mp4"]
        self.timer_start_time = 0
        self.click_times_folder = self.create_unique_folder()  # 创建唯一文件夹
        self.click_times_file = os.path.join(self.click_times_folder, "click_times.txt")  # 存储时间的文件名
        self.ensure_file_exists()  # 确保文件存在
        self.bind_key_press()  # 绑定键盘事件

    def bind_key_press(self):
        # 绑定ESC键退出程序
        self.root.bind('<Escape>', self.exit_player)
        # 绑定空格键暂停/继续播放
        self.root.bind('<space>', self.pause_playback)

    def exit_player(self, event=None):
        if self.video_window:
            self.video_window.destroy()
            self.video_window = None
        else:
            self.root.destroy()  # 退出程序

    def start_playback(self):
        self.start_button.place_forget()
        self.open_video_window()
        self.timer_start_time = time.time()  # 记录开始时间

    def open_video_window(self):
        self.video_window = tk.Toplevel(self.root)
        self.video_window.attributes('-fullscreen', True)
        self.video_window.configure(bg='black')
        self.video_capture = cv2.VideoCapture(self.video_files[self.video_index])
        self.video_label = tk.Label(self.video_window)
        self.video_label.pack()
        # 绑定鼠标左键事件
        self.video_label.bind('<Button-1>', self.record_mouse_click)
        # 添加显示播放次数的标签
        self.play_count_label = tk.Label(self.video_window, text="Plays: 0", bg='black', fg='white')
        self.play_count_label.place(relx=0.95, rely=0.05, anchor=tk.CENTER)
        # 绑定ESC键关闭视频窗口
        self.video_window.bind('<Escape>', self.exit_player)
        self.play_video()

    def play_video(self):
        if self.is_paused:
            return
        ret, frame = self.video_capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image=img)
            self.video_label.config(image=photo)
            self.video_label.image = photo
            self.video_window.after(30, self.play_video)
        else:
            self.video_capture.release()
            self.play_count += 1
            self.update_play_count_label()  # 更新播放次数显示
            if self.play_count < self.max_plays:
                # 这里重新获取当前视频帧，继续播放当前视频
                self.video_capture = cv2.VideoCapture(self.video_files[self.video_index])
                self.play_video()
            else:
                self.play_count = 0
                self.video_index = (self.video_index + 1) % len(self.video_files)
                if self.video_index == 0:
                    self.root.destroy()
                else:
                    # 关闭当前视频窗口，打开下一个视频窗口
                    self.video_window.destroy()
                    self.open_video_window()

    def update_play_count_label(self):
        self.play_count_label.config(text=f"Plays: {self.play_count}")

    def record_mouse_click(self, event):
        # 记录鼠标点击时的时间
        current_time = time.time()
        elapsed_time = current_time - self.timer_start_time
        self.save_time_to_file(elapsed_time)

    def save_time_to_file(self, elapsed_time):
        # 将记录的时间保存到文本文件
        with open(self.click_times_file, "a") as file:
            file.write(f"{elapsed_time:.3f}\n")

    def ensure_file_exists(self):
        # 确保存储时间的文件存在
        if not os.path.exists(self.click_times_file):
            open(self.click_times_file, 'w').close()

    def create_unique_folder(self):
        # 创建一个基于当前日期和时间的唯一文件夹
        current_time = time.strftime("%Y%m%d_%H%M%S")
        folder_name = f"click_times_{current_time}"
        os.makedirs(folder_name, exist_ok=True)
        return folder_name

    def pause_playback(self, event=None):
        self.is_paused = not self.is_paused
        if self.is_paused:
            print("视频已暂停")
        else:
            print("视频继续播放")
            self.play_video()

if __name__ == "__main__":
    player = VideoPlayer()
    player.root.mainloop()