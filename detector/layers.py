import cv2

def get_layers():
    
    # read model from YOLOv3 learned network config and weights
    dnn_net = cv2.dnn.readNetFromDarknet(".\detector\yolo-coco\yolov3.cfg", ".\detector\yolo-coco\yolov3.weights")

    layers = dnn_net.getLayerNames()
    # print(layers)
    layers = [layers[i[0] - 1] for i in dnn_net.getUnconnectedOutLayers()]
    return layers, dnn_net