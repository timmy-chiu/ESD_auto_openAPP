import pygame
import sys
import pygetwindow as gw
import time

def paint():
    # 初始化 Pygame
    pygame.init()

    # 設定可調整大小的視窗
    screen_width, screen_height = 800, 600  # 初始視窗大小
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Touch Test")

    # 定義顏色
    WHITE = (255, 255, 255)

    # 定義一組顏色，繪製線條時會循環使用
    colors = [
        (0, 255, 0),     # 綠色
        (255, 0, 0),     # 紅色
    ]
    color_index = 0  # 當前顏色的索引
    current_color = colors[color_index]  # 當前繪製顏色

    # 填充背景為白色
    screen.fill(WHITE)
    pygame.display.flip()

    # 初始化變數
    drawing = False
    last_pos = None
    fullscreen = False  # 全螢幕模式的狀態

    # 設定計時器，初始化為當前時間（毫秒）
    last_event_time = pygame.time.get_ticks()

    # 創建時鐘物件，用於控制更新頻率
    clock = pygame.time.Clock()

    # 主迴圈
    while True:
        current_time = pygame.time.get_ticks()  # 獲取當前時間（毫秒）

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # 開始繪製
            elif event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                last_pos = event.pos
                last_event_time = current_time  # 重置計時器

            # 停止繪製，並切換顏色
            elif event.type == pygame.MOUSEBUTTONUP:
                drawing = False
                last_pos = None
                last_event_time = current_time  # 重置計時器
                current_color = colors[1]

            # 繪製線條
            elif event.type == pygame.MOUSEMOTION:
                if drawing:
                    current_pos = event.pos
                    if last_pos is not None:
                        pygame.draw.line(screen, current_color, last_pos, current_pos, 7)
                    last_pos = current_pos
                    last_event_time = current_time  # 重置計時器

            # 按下 ESC 鍵退出
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    window = gw.getWindowsWithTitle('touch')
                    if window:
                        window[0].minimize()

            # 視窗大小調整事件
            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.size  # 更新視窗大小
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                screen.fill(WHITE)  # 調整大小後重置背景

        # 如果超過10秒沒有滑鼠事件，重置畫面為全白
        if current_time - last_event_time > 3000:
            screen.fill(WHITE)
            pygame.display.flip()
            last_event_time = current_time  # 重置計時器
            color_index = 0
            current_color = colors[color_index]  # 重置繪製顏色

        # 更新顯示
        pygame.display.update()

        # 控制更新頻率（60幀）
        clock.tick(60)

# 若是此程式為主程式，則執行 main 函數
if __name__ == "__main__":
    paint()
