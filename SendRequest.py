import requests
import json
import logging

API = {"IntensitySet": "/sites/{siteId}/devices/{deviceId}/level",
       "ColorSet": "/sites/{siteId}/devices/{deviceId}/color"}


class SendRequest:
    def __init__(self, url,apiKey =  "zZW3DPNfb23pxs2c19uLb5YKX8AHRRCJ3eOIFQPO"):
        self.url = url
        self.apiKey = apiKey
    def setLightIntensity(self, siteID, deviceID, level):
        data = {"level": level}
        header = {"x-api-key": self.apiKey}
        response = requests.put(url=self.url + API["IntensitySet"].format(siteId=siteID, deviceId=deviceID),
                                headers = header, json=json.dumps(data))
        if response.ok:
            content = response.json()
            print("set level successfully  = {}".format(content))
        else:
            content = response.json()
            print("set level failed  = {}".format(content))

    def setLightColor(self,siteID,deviceID,color):
        data = {"color": color}
        header = {"x-api-key": self.apiKey}
        response = requests.put(url=self.url + API["ColorSet"].format(siteId=siteID, deviceId=deviceID),
                                headers = header,json=json.dumps(data))
        if response.ok:
            content = response.json()
            print("set color successfully  = {}".format(content))
        else:
            content = response.json()
            print("set color failed  = {}".format(content))

