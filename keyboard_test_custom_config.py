import sys
import json
from pathlib import Path

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPalette, QColor
import pygetwindow as gw
from touchpad_controller import ensure_touchpad_on
import pyautogui
import win32gui, win32con, win32api


# 定義要測試的一般按鍵列表
# Shift / Ctrl 不分左右鍵
key_list_general = [
    'Esc', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
    'Home', 'End', 'Insert', 'Delete', 'PageUp', 'PageDown',
    '`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace',
    'Tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\',
    'CapsLock', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', '\'', 'Enter',
    'Shift', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'Up',
    'Ctrl', 'Alt', 'Space', 'Left', 'Down', 'Right'
]

# 定義要測試的數字鍵盤按鍵列表
key_list_numeric = [
    'NumLock *2', 'NumLock', '/', '*', '-',
    '7', '8', '9', '+',
    '4', '5', '6',
    '1', '2', '3', 'Enter_Numpad',
    '0', '.'
]

# 建立按鍵名稱與 PyQt 的鍵代碼對應關係
# Shift / Ctrl 不分左右鍵
key_mapping = {
    'Esc': QtCore.Qt.Key_Escape,
    'F1': QtCore.Qt.Key_F1,
    'F2': QtCore.Qt.Key_F2,
    'F3': QtCore.Qt.Key_F3,
    'F4': QtCore.Qt.Key_F4,
    'F5': QtCore.Qt.Key_F5,
    'F6': QtCore.Qt.Key_F6,
    'F7': QtCore.Qt.Key_F7,
    'F8': QtCore.Qt.Key_F8,
    'F9': QtCore.Qt.Key_F9,
    'F10': QtCore.Qt.Key_F10,
    'F11': QtCore.Qt.Key_F11,
    'F12': QtCore.Qt.Key_F12,
    '`': QtCore.Qt.Key_QuoteLeft,
    '1': QtCore.Qt.Key_1,
    '2': QtCore.Qt.Key_2,
    '3': QtCore.Qt.Key_3,
    '4': QtCore.Qt.Key_4,
    '5': QtCore.Qt.Key_5,
    '6': QtCore.Qt.Key_6,
    '7': QtCore.Qt.Key_7,
    '8': QtCore.Qt.Key_8,
    '9': QtCore.Qt.Key_9,
    '0': QtCore.Qt.Key_0,
    '-': QtCore.Qt.Key_Minus,
    '=': QtCore.Qt.Key_Equal,
    'Backspace': QtCore.Qt.Key_Backspace,
    'Tab': QtCore.Qt.Key_Tab,
    'Q': QtCore.Qt.Key_Q,
    'W': QtCore.Qt.Key_W,
    'E': QtCore.Qt.Key_E,
    'R': QtCore.Qt.Key_R,
    'T': QtCore.Qt.Key_T,
    'Y': QtCore.Qt.Key_Y,
    'U': QtCore.Qt.Key_U,
    'I': QtCore.Qt.Key_I,
    'O': QtCore.Qt.Key_O,
    'P': QtCore.Qt.Key_P,
    '[': QtCore.Qt.Key_BracketLeft,
    ']': QtCore.Qt.Key_BracketRight,
    '\\': QtCore.Qt.Key_Backslash,
    'CapsLock': QtCore.Qt.Key_CapsLock,
    'A': QtCore.Qt.Key_A,
    'S': QtCore.Qt.Key_S,
    'D': QtCore.Qt.Key_D,
    'F': QtCore.Qt.Key_F,
    'G': QtCore.Qt.Key_G,
    'H': QtCore.Qt.Key_H,
    'J': QtCore.Qt.Key_J,
    'K': QtCore.Qt.Key_K,
    'L': QtCore.Qt.Key_L,
    ';': QtCore.Qt.Key_Semicolon,
    '\'': QtCore.Qt.Key_Apostrophe,
    'Enter': QtCore.Qt.Key_Return,
    'Shift': QtCore.Qt.Key_Shift,
    'Z': QtCore.Qt.Key_Z,
    'X': QtCore.Qt.Key_X,
    'C': QtCore.Qt.Key_C,
    'V': QtCore.Qt.Key_V,
    'B': QtCore.Qt.Key_B,
    'N': QtCore.Qt.Key_N,
    'M': QtCore.Qt.Key_M,
    ',': QtCore.Qt.Key_Comma,
    '.': QtCore.Qt.Key_Period,
    '/': QtCore.Qt.Key_Slash,
    'Ctrl': QtCore.Qt.Key_Control,
    'Alt': QtCore.Qt.Key_Alt,
    'Space': QtCore.Qt.Key_Space,
    'Insert': QtCore.Qt.Key_Insert,
    'Delete': QtCore.Qt.Key_Delete,
    'Home': QtCore.Qt.Key_Home,
    'End': QtCore.Qt.Key_End,
    'PageUp': QtCore.Qt.Key_PageUp,
    'PageDown': QtCore.Qt.Key_PageDown,
    'Up': QtCore.Qt.Key_Up,
    'Down': QtCore.Qt.Key_Down,
    'Left': QtCore.Qt.Key_Left,
    'Right': QtCore.Qt.Key_Right,
    # 數字鍵盤按鍵對應
    'NumLock': QtCore.Qt.Key_NumLock,
    'NumLock *2': QtCore.Qt.Key_NumLock,
    '*': QtCore.Qt.Key_Asterisk,
    '+': QtCore.Qt.Key_Plus,
    'Enter_Numpad': QtCore.Qt.Key_Enter,
}


LEGACY_KEY_NAME_MAP = {
    'Shift_L': 'Shift',
    'Shift_R': 'Shift',
    'Ctrl_L': 'Ctrl',
    'Ctrl_R': 'Ctrl',
    'Alt_L': 'Alt',
    'Alt_R': 'Alt',
}


def normalize_key_name(key_name):
    return LEGACY_KEY_NAME_MAP.get(key_name, key_name)


def get_app_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).parent


CONFIG_PATH = get_app_dir() / "keyboard_config.json"
DEFAULT_CONFIG = {
    "custom_keys": key_list_general
}


def save_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)


def load_config():
    """讀取 keyboard_config.json；不存在、空檔、空清單、格式錯誤都回預設順序。"""
    if not CONFIG_PATH.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    try:
        raw_text = CONFIG_PATH.read_text(encoding="utf-8").strip()
        if not raw_text:
            return DEFAULT_CONFIG.copy()

        config = json.loads(raw_text)
    except Exception as e:
        print("讀取 keyboard_config.json 失敗，使用預設值:", e)
        return DEFAULT_CONFIG.copy()

    if not isinstance(config, dict):
        return DEFAULT_CONFIG.copy()

    custom_keys = config.get("custom_keys", [])
    if not isinstance(custom_keys, list):
        custom_keys = []

    valid_keys = []
    for key_name in custom_keys:
        if not isinstance(key_name, str):
            continue

        normalized_name = normalize_key_name(key_name)
        if normalized_name in key_mapping:
            valid_keys.append(normalized_name)

    if not valid_keys:
        valid_keys = key_list_general

    return {
        "custom_keys": valid_keys
    }


class KeyboardTestApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # 當前測試的按鍵索引
        self.current_key_index = 0
        # Enter 鍵連續按下計數
        self.enter_press_count = 0
        # Right 鍵連續按下計數
        self.right_press_count = 0
        # Space 鍵連續按下計數
        self.space_press_count = 0
        # S 鍵連續按下計數，只在未開始 / 測試完成時有效
        self.s_press_count = 0
        # 測試是否已經開始的旗標
        self.test_started = False
        # 是否處於數字鍵盤測試模式
        self.in_numeric_test = False
        # 是否處於自訂按鍵模式
        self.custom_mode = False
        # 自訂模式暫存按鍵列表
        self.custom_key_list = []
        # 自訂模式只記錄：在自訂模式內按下、並且放開的完整按鍵週期
        # 避免 S x3 進入自訂模式時，最後一次 S 的 keyRelease 被誤加入
        self.custom_pressed_keys = set()
        # ensure_topmost_and_focus 會用 Win32 模擬 ALT 來搶焦，避免被判定成使用者按鍵
        self.ignore_focus_alt_event = False
        # 讀取設定檔
        self.config = load_config()
        # 當前使用的按鍵列表（初始為 config 內自訂鍵，空值則為預設一般鍵盤）
        self.key_list = self.config["custom_keys"]
        # 定時器，用於在測試完成後延時變回白色背景
        self.reset_timer = QtCore.QTimer()
        self.reset_timer.timeout.connect(self.reset_background_color)
        # 定時器，用於在測試中途超過時間變成紅色背景
        self.key_timeout_timer = QtCore.QTimer()
        self.key_timeout_timer.timeout.connect(self.timeout_set_background_color)
        self.init_ui()
        self.show()

    def init_ui(self):
        """初始化介面元素"""
        self.setWindowTitle("Keyboard Test")
        self.setGeometry(100, 100, 500, 150)
        self.setMinimumSize(500, 150)

        # 置於 __init__ 的結尾附近（init_ui() 之後）
        self.guard_enabled = True  # 是否執行「置頂+搶焦」
        self.pause_secs = 60  # 三連空白後暫停秒數

        self.raise_()
        self.activateWindow()
        self.setFocus()

        # 每秒維持一次置頂+聚焦（僅在 guard_enabled=True 時才做）
        self.topmost_timer = QtCore.QTimer(self)
        self.topmost_timer.timeout.connect(lambda: self.ensure_topmost_and_focus())
        self.topmost_timer.start(3000)

        # 創建標籤用於顯示提示文字
        self.label = QtWidgets.QLabel("", self)
        self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)  # 啟用文字自動換行
        font = self.label.font()
        font.setPointSize(20)
        self.label.setFont(font)

        # 使用捲動區域，避免自訂按鍵順序太長時看不到
        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroll_area.setWidget(self.label)

        # 使用垂直佈局管理器
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.scroll_area)
        self.setLayout(layout)

        # 初次顯示要求按下 Enter 鍵 3 次
        self.display_start_message()

    def ensure_topmost_and_focus(self):
        """確保本視窗為 TOPMOST，必要時把焦點搶回來"""
        hwnd = int(self.winId())

        try:
            # 置頂（Win32，覆蓋一些框架在特定情況被降層）
            win32gui.SetWindowPos(
                hwnd,
                win32con.HWND_TOPMOST,
                0, 0, 0, 0,
                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW
            )
        except Exception as e:
            print("置頂失敗:", e)
            return

        try:
            # Windows 防止任意搶焦點，按住 ALT 可降低限制
            # 這個 ALT 是程式自動送出的，keyPressEvent 會濾掉，不列入測試
            self.ignore_focus_alt_event = True
            win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)  # ALT down

            # 顯示但不激活，再前景化
            win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
            win32gui.SetForegroundWindow(hwnd)
            # Qt 端同步提升
            self.raise_()
            self.activateWindow()
            self.setFocus()

        except Exception as e:
            print("Focus error:", e)
        finally:
            try:
                win32api.keybd_event(
                    win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0
                )
            except:
                pass
            QtCore.QTimer.singleShot(300, lambda: setattr(self, "ignore_focus_alt_event", False))

    def pause_guard(self):
        # 立刻取消置頂（Win32）
        try:
            hwnd = int(self.winId())
            win32gui.SetWindowPos(
                hwnd,
                win32con.HWND_NOTOPMOST,
                0, 0, 0, 0,
                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW
            )
        except Exception as e:
            print("pause_guard 取消置頂失敗:", e)

        # 停掉每 3 秒自動置頂的定時器，避免又被拉回去
        if self.topmost_timer.isActive():
            self.topmost_timer.stop()

        # 不要 setWindowFlag、不用 show()
        QtCore.QTimer.singleShot(self.pause_secs * 1000, self.resume_guard)

    def resume_guard(self):
        # 重新啟動定時器
        if not self.topmost_timer.isActive():
            self.topmost_timer.start(3000)

        # 不要 setWindowFlag、不用 show()
        QtCore.QTimer.singleShot(10, lambda: self.ensure_topmost_and_focus())

    def display_start_message(self):
        """顯示起始訊息"""
        self.label.setText(
            "按 Enter 3 次開始測試。\n"
            "按 S 3 次進入自訂按鍵模式。\n"
            f"目前自訂按鍵數量：{len(self.config['custom_keys'])}"
        )
        self.set_background_color("white")

    def display_current_key(self):
        """更新顯示當前需要按下的按鍵"""
        if self.current_key_index >= len(self.key_list):
            if self.in_numeric_test:
                self.label.setText(
                    "數字鍵盤測試完成！\n"
                    "按 Enter 3 次重新開始"
                )
            else:
                self.label.setText(
                    "鍵盤測試完成！\n"
                    "按 Enter 3 次重新開始\n"
                    "按 S 3 次進入自訂按鍵模式\n"
                    "按 Right 3 次進入數字鍵盤測試"
                )
            self.set_background_color(QColor(0, 200, 0))
            if self.key_timeout_timer.isActive():
                self.key_timeout_timer.stop()
            if self.reset_timer.isActive():
                self.reset_timer.stop()
            self.reset_timer.start(240000)
        else:
            self.label.setText(
                f"請按下：{self.key_list[self.current_key_index]}\n"
                "如果沒有這顆按鍵，按 Esc 跳過"
            )
            self.set_background_color("white")
            if self.reset_timer.isActive():
                self.reset_timer.stop()
            if self.key_timeout_timer.isActive():
                self.key_timeout_timer.stop()
            self.key_timeout_timer.start(30000)

    def enter_custom_mode(self):
        """進入自訂按鍵模式"""
        self.custom_mode = True
        self.custom_key_list = []
        self.custom_pressed_keys.clear()
        self.enter_press_count = 0
        self.right_press_count = 0
        self.space_press_count = 0
        self.s_press_count = 0
        self.test_started = False
        self.current_key_index = 0

        if self.key_timeout_timer.isActive():
            self.key_timeout_timer.stop()
        if self.reset_timer.isActive():
            self.reset_timer.stop()

        # 只有進入自訂模式後才放大視窗
        # self.setMinimumSize(700, 450)
        self.resize(600, 520)

        self.set_background_color(QColor(255, 255, 180))
        self.label.setText(
            "自訂按鍵模式\n"
            "請依照想測試的順序按下按鍵。\n"
            "按 Ctrl + S 儲存。\n\n"
            "目前按鍵數量：0"
        )

    def format_key_sequence(self, keys, keys_per_line=10):
        """將按鍵順序固定分行，避免一整排太長看不到。"""
        lines = []
        for i in range(0, len(keys), keys_per_line):
            lines.append(" → ".join(keys[i:i + keys_per_line]))
        return "\n".join(lines)

    def update_custom_mode_display(self, last_key_name=None):
        """更新自訂模式畫面"""
        key_sequence = self.format_key_sequence(self.custom_key_list, keys_per_line=8)

        text = "自訂按鍵模式\n"
        text += "請依照想測試的順序按下按鍵。\n"
        text += "按 Ctrl + S 儲存。\n\n"

        if last_key_name:
            text += f"剛加入：{last_key_name}\n"

        text += f"目前按鍵數量：{len(self.custom_key_list)}"

        if key_sequence:
            text += f"\n\n目前順序：\n{key_sequence}"

        self.label.setText(text)
        self.label.adjustSize()

    def save_custom_keys(self):
        """儲存自訂按鍵清單，儲存後回到等待 Enter x3 開始測試。"""
        if not self.custom_key_list:
            self.config["custom_keys"] = key_list_general
        else:
            self.config["custom_keys"] = self.custom_key_list

        save_config(self.config)

        self.key_list = self.config["custom_keys"]
        self.custom_mode = False
        self.test_started = False
        self.in_numeric_test = False
        self.current_key_index = 0
        self.enter_press_count = 0
        self.right_press_count = 0
        self.space_press_count = 0
        self.s_press_count = 0

        self.set_background_color(QColor(255, 255, 255))
        self.resize(500, 150)
        self.label.setText(
            "自訂按鍵已儲存！\n"
            f"總按鍵數量：{len(self.key_list)}\n"
            "按 Enter 3 次開始測試。"
        )

    def set_background_color(self, color):
        """更改背景顏色"""
        palette = self.palette()
        if isinstance(color, QColor):
            palette.setColor(QPalette.Window, color)
        else:
            palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

    def reset_background_color(self):
        """在定時器超時後，將背景顏色重置為白色"""
        self.set_background_color("white")
        # 停止定時器
        self.reset_timer.stop()

    def timeout_set_background_color(self):
        """在按鍵定時器超時後，將背景顏色設為紅色"""
        self.set_background_color(QColor(220, 0, 0))
        # 停止定時器
        self.key_timeout_timer.stop()

    def get_key_name(self, key):
        """根據按鍵代碼獲取按鍵名稱，Shift / Ctrl 不分左右。"""
        if key == QtCore.Qt.Key_Shift:
            return "Shift"
        if key == QtCore.Qt.Key_Control:
            return "Ctrl"
        if key == QtCore.Qt.Key_Alt:
            return "Alt"
        if key == QtCore.Qt.Key_Return:
            return "Enter"
        if key == QtCore.Qt.Key_Enter:
            return "Enter_Numpad"

        # 反向查找 key_mapping 中的鍵名
        for name, code in key_mapping.items():
            if key == code:
                return name
        # 處理字母和其他可打印字符
        if 32 <= key <= 126:
            return chr(key).upper()
        return f"Unknown key ({key})"

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return  # 忽略長按產生的重複事件

        """處理按鍵事件"""
        key = event.key()
        key_name = self.get_key_name(key)
        modifiers = event.modifiers()

        # 濾掉 ensure_topmost_and_focus 為了搶焦點自動送出的 ALT
        if key == QtCore.Qt.Key_Alt and self.ignore_focus_alt_event:
            return

        print(f"按下按鍵：{key_name}")

        # 自訂模式：必須在自訂模式內完成 keyPress + keyRelease 才加入。
        # 這樣 S x3 進入自訂模式時，第三次 S 的 keyRelease 不會被誤記錄。
        # Ctrl + S 仍作為儲存快捷鍵，不會把 Ctrl / S 加入清單。
        if self.custom_mode:
            if modifiers & QtCore.Qt.ControlModifier and key == QtCore.Qt.Key_S:
                print("自訂按鍵儲存快捷鍵：Ctrl + S")
                self.custom_pressed_keys.clear()
                self.save_custom_keys()
                return

            self.custom_pressed_keys.add(key)
            return

        # 初次啟動和測試完成後皆需按下 Enter / Right / S / Space 鍵 3 次才能繼續
        # S x3 只在這個區塊有效，不會影響測試中的 S 鍵
        if not self.test_started or self.current_key_index >= len(self.key_list):
            if key == QtCore.Qt.Key_Return or key == QtCore.Qt.Key_Enter:
                # 按下 Enter 鍵計數
                self.enter_press_count += 1
                self.right_press_count = 0
                self.space_press_count = 0
                self.s_press_count = 0

                if self.enter_press_count >= 3:
                    # 開始一般鍵盤測試，使用 config 內的 custom_keys；若 json 空值則 load_config 已回預設順序
                    self.config = load_config()
                    self.test_started = True
                    self.in_numeric_test = False
                    self.current_key_index = 0
                    self.enter_press_count = 0
                    self.key_list = self.config["custom_keys"]
                    self.display_current_key()

            # 按下 S 鍵計數進入自訂模式
            elif key == QtCore.Qt.Key_S:
                self.s_press_count += 1
                self.enter_press_count = 0
                self.right_press_count = 0
                self.space_press_count = 0

                if self.s_press_count >= 3:
                    self.enter_custom_mode()

            # 按下 Right 鍵計數進入數字鍵盤測試
            elif key == QtCore.Qt.Key_Right and not self.in_numeric_test:
                self.right_press_count += 1
                self.enter_press_count = 0
                self.space_press_count = 0
                self.s_press_count = 0

                if self.right_press_count >= 3:
                    # 進入數字鍵盤測試
                    self.test_started = True
                    self.in_numeric_test = True
                    self.current_key_index = 0
                    self.right_press_count = 0
                    self.key_list = key_list_numeric
                    self.display_current_key()

            # 按下 Space 鍵計數切換視窗
            elif key == QtCore.Qt.Key_Space:
                self.space_press_count += 1
                self.enter_press_count = 0
                self.right_press_count = 0
                self.s_press_count = 0

                if self.space_press_count >= 3:
                    self.space_press_count = 0
                    self.pause_guard()
                    self.focus_touch_test_window()
                return
            elif key == QtCore.Qt.Key_Alt:
                # 手動按 Alt 不做啟動/切換計數；測試中若目前目標是 Alt 仍會正常判定
                pass
            else:
                # 其他按鍵，重置計數
                self.enter_press_count = 0
                self.right_press_count = 0
                self.space_press_count = 0
                self.s_press_count = 0
            return

        # 獲取當前應按下的按鍵
        expected_key_name = self.key_list[self.current_key_index]
        expected_key = key_mapping.get(expected_key_name, None)

        if key_name == "`" or key_name == "Esc":
            # 按下 Esc 鍵，跳過當前按鍵
            self.current_key_index += 1
            self.display_current_key()
        elif key == expected_key:
            # 按下的鍵與期望的鍵匹配
            self.current_key_index += 1
            self.display_current_key()
        else:
            # 按錯了鍵，可以在此處添加提示訊息或記錄
            pass

    def keyReleaseEvent(self, event):
        """自訂模式使用放開按鍵作為加入點，避免 Ctrl + S 把 Ctrl 誤加入。"""
        if not self.custom_mode:
            return

        if event.isAutoRepeat():
            return

        key = event.key()
        key_name = self.get_key_name(key)

        # 濾掉 ensure_topmost_and_focus 為了搶焦點自動送出的 ALT
        if key == QtCore.Qt.Key_Alt and self.ignore_focus_alt_event:
            return

        # 只有在自訂模式內有收到 keyPress，並且又收到 keyRelease，才算一次完整觸發。
        # 用來排除進入自訂模式前已經按下、進入後才放開的第三次 S。
        if key not in self.custom_pressed_keys:
            return

        self.custom_pressed_keys.discard(key)

        if key_name in key_mapping:
            self.custom_key_list.append(key_name)
            print(f"自訂按鍵加入：{key_name}")
            self.update_custom_mode_display(key_name)
        else:
            print(f"不支援的按鍵：{key_name}")

    def focus_touch_test_window(self):
        try:
            windows = gw.getWindowsWithTitle("Touch Test")
            if windows:
                # 開啟 touchpad
                ensure_touchpad_on()

                # 🖱️ 將滑鼠移到螢幕正中央
                screen_width, screen_height = pyautogui.size()
                pyautogui.moveTo(screen_width // 2, screen_height // 2)
                print("滑鼠已移動到螢幕正中央")

                win = windows[0]
                if win.isMinimized:
                    win.restore()  # 還原視窗
                QtCore.QTimer.singleShot(0, lambda: win.activate())  # 聚焦視窗
                print("已叫出並聚焦 touch test 視窗")
            else:
                print("找不到 touch test 視窗")
        except Exception as e:
            print("切換視窗時發生錯誤:", e)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = KeyboardTestApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
