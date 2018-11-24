#https://forums.blinkstick.com/t/python-function-for-color-temperature/1068

from math import log

def color_temp(temp):
	temp = temp * 1.0
	if temp < 1:
		temp = 1
	# Algorithm for color temp taken from http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/
	temp = temp / 100
	if temp <= 66:
		r = 255
	else:
		r = temp - 60
		r = 329.698727446 * (r ** -0.1332047592)
		r = min(255, max(0, r))

	if temp < 66:
		g = temp
		g = 99.4708025861 * log(g) - 161.1195681661
		g = min(255, max(0, g))
	else:
		g = temp - 60
		g = 288.1221695283 * (g ** -0.0755148492)
		g = min(255, max(0, g))

	if temp >= 65:
		b = 255
	elif temp < 20:
		b = 0
	else:
		b = temp - 10
		b = 138.5177312231 * log(b) - 305.0447927307
		b = min(255, max(0, b))

	return (r/255, g/255, b/255)