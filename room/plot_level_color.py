import matplotlib.pyplot as plt
from collections import deque
import time


def updateLevel(fname = 'level.txt'):
    level = 100
    try:
        level = int(open(fname, 'r').read().strip())
    except Exception as e:
        print(e)
    if level > 100:
        level = 100
    if level < 0:
        level = 0
    return level


def updateColor(fname = 'color.txt'):
    color = 2000
    try:
        color = int(open(fname, 'r').read().strip())
    except Exception as e:
        print(e)
    if color > 9000:
        color = 9000
    if color < 2000:
        color = 2000
    return color


fig = plt.figure()

ax_color = fig.add_subplot(2, 1, 1)
ax_level = fig.add_subplot(2, 1, 2)
#ax1 = fig.add_subplot(1, 3, 2, projection='3d')
#ax2 = fig.add_subplot(1, 3, 3)

LEN = 100

level_data = deque([0] * LEN)
level_min = 0
level_max = 100
color_data = deque([2000] * LEN)
color_min = 1000
color_max = 10000

while True:

	level = updateLevel()
	color = updateColor()

	print('color = %d, level = %d' %(color, level))

	level_data.popleft()
	level_data.append(level)

	color_data.popleft()
	color_data.append(color)


	ax_color.clear()
	ax_color.set_ylim([color_min, color_max])
	ax_color.plot(color_data, 'r')
	ax_color.set_ylabel('color')
	
	ax_level.clear()
	ax_level.set_ylim([level_min, level_max])
	ax_level.plot(level_data, 'b')
	ax_level.set_ylabel('level')

	plt.title('Light Control Signal (color, level)')
	plt.draw() 	
	plt.pause(0.1)
	time.sleep(0.5)


