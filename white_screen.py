import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt


class WhiteScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("White Background Window")

        # 設定純白背景
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255))
        self.setPalette(palette)

        # 保留視窗邊框（才能最大化）
        self.setWindowFlag(Qt.FramelessWindowHint, False)

        # 設定大小和位置
        screen = QApplication.primaryScreen()
        rect = screen.availableGeometry()   # 可用工作區（扣除工作列）

        self.setGeometry(rect.x(), rect.y(), rect.width(), rect.height())

        # 自動最大化
        self.showMaximized()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WhiteScreen()
    sys.exit(app.exec_())
