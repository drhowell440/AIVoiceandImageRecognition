import cv2
import numpy as np
import tflite_runtime.interpreter as tflite
import time
import threading
import queue

# Load TFLite model and allocate tensors.
interpreter = tflite.Interpreter(model_path="ssd_mobilenet_v2_coco_quant_postprocess.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Open the camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

frame_queue = queue.Queue(maxsize=1)

# Capture thread function
def capture_thread():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_queue.full():
            frame_queue.get()
        
        frame_queue.put(frame)
        time.sleep(0.02)  # Optional slight delay to prevent excessive CPU usage

# Start the capture thread
threading.Thread(target=capture_thread, daemon=True).start()



# List of COCO class names
LABELS = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck",
    "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench",
    "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra",
    "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", 
    "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove",
    "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup", 
    "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
    "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch",
    "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse", 
    "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
    "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", 
    "toothbrush"
]


while True:
    if not frame_queue.empty():
        frame = frame_queue.get()
        
        start_time = time.time()

        # Resize directly to 300x300
        input_data = cv2.resize(frame, (300, 300))
        input_data = np.expand_dims(input_data, axis=0)

        # Set the input tensor and invoke the interpreter
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()

        # Retrieve detection results
        boxes = interpreter.get_tensor(output_details[0]['index'])[0]
        class_labels = interpreter.get_tensor(output_details[1]['index'])[0]
        scores = interpreter.get_tensor(output_details[2]['index'])[0]

        height, width, _ = frame.shape

        # Use numpy to get indices of scores above the threshold
        indices = np.where(scores > 0.4)

        # Check if there are any detections before processing them
        if len(indices[0]) > 0:
            for i in indices[0]:
                # Transform box coordinates
                ymin, xmin, ymax, xmax = boxes[i]
                startX, startY, endX, endY = int(xmin * width), int(ymin * height), int(xmax * width), int(ymax * height)

                # Draw the bounding box
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

                # Display the label
                label = f"{LABELS[int(class_labels[i])]}: {scores[i]:.2f}"
                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Calculate and display FPS
            fps = 1.0 / (time.time() - start_time)
            cv2.putText(frame, f"FPS: {fps:.2f}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        cv2.imshow('Human Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
