import cv2
import numpy as np

# Load the pre-trained MobileNet SSD model
prototxt_path = 'deploy.prototxt'
caffemodel_path = 'mobilenet_iter_73000.caffemodel'  # Adjust the name/path as needed
net = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)

# Define the list of classes and corresponding colors
CLASSES = ["background", "face", "dog", "cat"]  # Please adjust based on the classes in your model
COLORS = [(0, 255, 0), (0, 0, 255), (255, 0, 0), (0, 255, 255)]

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize to the input dimensions expected by MobileNet SSD
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)

    net.setInput(blob)
    detections = net.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.2:
            idx = int(detections[0, 0, i, 1])
            if CLASSES[idx] in ["face", "dog", "cat"]:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

    cv2.imshow('Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
