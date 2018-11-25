import DataLayer
import Router
import SendRequest
import StatusLayer
import Configs
import time
import time
import pytz
import datetime
import json
import copy
class AILight:
    def __init__(self,server, siteID, sensorID, timeInterval, historyLength):
        self.server = server
        self.siteID = siteID
        self.sensorID = sensorID
        self.timeInterval = timeInterval
        self.historyLength = historyLength
        self.data = []
    def local_to_utc(self,local_ts, utc_format='%Y-%m-%dT%H:%M:%S.000Z'):
        local_tz = pytz.timezone('Asia/Chongqing')
        local_format = "%Y-%m-%d %H:%M:%S"
        time_str = time.strftime(local_format, time.localtime(local_ts))
        dt = datetime.datetime.strptime(time_str, local_format)
        local_dt = local_tz.localize(dt, is_dst=None)
        utc_dt = local_dt.astimezone(pytz.utc)
        return utc_dt.strftime(utc_format)
    def startWork(self):
        dataLayer = DataLayer.DataLayer(self.siteID, self.sensorID)
        router = Router.Router()
        sender = SendRequest.SendRequest(self.server)
        statusLayer = StatusLayer.DecideStatus(self.timeInterval, self.historyLength)
        frame_index = 0
        log_file = open("log_file.json","w")
        all_data = {"data":[]}
        max_frame = 120
        while True:
            startTime = time.time()
            startTime = self.local_to_utc(startTime)
            dataCollection = dataLayer.collectData(startTime, None)
            currentStatus = router.Route(dataCollection)
            finalValue = statusLayer.decideLight(currentStatus)
            if finalValue["targetValue"]["color"]:
                sender.setLightColor(Configs.SITE_ID,Configs.DEVICE_ID,finalValue["currentValue"]["color"])
                sender.setLightIntensity(Configs.SITE_ID,Configs.DEVICE_ID,finalValue["currentValue"]["level"])
            log_data = {
                "frame_index":frame_index,
                "dataCollection":dataCollection,
                "currentStatus": currentStatus,
                "finalValue":finalValue
                }
            log_file = open("D:\\Dalong\\log_file.json","w")
            self.data.append(copy.deepcopy(log_data))
            all_data["data"] = self.data
            Configs.logger.info("log file length = {}".format(len(all_data["data"])))
            json.dump(all_data,log_file)
            log_file.close()

