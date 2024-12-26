import ctypes
import winreg as reg
import time

# 定義必要的參數
HWND_BROADCAST = 0xFFFF
WM_SETTINGCHANGE = 0x1A

def set_touch_indicator():
    try:
        # 打開指定的登錄檔位置
        key_path = r"Control Panel\Cursors"
        reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_SET_VALUE)

        # 設定 ContactVisualization 和 GestureVisualization 的值
        reg.SetValueEx(reg_key, "ContactVisualization", 0, reg.REG_DWORD, 2)
        reg.SetValueEx(reg_key, "GestureVisualization", 0, reg.REG_DWORD, 31)

        # 關閉登錄檔鍵
        reg.CloseKey(reg_key)

        print("觸控指示器設定已更新！")

    except Exception as e:
        print(f"無法修改登錄檔: {e}")

def refresh_settings():
    try:
        # 使用 ctypes 呼叫 SendMessageTimeout API 刷新設定
        ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment", 0x2, 5000, None)
        print("設定已刷新！")
    except Exception as e:
        print(f"無法刷新設定: {e}")

# 執行設定函數
set_touch_indicator()

# 等待一會讓登錄檔更新
time.sleep(1)

# 刷新設定
refresh_settings()
