import ctypes
import time

# 虛擬鍵碼定義
VK_NUMLOCK = 0x90
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002

# 模擬按下和放開 NumLock 鍵
def toggle_numlock():
    # 模擬按鍵
    ctypes.windll.user32.keybd_event(VK_NUMLOCK, 0x45, KEYEVENTF_EXTENDEDKEY, 0)
    # 模擬放開
    ctypes.windll.user32.keybd_event(VK_NUMLOCK, 0x45, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)

# 執行範例
toggle_numlock()
time.sleep(1)
toggle_numlock()
