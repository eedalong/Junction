import DataLayer
import Router
import SendRequest
import StatusLayer
import Configs
import time

class AILight:
    def __init__(self,server, siteID, sensorID, timeInterval, historyLength):
        self.server = server
        self.siteID = siteID
        self.sensorID = sensorID
        self.timeInterval = timeInterval
        self.historyLength = historyLength

    def startWork(self):
        dataLayer = DataLayer.DataLayer(self.siteID, self.sensorID)
        router = Router.Router()
        sender = SendRequest.SendRequest(self.server)
        statusLayer = StatusLayer.DecideStatus(self.timeInterval, self.historyLength)
        while True:
            startTime = time.time()
            dataCollection = dataLayer.collectData(startTime, startTime)
            currentStatus = router.Route(dataCollection)
            finalValue = statusLayer.decideLight(currentStatus)
            sender.setLightColor(finalValue["color"])
            sender.setLightIntensity(finalValue["level"])


