import cv2
import numpy as np

# 設定影片參數
width, height = 300, 600  # 解析度
fps = 1  # 每秒一幀
duration_minutes = 10  # 總計時分鐘數

# 計算總幀數
total_frames = duration_minutes * 60

# 建立影片寫入器
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('countdown_timer.mp4', fourcc, fps, (width, height))

# 產生計時畫面
for seconds in range(total_frames):
    # 計算當前時間 (分:秒)
    minutes = seconds // 60
    sec = seconds % 60
    time_str = f"{minutes:02}:{sec:02}"

    # 建立白底影像
    frame = np.ones((height, width, 3), dtype=np.uint8) * 255

    # 加入黑色文字
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 3
    thickness = 5
    text_size = cv2.getTextSize(time_str, font, font_scale, thickness)[0]
    text_x = (width - text_size[0]) // 2
    text_y = (height + text_size[1]) // 2
    cv2.putText(frame, time_str, (text_x, text_y), font, font_scale, (0, 0, 0), thickness)

    # 寫入影格
    out.write(frame)

# 釋放影片寫入器
out.release()
print("影片生成完成")
