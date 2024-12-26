import subprocess
import time
import pygetwindow as gw

# 使用 subprocess 啟動 paint.exe
# subprocess.Popen(["dist/paint.exe"])  # 確保路徑正確
#
# time.sleep(7)

window = gw.getWindowsWithTitle('touch test')
print(window)
if window:
    window[0].maximize()  # 將小畫家視窗最大化
