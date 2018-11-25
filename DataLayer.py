import Configs
from UserEmotion.call import UserEmotion
from indoorClimate import IndoorClimate
from occupancy import Occupancy


class DataLayer:
    def __init__(self,siteID,sensorID,):
        self.siteID = siteID
        self.sensorID = sensorID
        self.userEmotion = UserEmotion()
        self.occupancy = Occupancy()
        self.indoorClimate = IndoorClimate()
    def collectData(self,startTimeStamp,endTimeStamp):
        dataCollection = {}
        useremotion = self.userEmotion.getData(self.siteID,self.sensorID,startTimeStamp,endTimeStamp)
        if useremotion:
            dataCollection["UserEmotion"] = useremotion["emotion"]
            dataCollection["FaceConfidence"] = useremotion["faceConfidence"] / 100
            dataCollection["Tired"] = useremotion["tired"]
        '''
        usertired  = UserTired.getData(self.siteID,self.sensorID,startTimeStamp,endTimeStamp)
        if usertired:
            dataCollection["TiredStatus"] = usertired
        '''
        occupancy = self.occupancy.getData(self.siteID,Configs.OCCUPANCY_SENSOR_ID,startTimeStamp,endTimeStamp)
        if Occupancy:
            dataCollection["Occupancy"] = occupancy
        innerclimate = self.indoorClimate.getData(self.siteID,Configs.CLIMATE_SENSOR_ID,startTimeStamp,endTimeStamp)
        if innerclimate:
            dataCollection["InnerClimate"] = innerclimate
        Configs.logger.debug("check dataCollection = {}".format(dataCollection))
        return dataCollection



