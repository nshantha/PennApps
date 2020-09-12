import cv2
import numpy as np 


def detect(layers, dnn_net, frame):

    # creates 4-dimensional blob from image. 1/255 to scale the pixel values to [0..1]
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (448, 448), swapRB=True, crop=False)
    dnn_net.setInput(blob)
    outs = dnn_net.forward(layers)

    boxes = []
    centroids = []
    confidences = []
    h, w = frame.shape[:2]

    # https://opencv-tutorial.readthedocs.io/en/latest/yolo/yolo.html#identifiy-objects
    for out in outs:
        '''
        The outputs object are vectors of lenght 85           
        4: the bounding box (centerx, centery, width, height)
        1: box confidence
        80: class confidence
        '''
        for detection in out:
            scores = detection[5:]
            # get max confidence categories
            classID = np.argmax(scores)
            confidence = scores[classID]
            # extract category 0 for person
            if classID == 0 and confidence > 0.3:  
                # restore size to original
                box = detection[:4] * np.array([w, h, w, h])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                # upper left of box
                box = [x, y, int(width), int(height)]
                boxes.append(box)
                confidences.append(float(confidence))
                centroids.append((centerX, centerY))
    
    # apply non-maximum supression
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.3)

    res = []
    if len(indices) > 0:
        for i in indices.flatten():
            x, y, w, h = (boxes[i][k] for k in range(4))

            #detections results hold confidence, locations and centroids for detecttion
            res.append((confidences[i], (x, y, x + w, y + h), centroids[i]))
    return res
