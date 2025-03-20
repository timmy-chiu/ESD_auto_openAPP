import time

import psutil

def check_battery_status():
    battery = psutil.sensors_battery()
    if battery is None:
        print("無法獲取電池資訊，可能是桌機或沒有安裝感測器。")
        return

    percent = battery.percent
    charging = battery.power_plugged

    print(f"電池電量: {percent}%")
    if charging:
        print("筆電正在充電中🔌")
    else:
        print("筆電未充電🔋")

if __name__ == "__main__":
    while True:
        check_battery_status()
        time.sleep(5)
