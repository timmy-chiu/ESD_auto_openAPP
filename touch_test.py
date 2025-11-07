import time
import pygame
import sys
import pygetwindow as gw


def paint():
    pygame.init()

    # 取得當前螢幕解析度
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h

    # 無邊框 + 全螢幕
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
    pygame.display.set_caption("Touch Test")

    time.sleep(1)
    window = gw.getWindowsWithTitle('Touch Test')
    if window:
        window[0].minimize()

    WHITE = (255, 255, 255)
    GREEN = (0, 200, 0)
    RED = (255, 0, 0)

    colors = [GREEN, RED]
    current_color = colors[0]

    screen.fill(WHITE)
    pygame.display.flip()

    drawing = False
    last_pos = None
    test_done = False

    clock = pygame.time.Clock()

    # 滑鼠測試狀態變數
    left_clicked = False
    right_clicked = False
    mouse_moved = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # === 鍵盤操作 ===
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKQUOTE:
                    print("ESC：最小化")
                    # 重置所有狀態
                    drawing = False
                    last_pos = None
                    test_done = False
                    left_clicked = right_clicked = mouse_moved = False
                    print(mouse_moved)
                    screen.fill(WHITE)
                    pygame.display.flip()
                    current_color = colors[0]
                    window = gw.getWindowsWithTitle('Touch Test')
                    if window:
                        window[0].minimize()

            # 滑鼠按下
            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                last_pos = event.pos
                if event.button == 1 and not left_clicked:
                    left_clicked = True
                    print("偵測到左鍵點擊")
                elif event.button == 3 and not right_clicked:
                    right_clicked = True
                    print("偵測到右鍵點擊")
            # 滑鼠釋放
            elif event.type == pygame.MOUSEBUTTONUP:
                drawing = False
                last_pos = None
                current_color = colors[1]
            # 滑鼠移動
            elif event.type == pygame.MOUSEMOTION:
                if not mouse_moved:
                    mouse_moved = True
                    print("偵測到滑鼠移動")
                if drawing:
                    current_pos = event.pos
                    if last_pos:
                        pygame.draw.line(screen, current_color, last_pos, current_pos, 7)
                    last_pos = current_pos

            # 判斷滑鼠測試是否成功
            if left_clicked and right_clicked and mouse_moved and not test_done:
                test_done = True
                print("三項動作已完成，變更背景為綠色")
                screen.fill(GREEN)
                pygame.display.flip()

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    paint()