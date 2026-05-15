import pydirectinput
import time

SELECT_GROUP_MODIFIER = "ctrl"
SELECT_GROUP_KEY = "1"
MOVE_TARGET = (800, 500)
ABILITY_KEY = "q"
ABILITY_TARGET = (500, 500)

time.sleep(3)

pydirectinput.keyDown(SELECT_GROUP_MODIFIER)
pydirectinput.press(SELECT_GROUP_KEY)
pydirectinput.keyUp(SELECT_GROUP_MODIFIER)
time.sleep(0.2)

pydirectinput.rightClick(*MOVE_TARGET)
time.sleep(0.2)

pydirectinput.press(ABILITY_KEY)
time.sleep(0.2)

pydirectinput.click(*ABILITY_TARGET)
