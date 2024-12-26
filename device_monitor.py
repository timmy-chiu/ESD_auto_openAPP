import wmi
import time

def get_device_status():
    # 創建 WMI 對象，用於訪問系統資訊
    c = wmi.WMI()
    # 獲取所有即插即用設備的資訊
    devices = c.Win32_PnPEntity()
    device_status = {}
    for device in devices:
        device_id = device.PNPDeviceID  # 設備的唯一識別碼
        name = device.Name  # 設備名稱
        error_code = device.ConfigManagerErrorCode  # 設備的錯誤代碼
        status = device.Status  # 設備狀態
        # 將設備資訊存入字典
        device_status[device_id] = {
            'name': name,
            'error_code': error_code,
            'status': status
        }
    return device_status

def get_error_description(error_code):
    # 定義錯誤代碼對應的描述
    error_descriptions = {
        0: "設備正常運行。",
        1: "該設備未被正確配置。",
        10: "該設備無法啟動。",
        22: "該設備已被禁用。",
        43: "Windows 已經停止此設備，因為它報告了問題。",
        # 可以根據需要添加其他錯誤代碼和描述
    }
    return error_descriptions.get(error_code, "未知錯誤")

def main():
    # 獲取初始的設備狀態
    prev_status = get_device_status()
    print("開始監控設備狀態...")
    while True:
        time.sleep(1)  # 每秒檢測一次
        # 獲取當前的設備狀態
        current_status = get_device_status()
        # 檢查設備是否有變化
        for device_id in current_status:
            if device_id not in prev_status:
                # 如果檢測到新設備
                print(f"檢測到新設備：{current_status[device_id]['name']} (ID: {device_id})")
            else:
                prev_error = prev_status[device_id]['error_code']
                curr_error = current_status[device_id]['error_code']
                if prev_error != curr_error:
                    if curr_error != 0:
                        # 如果設備出現錯誤
                        error_desc = get_error_description(curr_error)
                        print(f"設備出現異常：{current_status[device_id]['name']} (ID: {device_id}) 錯誤代碼：{curr_error} ({error_desc})")
                    else:
                        # 如果設備恢復正常
                        print(f"設備恢復正常：{current_status[device_id]['name']} (ID: {device_id})")
        # 檢查設備是否被移除
        for device_id in prev_status:
            if device_id not in current_status:
                # 如果設備被移除
                print(f"設備被移除：{prev_status[device_id]['name']} (ID: {device_id})")
        # 更新上一輪的設備狀態
        prev_status = current_status


if __name__ == "__main__":
    main()
