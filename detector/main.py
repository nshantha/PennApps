import os
from video_processor import process_video
import cv2
from location_parser import parse_location

VIDEO_PATH = ".\input_videos"
location_map = parse_location(os.path.join(VIDEO_PATH, "locations.csv"))

VIDEO_EXTENSIONS = [".mp4"]
VIDEO_PATH = ".\input_videos"

# Set intervals (in frames) to send requests
REQ_INTERVAL = 30

for fileName in os.listdir(VIDEO_PATH):
    if fileName.endswith(tuple(VIDEO_EXTENSIONS)):

        # safe distance in pixels set to 50
        process_video(os.path.join(VIDEO_PATH, fileName), location_map, REQ_INTERVAL)


