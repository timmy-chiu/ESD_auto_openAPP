import subprocess
import pyautogui
import pygetwindow as gw
import time
import os
import json
import sys
from pathlib import Path

# 載入 config
BASE_DIR = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent


def app_path(path):
    path = Path(path)
    return path if path.is_absolute() else BASE_DIR / path


with open(BASE_DIR / "config.json", "r", encoding="utf-8") as f:
    config = json.load(f)


def open_device_manager(x, y, width, height):
    try:
        subprocess.Popen('devmgmt.msc', shell=True)
        adjust_window(['裝置管理員', 'Device Manager'], x, y, width, height)
    except Exception as e:
        print("open_device_manager 錯誤:", e)


def open_device_watcher(x, y, width, height):
    try:
        subprocess.Popen([str(app_path(config["device_watcher_path"]))])
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
        subprocess.Popen([str(app_path(config["keyboard_test_path"]))])
        adjust_window(['keyboard'], x, y, width, height)
    except Exception as e:
        print("open_keyboard_test 錯誤:", e)


def open_media_player(x, y, width, height):
    try:
        video_dir = app_path(config["video_dir"])
        video_dir.mkdir(parents=True, exist_ok=True)

        timer_path = video_dir / "timer.mp4"
        if not timer_path.exists():
            raise FileNotFoundError(timer_path)

        m3u8_path = video_dir / "playlist.m3u8"
        repeat_times = int(config.get("video_repeat_times", 1))
        with open(m3u8_path, "w", encoding="utf-8", newline="\n") as f:
            f.write("#EXTM3U\n")
            for _ in range(repeat_times):
                f.write("#EXTINF:-1,\n")
                f.write(f"{timer_path.as_uri()}\n")

        os.startfile(str(m3u8_path))
        adjust_window(['媒體播放器', 'Media Player'], x, y, width, height)
    except Exception as e:
        print("open_media_player 錯誤:", e)


def has_camera():
    """
    透過 PowerShell 檢查系統是否存在影像擷取裝置
    """
    try:
        result = subprocess.run(
            ['powershell', '-Command', 'Get-PnpDevice -Class Camera | Where-Object { $_.Status -eq "OK" }'],
            capture_output=True, text=True
        )
        return bool(result.stdout.strip())
    except Exception:
        return False


def open_camera(x, y, width, height):
    if has_camera():
        try:
            subprocess.Popen(['start', 'microsoft.windows.camera:'], shell=True)
            adjust_window(['相機', 'Camera'], x, y, width, height)
        except Exception as e:
            print("open_camera 錯誤:", e)
    else:
        print("沒有內建相機，不開啟此功能")


def open_paint_maximize():
    try:
        subprocess.Popen([str(app_path(config["touch_test_path"]))])
        while True:
            window = gw.getWindowsWithTitle('touch')
            if window:
                break
            time.sleep(1)
    except Exception as e:
        print("open_paint_maximize 錯誤:", e)


def open_burn(x, y, width, height):
    try:
        # 從 config 讀取所有可能路徑
        possible_paths = config.get("burnInTest_paths", [])

        burn_path = None
        for path in possible_paths:
            if os.path.exists(path):
                burn_path = path
                print(f"找到 BurnInTest 路徑: {path}")
                break

        # 若都找不到
        if not burn_path:
            print("❌ 找不到 BurnInTest 執行檔，請確認 config.json 中的路徑設定。")
            return

        subprocess.Popen(burn_path)
        time.sleep(20)
        adjust_window(['BurnInTest'], x, y, width, height)
        time.sleep(1)

        # 先將焦點切到桌面
        pyautogui.press('winleft')
        time.sleep(1)
        pyautogui.press('winleft')
        time.sleep(1)

        # 再切回 BurnInTest 視窗並啟動測試
        window = gw.getWindowsWithTitle('BurnInTest')
        if window:
            window[0].activate()
            time.sleep(1)
            pyautogui.press('f4')
            print("已按下 F4 啟動測試。")
        else:
            print("無法找到 BurnInTest 視窗")
        time.sleep(10)
    except Exception as e:
        print("open_burnInTest 錯誤:", e)


def adjust_window(titles, x, y, width, height):
    attempt = 0
    window_found = False
    while attempt < 40:
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
    time.sleep(1)
    if not window_found:
        print("找不到符合的視窗，已跳過。")


def open_and_layout_windows():
    screen_width, screen_height = pyautogui.size()
    screen_height -= 50

    w_half = int(screen_width * 0.5)
    open_burn(0, 0, w_half, screen_height)

    # 裝置管理員寬度
    width_dm = int(screen_width * 0.2)

    # 增加上方空間
    space_y = int(screen_height * 0.05)
    space_x = int(space_y * 1.5)
    open_camera(space_x, space_y, w_half - space_x, int(screen_height * 0.7))

    open_device_manager(screen_width - width_dm, 0, width_dm, screen_height)

    # 先開影片、電池頁面(可能蓋到裝置管理員)
    remaining_w = screen_width - width_dm - w_half
    open_media_player(w_half, space_y, remaining_w, int(screen_height * 0.34))
    open_battery_setting(w_half, int(screen_height * 0.65), remaining_w, int(screen_height * 0.3))

    height_dw = int(screen_height * 0.25)
    open_device_watcher(screen_width - width_dm, screen_height-height_dw, width_dm, height_dw)

    open_keyboard_test(w_half, int(screen_height * 0.4), remaining_w, int(screen_height * 0.3))


def open_white_window():
    try:
        subprocess.Popen([str(app_path(config["white_window_path"]))])
        for i in range(1, 15):
            windows = gw.getWindowsWithTitle("white")
            if windows:
                break
            time.sleep(1)
    except Exception as e:
        print("open_keyboard_test 錯誤:", e)


if __name__ == "__main__":
    open_paint_maximize()
    open_white_window()
    open_and_layout_windows()
