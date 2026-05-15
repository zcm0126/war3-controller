# War3 Voice Controller

用语音控制《魔兽争霸 III》英雄移动。

## Install

```powershell
uv venv
uv pip install -r requirements.txt
```

## Run

```powershell
.venv\Scripts\python src\run_voice_control.py
```

支持命令：

```text
英雄向前
英雄向后
英雄向左
英雄向右
```

## Launch Warcraft III Windowed

```powershell
.venv\Scripts\python src\launch_war3_windowed.py
```

也可以指定游戏路径：

```powershell
.venv\Scripts\python src\launch_war3_windowed.py --exe "D:\Games\Warcraft III\Warcraft III.exe"
```

或使用批处理：

```powershell
.\start_war3_windowed.bat
```
