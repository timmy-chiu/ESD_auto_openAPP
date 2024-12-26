import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QKeySequence, QPalette, QColor

# 定義要測試的按鍵列表
key_list = [
    'Esc', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
    '', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace',
    'Tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\',
    'CapsLock', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', '\'', 'Enter',
    'Shift_L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'Shift_R',
    'Ctrl_L', 'Alt_L', 'Space', 'Alt_R', 'Ctrl_R', 'Insert', 'Delete', 'Home',
    'End', 'PageUp', 'PageDown', 'Up', 'Down', 'Left', 'Right'
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
    '': QtCore.Qt.Key_QuoteLeft,
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
    'Right': QtCore.Qt.Key_Right
}

class KeyboardTestApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.current_key_index = 0
        self.enter_press_count = 0
        self.test_started = False  # 是否已經開始測試的旗標
        self.init_ui()
        self.show()

    def init_ui(self):
        """初始化介面元素"""
        self.setWindowTitle("Keyboard Test")
        self.setGeometry(100, 100, 500, 200)

        # 創建標籤用於顯示提示文字
        self.label = QtWidgets.QLabel("", self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
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
        self.label.setText("Press Enter 3 times to start the test.")
        self.set_background_color("white")

    def display_current_key(self):
        """更新顯示當前需要按下的按鍵"""
        if self.current_key_index >= len(key_list):
            # 如果已經測試完所有按鍵
            self.label.setText("Keyboard Test Complete!\nPress Enter 3 times to restart.")
            self.set_background_color(QColor(0, 200, 0))  # green
        else:
            # 顯示當前需要按下的按鍵
            self.label.setText(f"Please press: {key_list[self.current_key_index]}\n(Press Esc to skip if unavailable)")
            self.set_background_color("white")

    def set_background_color(self, color):
        """更改背景顏色"""
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

    def get_key_name(self, key):
        """根據按鍵代碼獲取按鍵名稱，主要用於調試輸出"""
        # 反向查找 key_mapping 中的鍵名
        for name, code in key_mapping.items():
            if key == code:
                return name
        # 處理字母和其他可打印字符
        if 32 <= key <= 126:
            return chr(key)
        return f"未知按鍵 ({key})"

    def keyPressEvent(self, event):
        """處理按鍵事件"""
        key = event.key()
        key_name = self.get_key_name(key)
        print(f"按下的鍵: {key_name}")

        # 初次啟動和測試完成後皆需按下 Enter 3 次才能繼續
        if not self.test_started or self.current_key_index >= len(key_list):
            if key == QtCore.Qt.Key_Return or key == QtCore.Qt.Key_Enter:
                self.enter_press_count += 1
                if self.enter_press_count >= 3:
                    # 若為初次啟動，開始測試；若測試完成，重新啟動測試
                    self.test_started = True
                    self.current_key_index = 0
                    self.enter_press_count = 0
                    self.display_current_key()
            else:
                self.enter_press_count = 0  # 若按錯其他鍵則重新計數
            return

        expected_key_name = key_list[self.current_key_index]
        expected_key = key_mapping.get(expected_key_name, None)

        if key == QtCore.Qt.Key_Escape:
            # 按下 Esc 鍵，跳過當前按鍵
            self.current_key_index += 1
            self.display_current_key()
        elif key == expected_key:
            # 按下的鍵與期望的鍵匹配
            self.current_key_index += 1
            self.display_current_key()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = KeyboardTestApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()