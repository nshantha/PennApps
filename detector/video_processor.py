import cv2
from layers import get_layers
from detector import detect
from distance_analysis import analyze_dist

def process_video(video_path, safe_dist):

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
    
    while True:

        ret, frame = video_captured.read()

        # exit when EOF
        if not ret:
            break
        
        # resize frame
       	new_height = int(frame.shape[0] / frame.shape[1] * 700)
        frame = cv2.resize(frame, (700, new_height))   
           
        # use YOLO to detect persons in frame
        detections = detect(layers, dnn_net, frame)

        # detect unsafe distance
        unsafe = analyze_dist(detections, safe_dist)


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

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q") or key == 27:
            return unsafe_avg