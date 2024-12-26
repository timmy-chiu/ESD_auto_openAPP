import os

# 確保 video 資料夾存在
os.makedirs("video", exist_ok=True)

# 將 m3u8 檔案內容儲存到 video/playlist.m3u8
m3u8_path = os.path.join("video", "playlist.m3u8")
with open(m3u8_path, "w") as f:
    f.write("#EXTM3U\n")
    for _ in range(5):  # 重複5次
        f.write("#EXTINF:-1,\n")
        f.write("timer.mp4\n")  # 相對於 m3u8 檔案的路徑

# 開啟 m3u8 檔案並自動播放
os.startfile(m3u8_path)  # 在 Windows 上會用預設播放器開啟並播放
