import json
import requests

class Occupancy:

	def __init__(self, key = "zZW3DPNfb23pxs2c19uLb5YKX8AHRRCJ3eOIFQPO"):
		self.key = key

	def getData(self, siteID, sensorID, timeDateFrom, timeDateTo = None):
		key = self.key

		header = {"x-api-key": key}

		if timeDateTo == None: #处理有1个日期时间参数，还是有2个日期时间参数
			body = test_data = {"timeDate": timeDateFrom}

			requestUrl = 'https://v0wwaqqnpa.execute-api.eu-west-1.amazonaws.com/V1/sites/%s/sensors/%s/occupancy' %(siteID, sensorID)

			response = requests.post(requestUrl, headers = header,json = json.dumps(body))

			res = response.json()

			print(res)

			if response.ok:
				return res["data"]["occupied"]
			else:
				return None
		else:
			body = test_data = {"timeDate": timeDateFrom, "timeDateTo": timeDateTo}
			
			requestUrl = 'https://v0wwaqqnpa.execute-api.eu-west-1.amazonaws.com/V1/sites/%s/sensors/%s/occupancy/measure' %(siteID, sensorID)

			response = requests.post(requestUrl, headers = header,json = json.dumps(body))

			res = response.json()

			print(res)

			if response.ok:
				return True if res["data"]["measure"] > 0 else False
			else:
				return None
	
		
	

if __name__ == "__main__":
	
	key = "zZW3DPNfb23pxs2c19uLb5YKX8AHRRCJ3eOIFQPO"
	
	Obj = Occupancy(key)

	siteID = "site_exp"
	sensorID = "b1239623-62b1-4a45-bf5a-b8b62056e372"
	timeDate = "2018-01-08T00:58:00.589234Z"

	print(siteID, sensorID, timeDate)

	bool_occupancy = Obj.getData(siteID, sensorID, timeDate)
	print("bool_occupancy: ")
	print(bool_occupancy)




		

		

