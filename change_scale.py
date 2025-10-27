import winreg
import subprocess
import time
import ctypes
from ctypes import wintypes


# ===== 你可調的參數 =====
# APP 在「1920x1200、100%」時的最小視窗
BASE_MIN_W = 500
BASE_MIN_H = 330

# 你想要的視窗佔比
TARGET_W_RATIO = 0.30
TARGET_H_RATIO = 0.35

# Windows 常見可用縮放清單（可依需要增減）
SUPPORTED_SCALES = [100, 125, 150, 175, 200, 225, 250, 300]

# 登錄檔位置（使用「全域/每使用者」的傳統 DPI 方式；需重啟 Explorer/可能要登出）
REG_PATH = r"Control Panel\Desktop"

# 對應表：百分比 -> LogPixels
# 100%=96, 125%=120, 150%=144, 175%=168, 200%=192, 225%=216, 250%=240, 300%=288
def percent_to_logpixels(percent: int) -> int:
    return round(96 * (percent / 100.0))

# 取得工作區(扣掉工作列)大小
def get_work_area():
    SPI_GETWORKAREA = 0x0030
    rect = wintypes.RECT()
    ctypes.windll.user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0)
    work_w = rect.right - rect.left
    work_h = rect.bottom - rect.top
    return work_w, work_h

def compute_recommended_scale(work_w, work_h):
    target_w = work_w * TARGET_W_RATIO
    target_h = work_h * TARGET_H_RATIO
    s_max_w = (target_w / BASE_MIN_W) * 100.0
    s_max_h = (target_h / BASE_MIN_H) * 100.0
    s_max = min(s_max_w, s_max_h)
    # 在受支援縮放中，取 <= s_max 的最大值；至少 100%
    candidates = [s for s in SUPPORTED_SCALES if s <= max(100, s_max)]
    if not candidates:
        return 100
    return max(candidates)

def set_windows_scale(percent: int):
    # 寫入 HKCU\Control Panel\Desktop：
    # Win8DpiScaling=1 啟用覆寫；LogPixels=對應 DPI
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, "Win8DpiScaling", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(key, "LogPixels", 0, winreg.REG_DWORD, percent_to_logpixels(percent))
    # 重啟 Explorer（多數情況會套用；仍可能需要登出）
    print("[INFO] 已寫入登錄。請在下次登入或重新開機後生效。")

def main():
    work_w, work_h = get_work_area()
    rec_scale = compute_recommended_scale(work_w, work_h)
    print(f"[INFO] 工作區: {work_w}x{work_h}")
    print(f"[INFO] 建議系統縮放：{rec_scale}%")
    set_windows_scale(rec_scale)
    print("[INFO] 已寫入登錄登出或重新開機生效。")

if __name__ == "__main__":
    # 以避免本程式自身被系統 DPI 拉伸，開啟 Per-Monitor DPI 感知（可有可無）
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PER_MONITOR_AWARE
    except Exception:
        pass
    main()
    time.sleep(3)
