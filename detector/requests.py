import json
import os

def send_req(weight, video_path, location_map):
    head, fileName = os.path.split(video_path)
    # post data
    data = {
            'lat': location_map[fileName]['lat'],
            'lng': location_map[fileName]['lng'],
            'weight': weight
            }
    json.dumps(data)
    print(data)
    # r = requests.post('http://72.80.53.164:8080', json=data)