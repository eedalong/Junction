import cv2
import json
import os
image_path = "D:\\Dalong\\Sleepy"
target_path = "D:\\Dalong\\Result"
log_file = "D:\\Dalong\\log_file.json"

input_file = open(log_file,"r")
input_file = json.load(input_file)

image_count = len(input_file["data"])
print(image_count)
for image_index in range(image_count):
    path = os.path.join(image_path,"frame_{}.jpg".format(image_index))
    image = cv2.imread(path)
    data = input_file["data"][image_index]
    cv2.putText(image, "currentStatus:{} ".format(data["currentStatus"]), (0, 20), cv2.FONT_HERSHEY_COMPLEX,0.5, (0, 0, 255), 1)
    if data["finalValue"]["targetValue"]["level"] == 30:
        targetStatus = "FocusOffWork"
    if data["finalValue"]["targetValue"]["level"] == 90:
        targetStatus = "Tired"
    if data["finalValue"]["targetValue"]["level"] == 50:
        targetStatus = "FocusOnWork"
    if data["finalValue"]["targetValue"]["level"] == 80:
        targetStatus = "FeelBad"
    if data["finalValue"]["targetValue"]["level"] == None:
        targetStatus = "FeelGood"
    cv2.putText(image, "targetStatus:{} ".format(targetStatus), (0, 40), cv2.FONT_HERSHEY_COMPLEX,0.5, (0, 0, 255), 1)
    cv2.putText(image, "currentValue:{} {} ".format(data["finalValue"]["currentValue"]["level"],data["finalValue"]["currentValue"]["color"]), (0, 60), cv2.FONT_HERSHEY_COMPLEX,0.5, (0, 0, 255), 1)
    cv2.putText(image, "targetValue:{} {} ".format(data["finalValue"]["targetValue"]["level"],data["finalValue"]["targetValue"]["color"]), (0, 80), cv2.FONT_HERSHEY_COMPLEX,0.5, (0, 0, 255), 1)
    cv2.putText(image, "Occupancy:{} ".format(data["dataCollection"]["Occupancy"]), (0, 100), cv2.FONT_HERSHEY_COMPLEX,0.5, (0, 0, 255), 1)
    cv2.putText(image, "co2:{} ".format(data["dataCollection"]["InnerClimate"]["co2"]), (0, 120), cv2.FONT_HERSHEY_COMPLEX,0.5, (0, 0, 255), 1)
    cv2.putText(image, "humidity:{} ".format(data["dataCollection"]["InnerClimate"]["humidity"]), (0, 140), cv2.FONT_HERSHEY_COMPLEX,0.5, (0, 0, 255), 1)

    cv2.imwrite(os.path.join(target_path,"frame_{}.jpg".format(image_index)),image)
