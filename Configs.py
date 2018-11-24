import os
import sys


def add_path(path):
    sys.path.insert(0, path)


#SERVER_URL = "https://v0wwaqqnpa.execute-api.eu-west-1.amazonaws.com"
DUMMY = True
SERVER_URL = "http://192.168.43.44:7001"
TIME_INTERVAL = 100
HISTORY_LENGTH = 6

SITE_ID = "site_exp"
CLIMATE_SENSOR_ID = "855f35c3-0dee-4e76-b06c-9e76c9ad08cc"
DEVICE_ID = "8b36b47a-1286-40a8-bc81-1ad32ddca3fc"
OCCUPANCY_SENSOR_ID = "40eba976-a328-47ba-900b-500f53a52f87"
API_KEY = "zZW3DPNfb23pxs2c19uLb5YKX8AHRRCJ3eOIFQPO"
WORK_START_TIME = 9
WORK_END_TIME = 17
OCCUPANCY_PATH = "./occupancy/"
add_path(OCCUPANCY_PATH)
INDOOR_PATH = "./indoorClimate/"
add_path(INDOOR_PATH)
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
