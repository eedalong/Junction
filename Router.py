
class Router:
    def __init__(self):
        # record the history user status and light status
        self.userStatus = {
            # FocusOffDesk contains 2 main situation: sleep on the desk or the user's focus is not on the testkable
            # this mode is set to save the energy
            "FocusOffWork":0,

            "Tired":0,
            # if the user is focusing on work, then just keep the setting of the light
            # if the user is once detected in focusing status, light status should be caution to change
            "FouseOnWork":0,
            # feel bad
            "FeelBad":0,
            # feel good
            "FeelGood":0,
            # if the user once set the light value, the setted value should not be changed for a while
        }
        self.tiredThd = 0.7
        self.co2Thd = 0.5

    def getStatus(self):
        saved_status = "FocusOnWork"
        saved_value = 0
        for key in self.userStatus:
            if self.userStatus[key] > saved_value:
                saved_value = self.userStatus
                saved_status = key
        return saved_status
    def Route(self,dataCollection):

        # we determine each status according to the environment data
        if dataCollection.get("TiredStatus",0) > self.tiredThd:
            self.userStatus["Tired"] += 0.1
        if dataCollection.get("Occupancy",False) and not dataCollection.get("Face"):
            self.userStatus["FocusOffWork"] += 0.1
        if dataCollection.get("InnerClimate",None):
            innerclimate = dataCollection.get("InnerClimate")
            if innerclimate["co2"] > self.co2Thd:
                self.userStatus["Tired"] += 0.1
        if dataCollection.get("UserEmotion",None):
            emotion = dataCollection.get("UserEmotion")
            feel_good = 0.5
            feel_bad  = 0.5
            if feel_good >= feel_bad:
                self.userStatus["FeelGood"] += 0.1
            else:
                self.userStatus["FeelBad"] += 0.1
        finalStatus = self.getStatus()
        return finalStatus


