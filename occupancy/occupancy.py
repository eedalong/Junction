import json
import requests

class Occupancy:

	def __init__(self, key = "zZW3DPNfb23pxs2c19uLb5YKX8AHRRCJ3eOIFQPO"):
		self.key = key

	def getData(self, siteID, sensorID, timeStamp):
		key = self.key

		header = {"x-api-key": key}
		body = test_data = {"timeDate": timeStamp}

		requestUrl = 'https://v0wwaqqnpa.execute-api.eu-west-1.amazonaws.com/V1/sites/%s/sensors/%s/occupancy' %(siteID, sensorID)

		response = requests.post(requestUrl, headers = header,json = json.dumps(body))

		res = response.json()

		print(res)

		if response.ok:
			return res["data"]["occupied"]
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









		#requestUrl = '/sites/{siteId}/sensors/{sensorId}/indoorclimate'
		# siteID = "site_exp"
		# sensorID = "b1239623-62b1-4a45-bf5a-b8b62056e372"
		# timeStamp = "2018-01-08T00:58:00.589234Z"
		# requestUrl = 'https://v0wwaqqnpa.execute-api.eu-west-1.amazonaws.com/V1/sites/%s/sensors/%s/indoorclimate' %(siteID, sensorID)

		# POST/sites/{siteId}/sensors/{sensorId}/occupancy

		

		

		#req = urllib2.Request(url = requrl,data =test_data_urlencode)
		#print req

		# res_data = urllib2.urlopen(req)
		# res = res_data.read()

		

		# #conn = httplib.HTTPConnection("https://v0wwaqqnpa.execute-api.eu-west-1.amazonaws.com")
		# conn = httplib.HTTPConnection("52.84.35.18")

		# siteID = "site_exp"
		# sensorID = "b1239623-62b1-4a45-bf5a-b8b62056e372"
		# timeStamp = "2018-01-08T00:58:00.589234Z"
		# requestUrl = 'https://v0wwaqqnpa.execute-api.eu-west-1.amazonaws.com/V1/sites/%s/sensors/%s/indoorclimate' %(siteID, sensorID)
		# requrl = requestUrl

		# test_data = {"timeDate": timeStamp}
		# test_data_urlencode = urllib.urlencode(test_data)

		# headerdata = {"x-api-key":"zZW3DPNfb23pxs2c19uLb5YKX8AHRRCJ3eOIFQPO", "accept":"application/json", "Content-Type": "application/json"}

		# conn.request(method="POST",url=requrl,body=test_data_urlencode,headers = headerdata) 

		# response = conn.getresponse()

		# res= response.read()

		# print res



		

		

