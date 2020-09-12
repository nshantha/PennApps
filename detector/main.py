import os
from video_processor import process_video
import requests
import json
from location_parser import parse_location

VIDEO_EXTENSIONS = [".mp4"]
VIDEO_PATH = ".\input_videos"

location_map = parse_location(os.path.join(VIDEO_PATH, "locations.csv"))

for fileName in os.listdir(VIDEO_PATH):
    if fileName.endswith(tuple(VIDEO_EXTENSIONS)):

        # safe distance in pixels set to 50
        weight = process_video(os.path.join(VIDEO_PATH, fileName), 30)

        # post data
        data = {
                'lat': location_map[fileName]['lat'],
                'lng': location_map[fileName]['lng'],
                'weight': weight
                }
        json.dumps(data)
        print(data)
        r = requests.post('http://localhost:8080', json=data)
