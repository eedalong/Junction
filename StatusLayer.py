from Router import Router
import time

StatusList = [
    # FocusOffDesk contains 2 main situation: sleep on the desk or the user's focus is not on the testkable
    # this mode is set to save the energy
    "FocusOffWork",

    "Tired",
    # if the user is focusing on work, then just keep the setting of the light
    # if the user is once detected in focusing status, light status should be caution to change
    "FouseOnWork",
    # feel bad
    "FeelBad",
    # feel good
    "FeelGood"
    # if the user once set the light value, the setted value should not be changed for a while
]
UserStatus = {
    # FocusOffDesk contains 2 main situation: sleep on the desk or the user's focus is not on the testkable
    # this mode is set to save the energy
    "FocusOffWork": {"startTime": 0, "startValue":{"level":20, "color":200},"currentValue": {"level": 20, "color": 2000}, "targetValue": {"level": 20, "color": 3000}},
    "Tired": {"startTime": 0,"startValue":{"level":20, "color":200}, "current": {"level": 20, "color": 2000}, "targetValue": {"level": 60, "color": 2000}},
    # if the user is focusing on work, then just keep the setting of the light
    # if the user is once detected in focusing status, light status should be caution to change
    "FouseOnWork": {"startTime": 0,"startValue":{"level":20, "color":200}, "currentValue": {"level": 20, "color": 2000}, "targetValue": {"level": None, "color": None}},
    # feel bad
    "FeelBad": {"startTime": 0,"startValue":{"level":20, "color":200}, "currentValue": {"level": 20, "color": 2000}, "targetValue": {"level": 20, "color": 2000}},
    # feel good
    "FeelGood": {"startTime": 0, "startValue":{"level":20, "color":200},"currentValue": {"level": 20, "color": 2000}, "targetValue": {"level": None, "color": None}},
    # if the user once set the light value, the setted value should not be changed for a while
    "UserSet": {"startTime": 0,"startValue":{"level":20, "color":200}, "currentValue": {"level": 20, "color": 2000}, "targetValue": {"level": None, "color": None}}

}


class DecideStatus:
    def __init__(self):
        # record the history user status and light status
        self.timeInterval = 10
        self.timeNow = 0,
        self.historyLength = 6
        self.lightHistory = [UserStatus["FocusOnWork"]] * self.historyLength
        self.statusPool = ["FocusOnWork"] * self.timeInterval

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
        data["currentValue"]["level"] +=  data["currentValue"]["level"] * wbScore
        data["currentValue"]["color"] += data["currentValue"]["color"] * wbScore
        data["currentValue"]["level"] = max(data["currentValue"]["level"],data["targetValue"]["level"])
        data["currentValue"]["color"] = max(data["currentValue"]["color"],data["targetValue"]["color"])
        return data
    def decideLight(self, status):
        if self.timeNow == self.timeInterval:
            userStatus = self.getStatus()
            targetValue = UserStatus[userStatus]
            startTime = time.time()
            currentLight = self.lightHistory[0]["currentValue"]
            self.lightHistory.pop()
            targetValue["startTime"] = startTime
            targetValue["startValue"] = currentLight
            targetValue["currentValue"] = currentLight
            self.lightHistory.insert(0, targetValue)
        else:
            # during the interval
            # 1. we put the status into the status pool
            # 2. we update the light status to get to the target status

            #1. put the status into the status pool
            self.statusPool[self.timeNow] = status
            self.timeNow += 1

            #2. Get the new value at time t during timeInterval
            newValue  = self.getValue(self.lightHistory[0])
            self.lightHistory[0] = newValue
            return newValue["currentValue"]




