import os
import sys
def add_path(path):
    sys.path.insert(0,path)

SERVER_URL = ""
TIME_INTERVAL = 100
HISTORY_LENGTH = 6
SITE_ID = ""
SENSOR_ID = ""
API_KEY = "zZW3DPNfb23pxs2c19uLb5YKX8AHRRCJ3eOIFQPO"

OCCUPANCY_PATH = "./occupancy/"
add_path(OCCUPANCY_PATH)
INDOOR_PATH = "./innerClimate/"
add_path(INDOOR_PATH)
