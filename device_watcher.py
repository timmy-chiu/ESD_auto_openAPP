import sys
import wmi  # 導入 wmi 模組，用於訪問 Windows 管理工具
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPalette, QColor
from check_battery import check_battery_status


def get_error_description(error_code):
    error_descriptions = {
        0: "設備正常運行。",
        1: "該設備未被正確配置。",
        10: "該設備無法啟動。",
        22: "該設備已被禁用。",
        43: "Windows 已經停止此設備，因為它報告了問題。",
    }
    return error_descriptions.get(error_code, "未知錯誤")

# 主視窗類
class DeviceMonitorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

        # 創建 WMI 物件和監視器，用於監控設備的創建、刪除和修改事件
        self.c = wmi.WMI()
        self.creation_watcher = self.c.Win32_PnPEntity.watch_for(notification_type="Creation")
        self.deletion_watcher = self.c.Win32_PnPEntity.watch_for(notification_type="Deletion")
        self.modification_watcher = self.c.Win32_PnPEntity.watch_for(notification_type="Modification")

        # 使用定時器每秒檢查設備狀態變化
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_device_status)
        self.timer.start(3000)  # 每1秒執行一次檢查
        self.last_battery_percent = None

    def init_ui(self):
        # 設置視窗標題和大小
        self.setWindowTitle("device watcher")
        self.setGeometry(100, 100, 400, 200)

        # 設置背景顏色
        self.default_palette = self.palette()
        self.alert_palette = self.palette()
        self.alert_palette.setColor(QPalette.Window, QColor(220, 0, 0))

        # 設置設備訊息標籤
        self.label = QLabel("監控設備狀態變化...", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)  # 啟用文字自動換行
        font = self.label.font()
        font.setPointSize(20)
        self.label.setFont(font)


        # 設置佈局
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def display_alert(self, message):
        # 顯示紅色背景並顯示訊息
        self.setPalette(self.alert_palette)
        self.label.setText(message)
        # 在5秒後恢復背景顏色
        # QTimer.singleShot(5000, self.reset_background)

    def reset_background(self):
        # 恢復到預設背景顏色
        self.setPalette(self.default_palette)
        self.label.setText("監控設備狀態變化...")

    def check_device_status(self):
        # 檢查設備創建事件
        try:
            new_device = self.creation_watcher(timeout_ms=1)  # 設置超時為1000毫秒
            if new_device:
                name = new_device.Name
                error_code = new_device.ConfigManagerErrorCode
                error_desc = get_error_description(error_code)
                self.display_alert(f"檢測到新設備： \n{name} \n({error_desc})")
        except wmi.x_wmi_timed_out:
            pass  # 超時則忽略
        except Exception as e:
            self.display_alert(f"創建監視器錯誤：{e}")

        # 檢查設備刪除事件
        try:
            removed_device = self.deletion_watcher(timeout_ms=1)
            if removed_device:
                name = removed_device.Name
                self.display_alert(f"設備被移除： \n{name}")
        except wmi.x_wmi_timed_out:
            pass  # 超時則忽略
        except Exception as e:
            self.display_alert(f"刪除監視器錯誤：{e}")

        # 檢查設備修改事件
        try:
            modified_device = self.modification_watcher(timeout_ms=1)
            if modified_device:
                name = modified_device.Name
                error_code = modified_device.ConfigManagerErrorCode
                error_desc = get_error_description(error_code)
                self.display_alert(f"設備狀態變化： \n{name} \n({error_desc})")
        except wmi.x_wmi_timed_out:
            pass  # 超時則忽略
        except Exception as e:
            self.display_alert(f"修改監視器錯誤：{e}")

        # 額外檢查電池狀態
        try:
            battery_status = check_battery_status()
            if battery_status:
                # 取得電池狀態
                is_charging, battery_percent = battery_status

                # 狀態為未充電
                if not is_charging:
                    self.display_alert("Battery not charging")

                # 電池電量下降
                if self.last_battery_percent is not None and battery_percent < self.last_battery_percent:
                    self.display_alert("Battery not charging")

                self.last_battery_percent = battery_percent
        except Exception as e:
            print(f"檢查電池狀態失敗: {e}")


def main():
    app = QApplication(sys.argv)
    window = DeviceMonitorWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
