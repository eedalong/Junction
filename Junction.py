import AILight
import Configs
def Junction(server, siteID,sensorID,timeInterval,historyLength):
    halvar = AILight.AILight(server,siteID,sensorID,timeInterval,historyLength)
    halvar.startWork()


if __name__ == "__main__":
    Junction(Configs.SERVER_URL,Configs.SITE_ID,Configs.OCCUPANCY_SENSOR_ID,Configs.TIME_INTERVAL,Configs.HISTORY_LENGTH)