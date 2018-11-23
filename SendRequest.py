import requests
import json
import logging

API = {"IntensitySet": "/sites/{siteId}/devices/{deviceId}/level",
       "ColorSet": "/sites/{siteId}/devices/{deviceId}/color"}


class SendRequest:
    def __init__(self, url):
        self.url = url

    def setLightIntensity(self, siteID, deviceID, level):
        data = {"level": level}
        response = requests.put(url=self.url + API["IntensitySet"].format(siteId=siteID, deviceId=deviceID),
                                json=json.dumps(data))
        if response.ok:
            content = response.json()
            print("set level successfully  = {}".format(content))
        else:
            content = response.json()
            print("set level failed  = {}".format(content))

    def setLightColor(self,siteID,deviceID,color):
        data = {"color": color}
        response = requests.put(url=self.url + API["ColorSet"].format(siteId=siteID, deviceId=deviceID),
                                json=json.dumps(data))
        if response.ok:
            content = response.json()
            print("set color successfully  = {}".format(content))
        else:
            content = response.json()
            print("set color failed  = {}".format(content))

