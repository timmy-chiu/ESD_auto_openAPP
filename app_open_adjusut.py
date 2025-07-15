import subprocess
import pyautogui
import pygetwindow as gw
import time
import os
import json

# 載入 config
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)


def open_device_manager(x, y, width, height):
    try:
        subprocess.Popen('devmgmt.msc', shell=True)
        adjust_window(['裝置管理員', 'Device Manager'], x, y, width, height)
    except Exception as e:
        print("open_device_manager 錯誤:", e)


def open_device_watcher(x, y, width, height):
    try:
        subprocess.Popen([config["device_watcher_path"]])
        adjust_window(['device watcher'], x, y, width, height)
    except Exception as e:
        print("open_device_watcher 錯誤:", e)


def open_battery_setting(x, y, width, height):
    try:
        os.system("start ms-settings:batterysaver")
        adjust_window(['設定', 'settings'], x, y, width, height)
    except Exception as e:
        print("open_battery_setting 錯誤:", e)


def open_keyboard_test(x, y, width, height):
    try:
        subprocess.Popen([config["keyboard_test_path"]])
        adjust_window(['keyboard'], x, y, width, height)
    except Exception as e:
        print("open_keyboard_test 錯誤:", e)


def open_media_player(x, y, width, height):
    try:
        os.makedirs(config["video_dir"], exist_ok=True)
        m3u8_path = os.path.join(config["video_dir"], "playlist.m3u8")
        with open(m3u8_path, "w") as f:
            f.write("#EXTM3U\n")
            for _ in range(15):
                f.write("#EXTINF:-1,\n")
                f.write("timer.mp4\n")
        os.startfile(m3u8_path)
        adjust_window(['媒體播放器', 'Media Player'], x, y, width, height)
    except Exception as e:
        print("open_media_player 錯誤:", e)


def open_camera(x, y, width, height):
    try:
        subprocess.Popen(['start', 'microsoft.windows.camera:'], shell=True)
        adjust_window(['相機', 'Camera'], x, y, width, height)
    except Exception as e:
        print("open_camera 錯誤:", e)


def open_paint_maximize():
    try:
        subprocess.Popen([config["touch_test_path"]])
        while True:
            window = gw.getWindowsWithTitle('touch')
            if window:
                window[0].maximize()
                # time.sleep(1)
                # window[0].minimize()
                break
            time.sleep(1)
    except Exception as e:
        print("open_paint_maximize 錯誤:", e)


def open_burnInTest(x, y, width, height):
    try:
        subprocess.Popen(config["burnintest_path"])
        time.sleep(10)

        # 先將焦點切到桌面（按 Win + D）
        pyautogui.hotkey('winleft', 'd')
        time.sleep(1)
        pyautogui.hotkey('winleft', 'd')

        # 再切回 BurnInTest 視窗並啟動測試
        window = gw.getWindowsWithTitle('BurnInTest 10.2')
        if window:
            window[0].activate()
            time.sleep(1)
            pyautogui.press('f4')
            print("已按下 F4 啟動測試。")
        else:
            print("無法找到 BurnInTest 視窗")

        adjust_window(['BurnInTest 10.2'], x, y, width, height)
        time.sleep(10)

        # 檢查是否有 3D 視窗
        three_d_window = gw.getWindowsWithTitle('BurnInTest 3D')
        if three_d_window:
            print("3D 視窗已開啟，切回 BurnInTest 視窗。")
            if window:
                window[0].activate()
        else:
            print("找不到 3D 視窗。")
    except Exception as e:
        print("open_burnInTest 錯誤:", e)



def adjust_window(titles, x, y, width, height):
    attempt = 0
    window_found = False
    while attempt < 20:
        for title in titles:
            windows = gw.getWindowsWithTitle(title)
            if windows:
                window = windows[0]
                window.moveTo(x, y)
                window.resizeTo(width, height)
                window_found = True
                print(f"已調整視窗 '{title}' 的大小與位置。")
                break
        if window_found:
            break
        attempt += 1
        time.sleep(1)
    if not window_found:
        print("找不到符合的視窗，已跳過。")


def open_and_layout_windows():
    screen_width, screen_height = pyautogui.size()
    screen_height -= 50

    w_half = int(screen_width * 0.5)
    open_burnInTest(0, 0, w_half, screen_height)

    width_dm = int(screen_width * 0.2)
    open_device_manager(screen_width - width_dm, 0, width_dm, screen_height)

    height_dw = int(screen_height * 0.25)
    open_device_watcher(screen_width - width_dm, screen_height-height_dw, width_dm, height_dw)

    open_camera(0, 0, w_half, int(screen_height * 0.7))

    remaining_w = screen_width - width_dm - w_half
    open_media_player(w_half, 0, remaining_w, int(screen_height * 0.4))
    open_battery_setting(w_half, int(screen_height * 0.7), remaining_w, int(screen_height * 0.3))
    open_keyboard_test(w_half, int(screen_height * 0.4), remaining_w, int(screen_height * 0.3))


if __name__ == "__main__":
    open_paint_maximize()
    open_and_layout_windows()
