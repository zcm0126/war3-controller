import time
import pyautogui
from pynput import keyboard

# 每次移动“迈”多远（像素）
MOVE_STEP = 150  # 可以根据你屏幕和感觉调：100/150/200

# 节流，防止按住一次触发太多次
MIN_INTERVAL = 0.12  # 每次触发之间至少 0.12 秒
last_trigger_time = 0


def move_hero(direction: str):
    """根据方向，在屏幕中间附近点右键，让英雄往该方向走"""
    global last_trigger_time

    now = time.time()
    if now - last_trigger_time < MIN_INTERVAL:
        return  # 离上次太近就丢掉，防止疯狂触发
    last_trigger_time = now

    screen_width, screen_height = pyautogui.size()
    cx, cy = screen_width // 2, screen_height // 2  # 屏幕中心

    if direction == "up":
        tx, ty = cx, cy - MOVE_STEP
    elif direction == "down":
        tx, ty = cx, cy + MOVE_STEP
    elif direction == "left":
        tx, ty = cx - MOVE_STEP, cy
    elif direction == "right":
        tx, ty = cx + MOVE_STEP, cy
    else:
        return

    # 记录原鼠标位置
    old_x, old_y = pyautogui.position()

    # 移动过去 → 右键 → 再移回原位
    pyautogui.moveTo(tx, ty, duration=0)           # duration=0 = 瞬移
    pyautogui.click(button="right")                # 右键一下，等于“往那边走”
    time.sleep(0.03)
    pyautogui.moveTo(old_x, old_y, duration=0)


def on_press(key):
    try:
        k = key.char.lower()  # 普通字母键
    except AttributeError:
        return

    if k == "w":
        move_hero("up")
    elif k == "s":
        move_hero("down")
    elif k == "a":
        move_hero("left")
    elif k == "d":
        move_hero("right")


def on_release(key):
    # 按 ESC 退出脚本
    if key == keyboard.Key.esc:
        print("收到 ESC，退出脚本。")
        return False


if __name__ == "__main__":
    print("脚本已启动：在游戏中按 W/A/S/D 让英雄移动，按 ESC 退出脚本。")

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
