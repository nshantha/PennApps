import cv2
from layers import get_layers
from detector import detect
from distance_analysis import analyze_dist
import numpy as np
import time
from requests import send_req



clicks = []
global frame

def mouse_on(event, x, y, *args, **kwargs):
    global clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        if "clicks" not in globals():
            clicks = []
        clicks.append((x, y))

        if len(clicks) <= 4:
            cv2.circle(frame, (x, y), 2, (0, 0, 255), 2)
        else:
            cv2.circle(frame, (x, y), 2, (255, 0, 0), 2)
            
        if len(clicks) > 1 and len(clicks) <= 4:
            cv2.line(frame, (x, y), (clicks[len(clicks)-2][0], clicks[len(clicks)-2][1]), (70, 70, 70), 2)
            if len(clicks) == 4:
                cv2.line(frame, (x, y), (clicks[0][0], clicks[0][1]), (70, 70, 70), 2)
        





def process_video(video_path, location_map, REQ_INTERVAL):
    count = 0
    global clicks
    # import Common Object in Context categories names
    file_coconames = open(".\detector\yolo-coco\coco.names")
    coco_categories = file_coconames.read().split("\n")
    
    # get layers and model
    layers, dnn_net = get_layers()

    # video frame by frame analysis
    video_captured = cv2.VideoCapture(video_path)

    # number of violations in social distance observed over all frames
    unsafe_accumulated = 0
    num_frames = 0
    global frame

    # configure mouse call back
    cv2.namedWindow("frame")
    cv2.setMouseCallback("frame", mouse_on)

    # FPS
    start_time = time.time()

    while True:

        ret, frame = video_captured.read()

        # exit when EOF
        if not ret:
            break
        
        # resize frame
       	new_height = int(frame.shape[0] / frame.shape[1] * 700)
        frame = cv2.resize(frame, (700, new_height))   
           
        # get mouse clicks
        if not count:
            while True:
                cv2.imshow("frame", frame)
                cv2.waitKey(1)
                if len(clicks) == 8:
                    cv2.destroyWindow("frame")
                    break
            four_pts = clicks


        # Transform perspective
        (H, W) = frame.shape[:2]
        src = np.float32(np.array(four_pts[:4]))
        dst = np.float32([[0, H], [W, H], [W, 0], [0, 0]])
        prespective_transform = cv2.getPerspectiveTransform(src, dst)
        birdseye_result = cv2.warpPerspective(frame, prespective_transform, (500, 600)) 

        # Transformed Capture 
        cv2.imshow('Birdseye', birdseye_result) 

        # Tranform distance to pixels
        pts = np.float32(np.array([four_pts[4:7]]))
        trans_pts = cv2.perspectiveTransform(pts, prespective_transform)[0]

        # Use three points to calculate real distance in pixels for 6 feet in x and y axis
        xdist_in_pixels = np.sqrt((trans_pts[0][0] - trans_pts[1][0]) ** 2 + (trans_pts[0][1] - trans_pts[1][1]) ** 2)
        ydist_in_pixels = np.sqrt((trans_pts[0][0] - trans_pts[2][0]) ** 2 + (trans_pts[0][1] - trans_pts[2][1]) ** 2)
        
        # Display four points of rectangle
        cv2.polylines(frame, [np.array(four_pts[:4], np.int32)], True, (255, 255, 255), thickness=2)
        



        # use YOLO to detect persons in frame
        detections = detect(layers, dnn_net, frame)

        # detect unsafe distance
        unsafe = analyze_dist(detections, prespective_transform, xdist_in_pixels, ydist_in_pixels)


        # loop over the results to render boxes
        for (i, (prob, bbox, centroid)) in enumerate(detections):
            (startX, startY, endX, endY) = bbox
            (cX, cY) = centroid
            color = (0, 255, 0)


            if i in unsafe:
                color = (0, 0, 255)

            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 1)
            # cv2.circle(frame, (cX, cY), 5, color, 1)

        text = "Current Social Distancing Violations: {}".format(len(unsafe))
        cv2.putText(frame, text, (10, frame.shape[0] - 50),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        unsafe_accumulated += len(unsafe)
        num_frames += 1
        unsafe_avg = unsafe_accumulated / num_frames

        text = "Average Violations Per Frame: {}".format(round(unsafe_avg, 2))
        cv2.putText(frame, text, (10, frame.shape[0] - 25),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)    

        if num_frames == 1:
            start_time = time.time()

        curr_time = time.time()
        if (curr_time - start_time) != 0:
            fps = num_frames / (curr_time - start_time)
            text = "FPS: {}".format(round(fps, 2))
            cv2.putText(frame, text, (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)    

        # cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if count != 0:
            cv2.imshow('processed', frame)    
        count = count + 1

        if (num_frames % REQ_INTERVAL == 0):
            send_req(unsafe_avg, video_path, location_map)

        if key == ord("q") or key == 27:
            cv2.destroyWindow("processed")
            clicks = []
            return
    clicks = []
    