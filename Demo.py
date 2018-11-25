import requests
import json
import time
import Configs
import os
import cv2
DUMMY_API = {

    "IntensitySet": "/V1/sites/{siteId}/devices/{deviceId}/level/{level}",
    "ColorSet": "/V1/sites/{siteId}/devices/{deviceId}/color/{color}"

}
json_paths = ["D:\\Dalong\\FocusOn2FocusOff\\log_file.json","D:\\Dalong\\FocusOff2FocusOn\\log_file.json",
             "D:\\Dalong\\FocusOn2Tired\\log_file.json",]
image_paths = ["D:\\Dalong\\FocusOn2FocusOff","D:\\Dalong\\FocusOff2FocusOn","D:\\Dalong\\FocusOn2Tired"]
demo_index = 0
demo_count = 3
while(True):
    json_path = json_paths[demo_index % demo_count]
    image_path = image_paths[demo_index % demo_count]
    input_file = open(json_path, 'r')
    input_file = json.load(input_file)
    input_data = input_file["data"]
    count = len(input_data)
    for image_index in range(count):
        image = cv2.imread(os.path.join(image_path,"frame_{}.jpg".format(image_index)))
        print(type(image))
        level = int(input_data[image_index]["finalValue"]["currentValue"]["level"])
        color = int(input_data[image_index]["finalValue"]["currentValue"]["color"])
        requests.post(url = Configs.SERVER_URL+DUMMY_API["IntensitySet"].format(siteId = Configs.SITE_ID,deviceId=Configs.DEVICE_ID,level=level))
        requests.post(url = Configs.SERVER_URL+DUMMY_API["ColorSet"].format(siteId = Configs.SITE_ID,deviceId=Configs.DEVICE_ID,color=color))
        Configs.logger.info("send level and color to server  = {} {}".format(level,color))
        cv2.imshow("test",image)
        if cv2.waitKey(1000) & 0xFF == ord('q'):
            break
    demo_index+=1


