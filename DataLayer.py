from UserEmotion import UserEmotion
from InnerClimate import InnerClimate
from Occupancy import Occupancy
from UserTired import UserTired
class DataLayer:
    def __init__(self,siteID,sensorID,startTimeStamp,endTimeStamp):
        self.siteID = siteID
        self.sensorID = sensorID
        self.startTimeStamp = startTimeStamp
        self.endTimeStamp = endTimeStamp

    def collectData(self):
        dataCollection = {}
        useremotion = UserEmotion.getData(self.siteID,self.sensorID,self.startTimeStamp,self.endTimeStamp)
        if useremotion:
            dataCollection["UserEmotion"] = useremotion
        usertired  = UserTired.getData(self.siteID,self.sensorID,self.startTimeStamp,self.endTimeStamp)
        if usertired:
            dataCollection["TiredStatus"] = usertired
        occupancy = Occupancy.getData(self.siteID,self.sensorID,self.startTimeStamp,self.endTimeStamp)
        if Occupancy:
            dataCollection["Occupancy"] = occupancy
        innerclimate = InnerClimate.getData(self.siteID,self.sensorID,self.startTimeStamp,self.endTimeStamp)
        if innerclimate:
            dataCollection["InnerClimate"] = innerclimate
        return dataCollection
    


