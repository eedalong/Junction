import json
import requests

class IndoorClimate:

	def __init__(self, key = "zZW3DPNfb23pxs2c19uLb5YKX8AHRRCJ3eOIFQPO"):
		self.key = key

	def getData(self, siteID, sensorID, timeDateFrom, timeDateTo):
		key = self.key

		header = {"x-api-key": key}
		body = test_data = {"timeDateFrom": timeDateFrom, "timeDateTo": timeDateTo}

		requestUrl = 'https://v0wwaqqnpa.execute-api.eu-west-1.amazonaws.com/V1/sites/%s/sensors/%s/indoorclimate' %(siteID, sensorID)

		response = requests.post(requestUrl, headers = header,json = json.dumps(body))

		res = response.json()

		print(res)
		
		if response.ok:
			return {
				"temperature": res["data"]["indoorClimate"][0]["temperature"],
				"humidity": res["data"]["indoorClimate"][0]["humidity"],
				"co2": res["data"]["indoorClimate"][0]["co2"]
			}
		else:
			return None
	
		
	

if __name__ == "__main__":
	
	key = "zZW3DPNfb23pxs2c19uLb5YKX8AHRRCJ3eOIFQPO"
	
	Obj = IndoorClimate(key)

	siteID = "site_exp"
	sensorID = "b1239623-62b1-4a45-bf5a-b8b62056e372"
	timeDateFrom= "2018-01-08T00:58:00.589234Z"
	timeDateTo = "2018-01-08T01:58:00.589234Z"

	print(siteID, sensorID, timeDateFrom, timeDateTo)

	indoor_climate = Obj.getData(siteID, sensorID, timeDateFrom, timeDateTo)
	print("indoor_climate: ")
	print(indoor_climate)
