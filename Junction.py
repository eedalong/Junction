import AILight
import Configs
def Junction(siteID,sensorID,timeInterval,historyLength):
    halvar = AILight.AILight(siteID,sensorID,timeInterval,historyLength)
    halvar.startWork()


if __name__ == "__main__":
    Junction(Configs.SITE_ID,Configs.SENSOR_ID,Configs.TIME_INTERVAL,Configs.HISTORY_LENGTH)