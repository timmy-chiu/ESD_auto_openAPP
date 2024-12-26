import subprocess
import pyautogui
import pygetwindow as gw
import time
import os


def open_device_manager(x, y, width, height):
    # 使用 subprocess 開啟裝置管理員
    subprocess.Popen('devmgmt.msc', shell=True)

    # 調整視窗大小與位置
    adjust_window(['裝置管理員', 'Device Manager'], x, y, width, height)

    # 使用 subprocess 開啟裝置監控
    subprocess.Popen(["dist/device_watcher.exe"])  # 確保路徑正確

    # 調整視窗大小與位置
    watcher_h = int(height / 4)
    watcher_y = y + height - watcher_h
    adjust_window(['device watcher'], x, watcher_y, width, watcher_h)


def open_notepad(x, y, width, height):
    # 使用 subprocess 啟動 keyboard_test.exe
    subprocess.Popen(["dist/keyboard_test_v2.exe"])  # 確保路徑正確

    # 調整視窗大小與位置
    adjust_window(['keyboard'], x, y, width, height)
    #
    # # 使用 subprocess 開啟記事本
    # subprocess.Popen('notepad.exe')
    #
    # # 調整視窗大小與位置
    # adjust_window(['記事本', 'Notepad'], x, y, width, height)


def open_media_player(x, y, width, height):
    # # 使用 subprocess 開啟媒體播放器（Windows Media Player）
    # subprocess.Popen('mediaplayer.exe')
    # time.sleep(2)

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

    # 調整視窗大小與位置
    adjust_window(['媒體播放器', 'Media Player'], x, y, width, height)


def open_camera(x, y, width, height):
    # 使用 subprocess 開啟媒體播放器（Windows Media Player）
    subprocess.Popen(['start', 'microsoft.windows.camera:'], shell=True)  # 開啟內建相機應用程式

    # 調整視窗大小與位置
    adjust_window(['相機', 'Camera'], x, y, width, height)


def open_paint_maximize():
    # 使用 subprocess 啟動 paint.exe
    subprocess.Popen(["dist/touch_test.exe"])  # 確保路徑正確

    # 等待程式開啟
    while True:
        window = gw.getWindowsWithTitle('touch')
        if window:
            window[0].maximize()  # 將小畫家視窗最大化
            time.sleep(1)
            # 最小化小畫家視窗
            window[0].minimize()
            break
        else:
            time.sleep(1)


def open_burnInTest(x, y, width, height):
    # 指定 BurnInTest 的執行檔路徑
    burnintest_path = r"C:\Program Files\BurnInTest\bit.exe"  # 請根據實際路徑調整

    # 使用 subprocess 開啟 BurnInTest
    subprocess.Popen(burnintest_path)

    # 等待 BurnInTest 完全啟動
    time.sleep(10)  # 根據實際情況調整等待時間

    # 關掉測試版試用的視窗
    pyautogui.press('enter')
    time.sleep(1)  # 等待操作完成

    window = gw.getWindowsWithTitle('BurnInTest')

    if window:
        window[0].activate()

        # F6 -> Start
        pyautogui.press('f6')
        time.sleep(3)  # 等待操作完成
        pyautogui.press('enter')
        time.sleep(1)  # 等待操作完成
        pyautogui.press('enter')
        time.sleep(3)  # 等待操作完成
    else:
        print("無法找到 BurnInTest 視窗，請確認程式是否正確開啟。")

    # 調整視窗大小與位置
    adjust_window(['BurnInTest'], x, y, width, height)

    time.sleep(5)  # 等待操作完成
    # 嘗試縮小 3D 視窗
    three_d_window = gw.getWindowsWithTitle('3D')  # 假設 3D 視窗標題包含 "3D"
    if three_d_window:
        three_d_window[0].minimize()  # 將 3D 視窗縮小
        print("3D 視窗已成功縮小。")
    else:
        print("找不到 3D 視窗。請確認視窗標題是否正確。")


def adjust_window(titles, x, y, width, height):
    """
    調整多個視窗的大小與位置。

    :param titles: 視窗的標題列表，用於識別視窗。
    :param x: 視窗的水平位置。
    :param y: 視窗的垂直位置。
    :param width: 視窗的寬度。
    :param height: 視窗的高度。
    """
    attempt = 0
    window_found = False

    while attempt < 20:  # 最多嘗試20次
        for title in titles:
            windows = gw.getWindowsWithTitle(title)
            if windows:
                window = windows[0]
                window.moveTo(x, y)
                window.resizeTo(width, height)
                window_found = True
                print(f"已調整視窗 '{title}' 的大小與位置。")
                break  # 找到符合的視窗後退出 for 迴圈
        if window_found:
            break  # 找到符合的視窗後退出 while 迴圈
        else:
            attempt += 1
            time.sleep(1)  # 等待1秒後重試

    if not window_found:
        print("找不到符合的視窗，已跳過。")


def open_and_layout_windows():
    # 取得螢幕尺寸
    screen_width, screen_height = pyautogui.size()
    screen_height -= 50  # 扣掉工作列高度

    # 裝置管理員寬度
    width_dm = int(screen_width * 0.2)  # 20% 寬度

    # 開啟裝置管理員
    open_device_manager(screen_width - width_dm, 0, width_dm, screen_height)

    # 調整剩餘寬度
    remaining_width = screen_width - width_dm
    w_half = int(remaining_width / 2)
    h_half = int(screen_height / 2)

    # 開啟burnInTest（剩餘畫面的左下）
    open_burnInTest(0, 0, w_half, h_half * 2)

    # 開啟相機（剩餘畫面的左上）
    open_camera(0, 0, w_half, h_half)

    # 開啟媒體播放器（剩餘畫面的右上）
    open_media_player(w_half, 0, w_half, h_half)

    # 開啟記事本（剩餘畫面的右下）
    open_notepad(w_half, h_half, w_half, h_half)


open_paint_maximize()
open_and_layout_windows()

