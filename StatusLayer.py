import time
import Configs

StatusList = [
    # FocusOffDesk contains 2 main situation: sleep on the desk or the user's focus is not on the testkable
    # this mode is set to save the energy
    "FocusOffWork",

    "Tired",
    # if the user is focusing on work, then just keep the setting of the light
    # if the user is once detected in focusing status, light status should be caution to change
    "FocusOnWork",
    # feel bad
    "FeelBad",
    # feel good
    "FeelGood"
    # if the user once set the light value, the setted value should not be changed for a while
]
UserStatus = {
    # FocusOffDesk contains 2 main situation: sleep on the desk or the user's focus is not on the testkable
    # this mode is set to save the energy
    "FocusOffWork": {"startTime": 0, "startValue":{"level":20, "color":200},"currentValue": {"level": 20, "color": 2000}, "targetValue": {"level": 30, "color": 2000}},
    "Tired": {"startTime": 0,"startValue":{"level":20, "color":200}, "current": {"level": 20, "color": 2000}, "targetValue": {"level": 90, "color": 6500}},
    # if the user is focusing on work, then just keep the setting of the light
    # if the user is once detected in focusing status, light status should be caution to change
    "FocusOnWork": {"startTime": 0,"startValue":{"level":50, "color":3500}, "currentValue": {"level": 50, "color": 3500}, "targetValue": {"level": 50, "color": 3500}},
    # feel bad
    "FeelBad": {"startTime": 0,"startValue":{"level":20, "color":200}, "currentValue": {"level": 20, "color": 2000}, "targetValue": {"level": 80, "color": 2500}},
    # feel good
    "FeelGood": {"startTime": 0, "startValue":{"level":20, "color":200},"currentValue": {"level": 20, "color": 2000}, "targetValue": {"level": None, "color": None}},
    # if the user once set the light value, the setted value should not be changed for a while

}


class DecideStatus:
    def __init__(self,timeInterval,historyLength):
        # record the history user status and light status
        self.timeInterval = 10
        self.timeNow = 0
        self.historyLength = 6
        self.lightHistory = [UserStatus["FocusOnWork"]] * self.historyLength
        self.statusPool = ["FocusOnWork"] * self.timeInterval
        self.status = "FocusOnWork"

    def getStatus(self):
        global StatusList
        savedStatus = "FocusOnWork"
        savedValue = 0
        for status in StatusList:
            count = self.statusPool.count(status)
            if count > savedValue:
                savedStatus = status
                savedValue = count
        return savedStatus

    def getValue(self,data):
        wbScore = 0.08
        if data["targetValue"]["level"] < data["currentValue"]["level"]:
            data["currentValue"]["level"] -=  data["currentValue"]["level"] * wbScore
            data["currentValue"]["level"] = max(data["currentValue"]["level"], data["targetValue"]["level"])
        else:
            data["currentValue"]["level"] += data["currentValue"]["level"] * wbScore
            data["currentValue"]["level"] = min(data["currentValue"]["level"], data["targetValue"]["level"])
        if data["targetValue"]["color"] < data["currentValue"]["color"]:
            data["currentValue"]["color"] -= data["currentValue"]["color"] * wbScore
            data["currentValue"]["color"] = max(data["currentValue"]["color"],data["targetValue"]["color"])
        else:
            data["currentValue"]["color"] += data["currentValue"]["color"] * wbScore
            data["currentValue"]["color"] = min(data["currentValue"]["color"], data["targetValue"]["color"])
        return data
    def duringWorkTime(self):
        currentTime = time.localtime()
        if currentTime.tm_hour > Configs.WORK_START_TIME and currentTime < Configs.WORK_END_TIME:
            return True
        return False
    def decideLight(self, status):
        Configs.logger.debug("check userstatus = {}".format(self.status))
        if self.timeNow == self.timeInterval:
            self.timeNow = 0
            userStatus = self.getStatus()
            self.status = userStatus
            targetValue = UserStatus[userStatus]
            # if not working time, set the light to help people relax
            if userStatus == "Tired" and not self.duringWorkTime():
                targetValue["targetValue"] = {"color":4000, "level":55}
            startTime = time.time()
            currentLight = self.lightHistory[0]["currentValue"]
            self.lightHistory.pop()
            targetValue["startTime"] = startTime
            targetValue["startValue"] = currentLight
            targetValue["currentValue"] = currentLight
            self.lightHistory.insert(0, targetValue)

        # during the interval
        # 1. we put the status into the status pool
        # 2. we update the light status to get to the target status

        #1. put the status into the status pool
        self.statusPool[self.timeNow] = status
        self.timeNow += 1


        #2. Get the new value at time t during timeInterval
        newValue = self.lightHistory[0]
        if self.status != "FeelGood":
            newValue  = self.getValue(self.lightHistory[0])
        self.lightHistory[0] = newValue
        Configs.logger.debug("check  statusPool = {}".format(self.statusPool))
        Configs.logger.debug("check userstatus = {}".format(self.status))
        Configs.logger.debug("check  light value = {}".format(newValue))
        Configs.logger.debug("check timeNow = {}".format(self.timeNow))
        return newValue



