import requests
import json
import Configs
API = {

    "IntensitySet": "/V1/sites/{siteId}/devices/{deviceId}/level",
    "ColorSet": "/V1/sites/{siteId}/devices/{deviceId}/color"

    }
DUMMY_API = {

    "IntensitySet": "/V1/sites/{siteId}/devices/{deviceId}/level/{level}",
    "ColorSet": "/V1/sites/{siteId}/devices/{deviceId}/color/{color}"

    }
class SendRequest:
    def __init__(self, url,apiKey =  "zZW3DPNfb23pxs2c19uLb5YKX8AHRRCJ3eOIFQPO"):
        self.url = url
        self.apiKey = apiKey
    def setLightIntensity(self, siteID, deviceID, level):
        level = int(level)
        #Configs.logger.debug("check light level = {}".format(int(level)))
        data = {"level": int(level)}
        header = {"x-api-key": self.apiKey}
        #Configs.logger.debug("check body = {}".format(data))
        response = ""
        if Configs.DUMMY:
            response = requests.post(url=self.url + DUMMY_API["IntensitySet"].format(siteId=siteID, deviceId=deviceID,level = level),
                                     data = {})
        else:
            response = requests.put(url=self.url + API["IntensitySet"].format(siteId=siteID, deviceId=deviceID),
                                headers = header, json=data)
        print(response)
        if response.ok:

            content = response.json()
            print("set level successfully  = {}".format(content))
        else:


            print("set level failed ")

    def setLightColor(self,siteID,deviceID,color):
        color = int(color)
        data = {"color": int(color)}
        Configs.logger.debug("check light color = {}".format(int(color)))
        header = {"x-api-key": self.apiKey}
        response = ""
        if Configs.DUMMY:
            response = requests.post(
                url=self.url + DUMMY_API["ColorSet"].format(siteId=siteID, deviceId=deviceID, color=color),
                data={})
        else:
            response = requests.put(url=self.url + API["ColorSet"].format(siteId=siteID, deviceId=deviceID),
                                     headers=header, json=data)
        if response.ok:
            content = response.json()
            print("set color successfully  = {}".format(content))
        else:

            print("set color failed ")

