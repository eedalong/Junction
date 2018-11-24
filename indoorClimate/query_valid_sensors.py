#coding:utf-8
import json
import requests

from indoorClimate import IndoorClimate

key = "zZW3DPNfb23pxs2c19uLb5YKX8AHRRCJ3eOIFQPO"
header = {"x-api-key": key}
siteId = "site_exp"
#deviceType = "MultiSensor" #PrensenceSensor
deviceType = "PresenceSensor"
itemCount = 100
startIndex = 0

requestUrl = "https://v0wwaqqnpa.execute-api.eu-west-1.amazonaws.com/V1/sites/%s/devices?deviceType=%s&itemCount=%d&startIndex=%d" %(siteId, deviceType, itemCount, startIndex)

response = requests.get(requestUrl, headers = header)

res = response.json()

Indoor = IndoorClimate()


timeDateFrom= "2018-11-23T00:58:00.589234Z"
timeDateTo = "2018-11-23T01:58:00.589234Z"

if response.ok:
	n_sensors = len(res["data"]["items"])
	print("n_sensors=%d" %n_sensors)
	for item in res["data"]["items"]:
		sensorId = item["id"]
		indoor_climate = Indoor.getData(siteId, sensorId, timeDateFrom, timeDateTo)
		print(sensorId)
		print(indoor_climate)


else:
	print(res)
