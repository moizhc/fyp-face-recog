import cv2
from PIL import Image
import argparse
import numpy as np
import torch
import os
import csv
from datetime import datetime, timedelta
from config import get_config
from mtcnn import MTCNN
from Learner import face_learner
from utils import load_facebank, draw_box_name, prepare_facebank
from retinaface.detect_class_hr import FaceDetector
from face_aligner import FaceAligner
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import threading

# Define constants for screen width and height
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

# Initialize Tkinter root window
root = tk.Tk()
root.title("Facial Recognition Attendance System")

# Create a frame to hold the video output and instructions
main_frame = tk.Frame(root, bg="#3E3B3C")
main_frame.pack(fill=tk.BOTH, expand=True)

# Create a label for instructions
instructions_label = tk.Label(main_frame, text="Press 'q' to stop attendance", fg="white", bg="#3E3B3C", font="Arial 15 bold")
instructions_label.pack()

# Create a frame for tracking output
tracking_frame = tk.LabelFrame(main_frame, text="Tracking Output", bg="#3E3B3C", fg="#2ea3ef", font="Arial 15 bold", labelanchor="n")
tracking_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Create a label to display video frames
video_label = tk.Label(tracking_frame)
video_label.pack()

# Function to update video frames in the Tkinter window
def update_frame(frame):
    # Convert the frame to an image format compatible with Tkinter
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)

    # Update the label with the new image
    video_label.imgtk = img
    video_label.configure(image=img)

def start_video_processing():
    parser = argparse.ArgumentParser(description='for face verification')
    parser.add_argument("-u", "--update", help="whether perform update the facebank", action="store_true")
    parser.add_argument('-th', '--threshold', help='threshold to decide identical faces', default=1.54, type=float)
    parser.add_argument("-tta", "--tta", help="whether test time augmentation", action="store_true")
    parser.add_argument("-c", "--score", help="whether show the confidence score", action="store_true")
    parser.add_argument("-b", "--begin", help="from when to start detection (in seconds)", default=0, type=int)
    parser.add_argument("-d", "--duration", help="perform detection for how long (in seconds)", default=0, type=int)
    args = parser.parse_args()
    
    # Initialize CSV file for attendance
    csv_filename = 'attendance.csv'
    csv_file = open(csv_filename, 'w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Name', 'Date and Time'])  # Header row with Date and Time
    
    conf = get_config(False)
    mtcnn = MTCNN()
    detector = FaceDetector()
    rface = FaceAligner(detector.detect_landmarks, desiredFaceWidth=112, desiredFaceHeight=112)
    
    learner = face_learner(conf, True)
    learner.threshold = 1.54  # Default threshold, can be adjusted
    learner.load_state(conf, r'work_space\save\model_ir_se50.pth', True, True)
    learner.model.eval()
    
    # Prepare facebank if update is required
    if conf.update_faces:
        if conf.detector_name == 'retinaface':
            targets, names = prepare_facebank(conf, learner.model, rface, tta=args.tta)
        elif conf.detector_name == 'mtcnn':
            targets, names = prepare_facebank(conf, learner.model, mtcnn, tta=args.tta)
        else:
            print('detector not found for facebank update')
        print('facebank updated')
    else:
        targets, names = load_facebank(conf)
        print('facebank loaded')
        
    # Use the video path provided in the configuration
    video_file_path = conf.video_path
    cap = cv2.VideoCapture(video_file_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_file_path}.")
        exit(1)
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Video {video_file_path} loaded successfully.")
    print(f"Frames per second (fps): {fps}")

    detection_times = {}
    detected_names = set()

    while cap.isOpened():
        isSuccess, frame = cap.read()
        frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))

        if isSuccess:
            try:
                if conf.detector_name == 'mtcnn':
                    bboxes, faces = mtcnn.align_multi(frame, conf.face_limit, conf.min_face_size)
                else:
                    img = frame
                    faces, _, bboxes = rface.align_multi(img)

                if faces is None:
                    continue

            except Exception as e:
                print(f'Error in face alignment: {e}')
                bboxes = []
                faces = []

            if len(bboxes) == 0:
                continue

            if conf.detector_name != 'mtcnn':
                faces = [Image.fromarray(face) for face in faces]
            else:
                bboxes = bboxes[:, :-1].astype(int) + [-1, -1, 1, 1]

            targets_list = [targets]
            results, score = learner.infer(conf, faces, targets_list, True)

            current_time = datetime.now()

            for idx, bbox in enumerate(bboxes):
                name = names[results[idx] + 1]
                face_width = bbox[2] - bbox[0]
                face_height = bbox[3] - bbox[1]

                if face_width >= 60 and face_height >= 60:
                    if name not in detected_names:
                        if name not in detection_times:
                            detection_times[name] = current_time
                        elif current_time - detection_times[name] >= timedelta(seconds=2):
                            detected_names.add(name)
                            csv_writer.writerow([name, current_time.strftime("%Y-%m-%d %H:%M:%S")])
                            print(f"Recorded: {name} at {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
                            del detection_times[name]
                    else:
                        # Reset the detection time if not continuous
                        detection_times[name] = current_time

                # Always draw the bounding box and name
                if args.score:
                    frame = draw_box_name(bbox, name + '_{:.2f}'.format(score[idx]), frame)
                else:
                    frame = draw_box_name(bbox, name, frame)

            update_frame(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Video processing for {video_file_path} complete.")

    # Close CSV file
    csv_file.close()

# Function to start video processing in a separate thread
def start_thread():
    # Run video processing after the mainloop has started
    root.after(1000, start_video_processing)

# Add a button to start video processing
start_button = tk.Button(main_frame, text="Start Video Processing", command=start_thread, font="Arial 15", bg="#000000", fg="white")
start_button.pack(pady=10)

# Run the Tkinter main loop
root.mainloop()
