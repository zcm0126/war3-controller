"""
War3Controller: 用于控制《魔兽争霸》单位 / 英雄的基础执行层。

当前只实现：
- 相对于屏幕中心的方向移动（前后左右、斜向）
- 底层是：通过 pyautogui 模拟鼠标右键点击地面

后续可以在这个类里继续加：
- attack_move()
- select_group()
- cast_spell()
- 等等
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Tuple, Literal, Optional

import pyautogui


Direction = Literal[
    "up",
    "down",
    "left",
    "right",
    "up_left",
    "up_right",
    "down_left",
    "down_right",
]


@dataclass
class War3ControllerConfig:
    """控制参数配置，可根据机器和手感调整。"""
    move_step: int = 120          # 每次移动“迈”多远（像素）
    click_delay: float = 0.03     # 右键和恢复鼠标之间的停顿（秒）
    use_screen_center: bool = True  # 暂时固定以屏幕中心为参考点


class War3Controller:
    """Warcraft III 控制执行层（当前只实现移动）。"""

    def __init__(self, config: Optional[War3ControllerConfig] = None) -> None:
        self.config = config or War3ControllerConfig()

    # -----------------------
    # 对外暴露的移动接口
    # -----------------------
    def move(self, direction: Direction) -> None:
        """
        让英雄朝某个方向移动一步。

        原理：以屏幕中心为参考点，在对应方向偏移一定距离，右键一下。
        注意：假设游戏窗口当前激活，且英雄大致在屏幕中心附近。
        """
        target_x, target_y = self._compute_target_point(direction)
        self._right_click_at(target_x, target_y)

    def move_up(self) -> None:
        self.move("up")

    def move_down(self) -> None:
        self.move("down")

    def move_left(self) -> None:
        self.move("left")

    def move_right(self) -> None:
        self.move("right")

    def move_up_left(self) -> None:
        self.move("up_left")

    def move_up_right(self) -> None:
        self.move("up_right")

    def move_down_left(self) -> None:
        self.move("down_left")

    def move_down_right(self) -> None:
        self.move("down_right")

    # -----------------------
    # 内部工具函数
    # -----------------------
    def _get_reference_point(self) -> Tuple[int, int]:
        """
        获取移动参考点坐标。

        当前实现：屏幕中心。
        后续可以改成：
        - 游戏窗口中心
        - 识别到的英雄坐标（视觉识别后）
        """
        width, height = pyautogui.size()
        return width // 2, height // 2

    def _compute_target_point(self, direction: Direction) -> Tuple[int, int]:
        cx, cy = self._get_reference_point()
        step = self.config.move_step

        dx = 0
        dy = 0

        if "up" in direction:
            dy -= 1
        if "down" in direction:
            dy += 1
        if "left" in direction:
            dx -= 1
        if "right" in direction:
            dx += 1

        # 无方向或者 dx=dy=0 的情况避免除零，直接返回中心（相当于不动）
        if dx == 0 and dy == 0:
            return cx, cy

        # 简单的 8 向离散，不做长度归一，直接 step * dx/dy
        tx = cx + dx * step
        ty = cy + dy * step
        return int(tx), int(ty)

    def _right_click_at(self, x: int, y: int) -> None:
        """
        在指定屏幕坐标模拟一次右键点击。
        为了不干扰玩家操作：点击前后会恢复鼠标原位置。
        """
        # 记录原鼠标位置
        old_x, old_y = pyautogui.position()

        # 移过去 → 右键 → 再移回来
        pyautogui.moveTo(x, y, duration=0)
        pyautogui.click(button="right")
        time.sleep(self.config.click_delay)
        pyautogui.moveTo(old_x, old_y, duration=0)
