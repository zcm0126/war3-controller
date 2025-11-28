"""
简单示例：使用 War3Controller + pynput，实现 WASD 控制英雄移动。

快捷键说明：
- F6: 开/关 控制模式（打开后 WASD 才会控制英雄）
- W/A/S/D: 在控制模式开启时，让英雄前后左右/斜向移动
- Esc: 退出脚本
"""

import threading
import time
from typing import Set

from pynput import keyboard

from war3_controller import War3Controller, War3ControllerConfig


MOVE_STEP = 120
STEP_INTERVAL = 0.10  # 连续移动间隔（秒）


movement_keys: Set[str] = set()
control_enabled = False
running = True

controller = War3Controller(
    War3ControllerConfig(
        move_step=MOVE_STEP,
        click_delay=0.03,
    )
)


def movement_loop() -> None:
    """后台循环，根据当前按键状态持续移动英雄。"""
    global running

    while running:
        if control_enabled and movement_keys:
            # 计算方向
            up = "w" in movement_keys
            down = "s" in movement_keys
            left = "a" in movement_keys
            right = "d" in movement_keys

            direction = None

            if up and not down and not left and not right:
                direction = "up"
            elif down and not up and not left and not right:
                direction = "down"
            elif left and not right and not up and not down:
                direction = "left"
            elif right and not left and not up and not down:
                direction = "right"
            elif up and left:
                direction = "up_left"
            elif up and right:
                direction = "up_right"
            elif down and left:
                direction = "down_left"
            elif down and right:
                direction = "down_right"

            if direction:
                controller.move(direction)  # 核心调用

        time.sleep(STEP_INTERVAL)


def on_press(key) -> None:
    global control_enabled, running

    try:
        k = key.char.lower()
    except AttributeError:
        k = None

    if k in ("w", "a", "s", "d"):
        movement_keys.add(k)

    if key == keyboard.Key.f6:
        control_enabled = not control_enabled
        print(f"[INFO] 控制模式: {'开启' if control_enabled else '关闭'}")

    if key == keyboard.Key.esc:
        print("[INFO] 收到 ESC，准备退出脚本...")
        running = False
        return False  # 停止监听


def on_release(key) -> None:
    try:
        k = key.char.lower()
    except AttributeError:
        k = None

    if k in movement_keys:
        movement_keys.discard(k)


if __name__ == "__main__":
    print("WASD Demo 启动：")
    print("- F6: 开/关 WASD 控制模式")
    print("- 控制模式开启时，W/A/S/D = 英雄前后左右/斜向移动")
    print("- Esc: 退出脚本")

    t = threading.Thread(target=movement_loop, daemon=True)
    t.start()

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    print("脚本已退出。")
