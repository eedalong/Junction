import Configs
from UserEmotion import UserEmotion
from IndoorClimate import IndoorClimate
from occupancy import Occupancy
from UserTired import UserTired

class DataLayer:
    def __init__(self,siteID,sensorID,):
        self.siteID = siteID
        self.sensorID = sensorID
    def collectData(self,startTimeStamp,endTimeStamp):
        dataCollection = {}
        useremotion = UserEmotion.getData(self.siteID,self.sensorID,startTimeStamp,endTimeStamp)
        if useremotion:
            dataCollection["UserEmotion"] = useremotion
        usertired  = UserTired.getData(self.siteID,self.sensorID,startTimeStamp,endTimeStamp)
        if usertired:
            dataCollection["TiredStatus"] = usertired
        occupancy = Occupancy.getData(self.siteID,self.sensorID,startTimeStamp,endTimeStamp)
        if Occupancy:
            dataCollection["Occupancy"] = occupancy
        innerclimate = IndoorClimate.getData(self.siteID,self.sensorID,startTimeStamp,endTimeStamp)
        if innerclimate:
            dataCollection["InnerClimate"] = innerclimate
        return dataCollection



