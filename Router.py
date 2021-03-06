import time
import numpy as np
import Configs
class Router:
    def __init__(self):
        # record the history user status and light status
        self.userStatus = {
            # FocusOffDesk contains 2 main situation: sleep on the desk or the user's focus is not on the testkable
            # this mode is set to save the energy
            "FocusOffWork": 0,

            "Tired": 0,
            # if the user is focusing on work, then just keep the setting of the light
            # if the user is once detected in focusing status, light status should be caution to change
            "FocusOnWork": 0,
            # feel bad
            "FeelBad": 0,
            # feel good
            "FeelGood": 0,
            # if the user once set the light value, the setted value should not be changed for a while
        }
        self.tiredThd = 0.25
        self.faceThd = 0.4
        self.co2Thd = 600


    def getStatus(self):
        saved_status = "FocusOnWork"
        saved_value = 0
        for key in self.userStatus:
            if self.userStatus[key] > saved_value:
                saved_value = self.userStatus[key]
                saved_status = key
        return saved_status

    def Route(self, dataCollection):

        # we determine each status according to the environment data
        dataCollection["Occupancy"] = 1

        #if dataCollection.get("TiredStatus", 0) > self.tiredThd:
        self.userStatus["Tired"] += 0.1 * int(dataCollection.get("Tired", 0) > self.tiredThd)
        if dataCollection.get("Occupancy", False) and dataCollection.get("FaceConfidence",0) < self.faceThd:
            self.userStatus["FocusOffWork"] += 0.1
            Configs.logger.debug("check faceConfidence,FocusOffWork++ = {}".format(dataCollection.get("FaceConfidence",0)))
        if dataCollection.get("Occupancy", False) and dataCollection.get("FaceConfidence",0) > 0.8:
            self.userStatus["FocusOnWork"] += 0.1
        if dataCollection.get("InnerClimate", None):
            innerclimate = dataCollection.get("InnerClimate")
            if innerclimate["co2"] > self.co2Thd:
                self.userStatus["Tired"] += 0.001
        currentTime = time.localtime()
        self.userStatus["Tired"] += (currentTime.tm_hour / 24 + currentTime.tm_min / 60) / 10

        if dataCollection.get("UserEmotion", None) and dataCollection.get("FaceConfidence") > 0.8:
            emotion = dataCollection.get("UserEmotion")

            feelGood = emotion[0] + emotion[6]
            feelBad = emotion[1] + emotion[2] + emotion[3] + emotion[4] + emotion[5]
            if feelGood >=  feelBad :
                self.userStatus["FeelGood"] += 0.1
            else:
                self.userStatus["FeelBad"] += 0.1
        Configs.logger.debug("check dataCollection = {}".format(dataCollection))
        Configs.logger.debug("check status score now  = {}".format(self.userStatus))
        finalStatus = self.getStatus()
        Configs.logger.debug("check final status in Router = {}".format(finalStatus))


        return finalStatus
