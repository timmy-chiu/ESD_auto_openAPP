import sys
import json
import time
from pathlib import Path
import wmi  # 導入 wmi 模組，用於訪問 Windows 管理工具
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPalette, QColor
from check_battery import check_battery_status


def get_app_dir():
    return Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent


def load_config():
    app_dir = get_app_dir()
    candidates = [
        app_dir / "config.json",
        app_dir.parent / "config.json",
    ]

    for path in candidates:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)

    return {}


config = load_config()


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

        # 新增：目前所有「還在異常中」的項目（設備 + 電池）
        # key 範例： "device:xxxx", "battery"
        self.active_errors = set()
        self.pending_errors = {}
        self.alert_delay_seconds = max(0, float(config.get("device_watcher_alert_delay_seconds", 5)))

        # 創建 WMI 物件和監視器，用於監控設備的創建、刪除和修改事件
        self.c = wmi.WMI()
        self.creation_watcher = self.c.Win32_PnPEntity.watch_for(notification_type="Creation")
        self.deletion_watcher = self.c.Win32_PnPEntity.watch_for(notification_type="Deletion")
        self.modification_watcher = self.c.Win32_PnPEntity.watch_for(notification_type="Modification")

        # 使用定時器每秒檢查設備狀態變化
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_device_status)
        self.timer.start(500)  # 每1秒執行一次檢查
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

    def get_device_key(self, device):
        """
        取得設備的唯一 key，盡量避免重複
        """
        return getattr(device, "PNPDeviceID", None) \
            or getattr(device, "DeviceID", None) \
            or getattr(device, "Name", "Unknown")

    def add_error(self, key, message):
        """
        新增一個異常項目，並切換成紅色背景
        """
        if self.alert_delay_seconds == 0 or key in self.active_errors:
            self.activate_error(key, message)
            return

        first_seen = self.pending_errors.get(key, (time.monotonic(), None))[0]
        self.pending_errors[key] = (first_seen, message)

    def activate_error(self, key, message):
        self.active_errors.add(key)
        self.pending_errors.pop(key, None)
        self.setPalette(self.alert_palette)
        self.label.setText(message)

    def promote_pending_errors(self):
        now = time.monotonic()
        expired = [
            (key, message)
            for key, (first_seen, message) in self.pending_errors.items()
            if now - first_seen >= self.alert_delay_seconds
        ]

        for key, message in expired:
            self.activate_error(key, message)

    def clear_error(self, key, message=None):
        """
        移除某項異常；如果 message 有提供，就顯示「恢復訊息」。
        """
        recovered = False
        self.pending_errors.pop(key, None)

        # 判斷這項是否原本就在異常列表
        if key in self.active_errors:
            self.active_errors.remove(key)
            recovered = True

        # 若有恢復，顯示恢復訊息
        if recovered and message:
            self.label.setText(message)

        # 若所有異常都清光 → 背景恢復
        if not self.active_errors:
            self.reset_background()

    def display_alert(self, message):
        # 顯示紅色背景並顯示訊息
        self.setPalette(self.alert_palette)
        self.label.setText(message)

    def reset_background(self):
        # 恢復到預設背景顏色
        self.setPalette(self.default_palette)
        self.label.setText("監控設備狀態變化...")

    def check_device_status(self):
        self.promote_pending_errors()

        # 檢查設備創建事件
        try:
            new_device = self.creation_watcher(timeout_ms=1)
            if new_device:
                name = new_device.Name
                error_code = new_device.ConfigManagerErrorCode
                error_desc = get_error_description(error_code)
                key = "device:" + self.get_device_key(new_device)

                if error_code != 0:
                    # 新出現就是異常 → 加入異常集合
                    self.add_error(key, f"檢測到新設備：\n{name}\n({error_desc})")
                else:
                    # 新插上的設備是正常的 → 確保不在錯誤集合內
                    self.clear_error(key, f"設備已恢復正常：\n{name}")
        except wmi.x_wmi_timed_out:
            pass
        except Exception as e:
            self.add_error("device:creation", f"創建監視器錯誤：{e}")

        # 檢查設備刪除事件
        try:
            removed_device = self.deletion_watcher(timeout_ms=1)
            if removed_device:
                name = removed_device.Name
                key = "device:" + self.get_device_key(removed_device)

                # 視為異常狀態
                self.add_error(key, f"設備被移除：\n{name}")
        except wmi.x_wmi_timed_out:
            pass
        except Exception as e:
            self.add_error("device:deletion", f"刪除監視器錯誤：{e}")

        # 檢查設備修改事件
        try:
            modified_device = self.modification_watcher(timeout_ms=1)
            if modified_device:
                name = modified_device.Name
                error_code = modified_device.ConfigManagerErrorCode
                error_desc = get_error_description(error_code)
                key = "device:" + self.get_device_key(modified_device)

                if error_code in [10, 22, 43]:
                    # 變成異常 → 加進集合
                    self.add_error(key, f"設備狀態變化：\n{name}\n({error_desc})")
                elif error_code == 0:
                    # 回到正常 → 移出集合，若全部正常會自動變白
                    self.clear_error(key, f"設備已恢復正常：\n{name}")
        except wmi.x_wmi_timed_out:
            pass
        except Exception as e:
            self.add_error("device:modify", f"修改監視器錯誤：{e}")

        # 額外檢查電池狀態
        try:
            battery_status = check_battery_status()
            if battery_status:
                # 取得電池狀態
                is_charging, battery_percent = battery_status

                battery_key = "battery"
                battery_issue = False

                # 狀態為未充電
                if not is_charging:
                    battery_issue = True

                # 電池電量下降
                if self.last_battery_percent is not None and battery_percent < self.last_battery_percent:
                    battery_issue = True
                else:
                    # 若電量沒下降才更新last電量
                    self.last_battery_percent = battery_percent

                if battery_issue:
                    self.add_error(battery_key, "Battery not charging")
                else:
                    self.clear_error(battery_key, "Battery status recovered")
        except Exception as e:
            print(f"檢查電池狀態失敗: {e}")


def main():
    app = QApplication(sys.argv)
    window = DeviceMonitorWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
