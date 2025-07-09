import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPalette, QColor
import pygetwindow as gw

# 定義要測試的一般按鍵列表
key_list_general = [
    'Esc', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
    '`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace',
    'Tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\',
    'CapsLock', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', '\'', 'Enter',
    'Shift_L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'Shift_R',
    'Ctrl_L', 'Alt_L', 'Space', 'Alt_R', 'Ctrl_R', 'Insert', 'Delete', 'Home',
    'End', 'PageUp', 'PageDown', 'Up', 'Down', 'Left', 'Right'
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
    'Shift_L': QtCore.Qt.Key_Shift,
    'Shift_R': QtCore.Qt.Key_Shift,
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
    'Ctrl_L': QtCore.Qt.Key_Control,
    'Ctrl_R': QtCore.Qt.Key_Control,
    'Alt_L': QtCore.Qt.Key_Alt,
    'Alt_R': QtCore.Qt.Key_Alt,
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
        # 測試是否已經開始的旗標
        self.test_started = False
        # 是否處於數字鍵盤測試模式
        self.in_numeric_test = False
        # 當前使用的按鍵列表（初始為一般鍵盤）
        self.key_list = key_list_general
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
        self.setGeometry(100, 100, 500, 200)

        # 創建標籤用於顯示提示文字
        self.label = QtWidgets.QLabel("", self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)  # 啟用文字自動換行
        font = self.label.font()
        font.setPointSize(20)
        self.label.setFont(font)

        # 使用垂直佈局管理器
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # 初次顯示要求按下 Enter 鍵 3 次
        self.display_start_message()

    def display_start_message(self):
        """顯示要求按下 Enter 鍵 3 次的起始訊息"""
        self.label.setText("Press Enter key 3 times to start the test.")
        self.set_background_color("white")

    def display_current_key(self):
        """更新顯示當前需要按下的按鍵"""
        if self.current_key_index >= len(self.key_list):
            # 如果已經測試完所有按鍵
            if self.in_numeric_test:
                # 如果是數字鍵盤測試完成
                self.label.setText("Numeric keypad test complete!\n"
                                   "Press Enter 3 times to restart")
            else:
                # 一般鍵盤測試完成
                self.label.setText("Keyboard test complete!\n"
                                   "Press Enter 3 times to restart\n"
                                   "Press Right key 3 times to enter numeric keypad test.")
            self.set_background_color(QColor(0, 200, 0))  # 綠色
            # 停止鍵盤按鍵計時
            if self.key_timeout_timer.isActive():
                self.key_timeout_timer.stop()
            # 啟動定時器，20秒後恢復白色背景
            if self.reset_timer.isActive():
                self.reset_timer.stop()
            self.reset_timer.start(20000)  # 20,000 毫秒 = 20 秒
        else:
            # 顯示當前需要按下的按鍵
            self.label.setText(f"Please press: {self.key_list[self.current_key_index]}\n(If unavailable, press Esc key to skip)")
            self.set_background_color("white")
            # 停止定時器，如果正在運行
            if self.reset_timer.isActive():
                self.reset_timer.stop()
            # 開始鍵盤按鍵計時，5秒沒按下正確按鍵變紅色
            if self.key_timeout_timer.isActive():
                self.key_timeout_timer.stop()
            self.key_timeout_timer.start(20000)

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
        """根據按鍵代碼獲取按鍵名稱，主要用於調試輸出"""
        # 反向查找 key_mapping 中的鍵名
        for name, code in key_mapping.items():
            if key == code:
                return name
        # 處理字母和其他可打印字符
        if 32 <= key <= 126:
            return chr(key)
        return f"Unknown key ({key})"

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return  # 忽略長按產生的重複事件

        """處理按鍵事件"""
        key = event.key()
        key_name = self.get_key_name(key)
        print(f"Key pressed: {key_name}")

        # 初次啟動和測試完成後皆需按下 Enter 或 Right 鍵 3 次才能繼續
        if not self.test_started or self.current_key_index >= len(self.key_list):
            if key == QtCore.Qt.Key_Return or key == QtCore.Qt.Key_Enter:
                # 按下 Enter 鍵計數
                self.enter_press_count += 1
                self.right_press_count = 0  # 重置 Right 鍵計數
                if self.enter_press_count >= 3:
                    # 重新開始一般鍵盤測試
                    self.test_started = True
                    self.in_numeric_test = False  # 設定為一般鍵盤測試模式
                    self.current_key_index = 0
                    self.enter_press_count = 0
                    self.key_list = key_list_general  # 切換回一般鍵盤按鍵列表
                    self.display_current_key()
            # 按下 Right 鍵計數進入數字鍵盤測試
            elif key == QtCore.Qt.Key_Right and not self.in_numeric_test:
                # 按下 Right 鍵計數
                self.right_press_count += 1
                self.enter_press_count = 0  # 重置 Enter 鍵計數
                if self.right_press_count >= 3:
                    # 進入數字鍵盤測試
                    self.test_started = True
                    self.in_numeric_test = True  # 設定為數字鍵盤測試模式
                    self.current_key_index = 0
                    self.right_press_count = 0
                    self.key_list = key_list_numeric  # 切換到數字鍵盤按鍵列表
                    self.display_current_key()
            # 按下 Space 鍵計數切換視窗
            elif key == QtCore.Qt.Key_Space:
                self.space_press_count += 1
                if self.space_press_count >= 3:
                    self.space_press_count = 0
                    self.focus_touch_test_window()
                return
            else:
                # 其他按鍵，重置計數
                self.enter_press_count = 0
                self.right_press_count = 0
                self.space_press_count = 0
            return

        # 獲取當前應按下的按鍵
        expected_key_name = self.key_list[self.current_key_index]
        expected_key = key_mapping.get(expected_key_name, None)

        if key == QtCore.Qt.Key_Escape:
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

    def focus_touch_test_window(self):
        try:
            windows = gw.getWindowsWithTitle("touch test")
            if windows:
                win = windows[0]
                if win.isMinimized:
                    win.restore()  # 還原視窗
                win.activate()  # 聚焦視窗
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
