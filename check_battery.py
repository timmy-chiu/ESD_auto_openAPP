import time
import psutil


def check_battery_status():
    battery = psutil.sensors_battery()
    if battery is None:
        print("無法獲取電池資訊，可能是桌機或沒有安裝感測器。")
        return

    battery_percent = battery.percent
    charging = battery.power_plugged

    if charging:
        is_charging = True
    else:
        is_charging = False

    return is_charging, battery_percent


if __name__ == "__main__":
    while True:
        is_charging, battery_percent = check_battery_status()
        if is_charging is False:
            print("電池未充電")
        time.sleep(1)
