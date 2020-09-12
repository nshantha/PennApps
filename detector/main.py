import os
from video_processor import process_video

VIDEO_EXTENSIONS = [".mp4"]
VIDEO_PATH = ".\input_videos"

for fileName in os.listdir(VIDEO_PATH):
    if fileName.endswith(tuple(VIDEO_EXTENSIONS)):

        # safe distance in pixels set to 50
        process_video(os.path.join(VIDEO_PATH, fileName), 50)