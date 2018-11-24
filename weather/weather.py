import json
import requests

class Weather:

	def __init__(self, key = "a9a1b6701177be507491fdd6c47e9fb3"):
		self.key = key

	def getData(self, siteID, sensorID, timeStamp):

		requestUrl = 'http://api.openweathermap.org/data/2.5/weather?id=658225&APPID=a9a1b6701177be507491fdd6c47e9fb3'

		response = requests.get(requestUrl)

		res = response.json()

		print(res)

		if response.ok:
			return {
				"temperature": res["main"]["temp"],
				"humidity": res["main"]["humidity"],
				"pressure": res["main"]["pressure"]
			}
		else:
			return None
	
		
	

if __name__ == "__main__":
	

	
	Obj = Weather()

	siteID = "site_exp"
	sensorID = "b1239623-62b1-4a45-bf5a-b8b62056e372"
	timeDate = "2018-01-08T00:58:00.589234Z"

	print(siteID, sensorID, timeDate)

	weather_helsinki = Obj.getData(siteID, sensorID, timeDate)
	print("weather_helsinki: ")
	print(weather_helsinki)

