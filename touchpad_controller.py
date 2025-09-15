# touchpad_controller.py
import ctypes
import winreg
from typing import Optional

# ========== 熱鍵切換 (Ctrl+Win+F24) ==========
user32 = ctypes.windll.user32
KEYEVENTF_KEYUP = 0x0002
VK_LCTRL, VK_LWIN, VK_F24 = 0xA2, 0x5B, 0x87


def toggle_by_hotkey():
    """送出 Ctrl+Win+F24，切換 Precision Touchpad On/Off"""
    user32.keybd_event(VK_LCTRL, 0, 0, 0)
    user32.keybd_event(VK_LWIN,  0, 0, 0)
    user32.keybd_event(VK_F24,   0, 0, 0)
    user32.keybd_event(VK_F24,   0, KEYEVENTF_KEYUP, 0)
    user32.keybd_event(VK_LWIN,  0, KEYEVENTF_KEYUP, 0)
    user32.keybd_event(VK_LCTRL, 0, KEYEVENTF_KEYUP, 0)


# ========== 讀取登錄檔狀態 ==========
KEY = r"Software\Microsoft\Windows\CurrentVersion\PrecisionTouchPad\Status"


def get_touchpad_state() -> Optional[bool]:
    """
    讀取觸控板狀態
    回傳 True=開, False=關, None=讀不到(此機型不支援)
    """
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, KEY) as k:
            val, _ = winreg.QueryValueEx(k, "Enabled")
            return bool(val)
    except FileNotFoundError:
        return None
    except OSError:
        return None


# ========== 確保指定狀態 ==========
def ensure_touchpad_on():
    """確保觸控板為 ON"""
    state = get_touchpad_state()
    if state is False:  # 目前關閉，執行 toggle
        toggle_by_hotkey()
    return get_touchpad_state()


def ensure_touchpad_off():
    """確保觸控板為 OFF"""
    state = get_touchpad_state()
    if state is True:  # 目前開啟，執行 toggle
        toggle_by_hotkey()
    return get_touchpad_state()


def toggle_touchpad():
    """單純切換"""
    toggle_by_hotkey()
    return get_touchpad_state()


# ========== 測試 ==========
if __name__ == "__main__":
    print("初始狀態:", get_touchpad_state())
    print("強制 OFF:", ensure_touchpad_off())
    print("強制 ON:", ensure_touchpad_on())
