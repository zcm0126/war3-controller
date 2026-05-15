# War3 Controller (Python)

用 Python 控制《魔兽争霸》单位（目前仅支持英雄 WASD 移动）。

## 功能

- WASD 控制英雄前后左右移动（模拟右键点地面）
- F6 开关“控制模式”
- ESC 退出脚本

## 运行

```bash
pip install -r requirements.txt
python src/war3_move_hero_wasd.py
```

## Windowed launch

Start Warcraft III in windowed mode:

```bash
python src/launch_war3_windowed.py
```

If the game cannot be found automatically, pass the executable path:

```bash
python src/launch_war3_windowed.py --exe "D:\Games\Warcraft III\Warcraft III.exe"
```

Or set `WAR3_EXE` first:

```powershell
$env:WAR3_EXE="D:\Games\Warcraft III\Warcraft III.exe"
python src/launch_war3_windowed.py
```
