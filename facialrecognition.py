import face_recognition
import picamera
import numpy as np
import os
import json
import cv2
from picamera.array import PiRGBArray
import tkinter as tk
from tkinter import scrolledtext
import time
import dlib
import threading

known_face_encodings = []
known_face_names = []
data_file = "known_faces.json"

app_running = True

if os.path.exists(data_file):
    with open(data_file, 'r') as f:
        data = json.load(f)
        known_face_names = data['names']
        known_face_encodings = [np.array(encoding) for encoding in data['encodings']]

# GUI Part
root = tk.Tk()
root.title("Face Name Input")

console = scrolledtext.ScrolledText(root, width=50, height=10, state="disabled")
console.pack(pady=10)

label = tk.Label(root, text="Enter name of new face:")
label.pack(pady=10)

text_input = tk.StringVar()
entry = tk.Entry(root, textvariable=text_input)
entry.pack(pady=10)

unknown_encodings = []

def submit():
    global known_face_encodings, known_face_names, unknown_encodings
    name = text_input.get()
    if name:
        for encoding in unknown_encodings:
            known_face_encodings.append(encoding)
            known_face_names.append(name)
            
        with open(data_file, 'w') as f:
            json.dump({
                'names': known_face_names,
                'encodings': [enc.tolist() for enc in known_face_encodings]
            }, f)

        unknown_encodings = []  # Reset the unknown encodings
        text_input.set("")

btn = tk.Button(root, text="Submit", command=submit)
btn.pack(pady=10)

# Initialize dlib models
predictor_path = "shape_predictor_68_face_landmarks_GTX.dat"
face_rec_model_path = "dlib_face_recognition_resnet_model_v1.dat"
predictor = dlib.shape_predictor(predictor_path)
face_rec_model = dlib.face_recognition_model_v1(face_rec_model_path)

def compute_encodings(frame, face_locations):
    dlib_face_locations = [dlib.rectangle(left, top, right, bottom) for (top, right, bottom, left) in face_locations]
    face_encodings = []
    
    for face_location in dlib_face_locations:
        shape = predictor(frame, face_location)
        if frame.shape[2] == 3:  # Ensure the frame has 3 color channels
            encoding = np.array(face_rec_model.compute_face_descriptor(frame, shape, num_jitters=1))
            face_encodings.append(encoding)
    
    return face_encodings

face_trackers = {}  # Will store tracker objects with the corresponding names.
recently_recognized = set()

def console_insert(msg):
    console.config(state="normal")
    console.insert(tk.END, msg + '\n')
    console.see(tk.END)
    console.config(state="disabled")


def recognize_faces(frame):
    global unknown_encodings, face_trackers, recently_recognized

    rgb_frame = frame[:, :, ::-1]  # Convert BGR to RGB

    # Update the trackers instead of recognizing each time
    for id, (tracker, name) in list(face_trackers.items()):
        quality = tracker.update(rgb_frame)
        if quality > 7:  
            pos = tracker.get_position()
            left = int(pos.left())
            top = int(pos.top())
            right = int(pos.right())
            bottom = int(pos.bottom())
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
        else:
            del face_trackers[id]

    # If there are no trackers, then recognize the face
    if not face_trackers:
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = compute_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            if name == "Unknown":
                unknown_encodings.append(face_encoding)
                console_insert("Unidentified face detected. Please enter a name in the input box and press submit.")
            else:
                console_insert(f"Recognized {name}")

            # Initiate tracker for the face
            tracker = dlib.correlation_tracker()
            rect = dlib.rectangle(left, top, right, bottom)
            tracker.start_track(rgb_frame, rect)
            face_id = str(top) + str(right)
            face_trackers[face_id] = (tracker, name)

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        global app_running
        app_running = False




def update_video():
    camera = picamera.PiCamera()
    camera.resolution = (320, 240)
    raw_capture = PiRGBArray(camera, size=(320, 240))

    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        if not app_running:
            break
        recognize_faces(frame.array)
        raw_capture.truncate(0)

    camera.close()

def on_closing():
    global app_running
    app_running = False
    cv2.destroyAllWindows()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Run video capture in a separate thread
threading.Thread(target=update_video).start()
root.mainloop()
