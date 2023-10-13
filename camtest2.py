import cv2
import dlib
import numpy as np
import time

# Load the COCO class labels
LABELS = open("coco.names").read().strip().split("\n")

# Use YOLOv3-tiny for faster detections
net = cv2.dnn.readNetFromDarknet("yolov3-tiny.cfg", "yolov3-tiny.weights")

unconnected_out_layers = net.getUnconnectedOutLayers().flatten()
layer_names = [net.getLayerNames()[i - 1] for i in unconnected_out_layers]

def get_fps(start_time, frame_counter):
    current_time = time.time()
    elapsed_time = current_time - start_time
    fps = frame_counter / elapsed_time
    return fps

def detect_objects(frame, net, layer_names):
    (H, W) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(layer_names)
    
    boxes = []
    confidences = []
    classIDs = []
    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            if confidence > 0.4:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)
    
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)
    
    trackers = [] # Initialize the trackers list here instead of clearing it
    
    if len(idxs) > 0:
        for i in idxs.flatten():
            if LABELS[classIDs[i]] in ["person", "dog"]:
                (x, y, w, h) = boxes[i]
                tracker = dlib.correlation_tracker()
                rect = dlib.rectangle(x, y, x + w, y + h)
                tracker.start_track(frame, rect)
                label = LABELS[classIDs[i]]
                trackers.append((tracker, label))
    
    return frame, trackers


def main():
    start_time = time.time()
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    
    if not cap.isOpened():
        print("Error: Couldn't open the camera.")
        exit()

    trackers = []
    frame_counter = 0
   


    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Couldn't read frame.")
            break

        frame_counter += 1
        fps = get_fps(start_time, frame_counter)
        if frame_counter % 60 == 0:
            frame, trackers = detect_objects(frame, net, layer_names)
        else:
            for tracker, label in trackers:
                tracker.update(frame)
                pos = tracker.get_position()
                
                startX = int(pos.left())
                startY = int(pos.top())
                endX = int(pos.right())
                endY = int(pos.bottom())
                
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                

        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.imshow('Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
