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
import json

SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768

def load_student_data(file_path):
    student_data = {}
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            student_data[row['Name']] = row
    return student_data

def get_attendance_file_path():
    directory = 'data/Attendance Sheets'
    if not os.path.exists(directory):
        os.makedirs(directory)
    current_date = datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.join(directory, f"{current_date}.csv")
    return file_path

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='for face verification')
    parser.add_argument("-u", "--update", help="whether perform update the facebank", action="store_true")
    parser.add_argument('-th', '--threshold', help='threshold to decide identical faces', default=1.54, type=float)
    parser.add_argument("-tta", "--tta", help="whether test time augmentation", action="store_true")
    parser.add_argument("-c", "--score", help="whether show the confidence score", action="store_true")
    parser.add_argument("-b", "--begin", help="from when to start detection (in seconds)", default=0, type=int)
    parser.add_argument("-d", "--duration", help="perform detection for how long (in seconds)", default=0, type=int)
    args = parser.parse_args()
    
    # Load student data
    student_data = load_student_data('student_data.csv')
    
    # Get attendance file path
    csv_filename = get_attendance_file_path()
    file_exists = os.path.isfile(csv_filename)
    
    # Initialize CSV file for attendance
    csv_file = open(csv_filename, 'a', newline='')
    csv_writer = csv.writer(csv_file)
    if not file_exists:
        csv_writer.writerow(['Name', 'ID', 'Gender', 'Degree', 'Department', 'Year', 'Semester', 'Date and Time'])
    
    """ conf = get_config(False) """
    # Load settings from config.json
    with open('config.json', 'r') as f:
        saved_config = json.load(f)

    # Initialize conf with values from config.json
    conf = get_config(detector_name=saved_config['detector_name'], model_name=saved_config['model_name'], training=False)
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

    # Create a named window with the specified size
    window_name = 'Face Recognition'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, SCREEN_WIDTH, SCREEN_HEIGHT)

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

                if face_width >= 20 and face_height >= 20:
                    if name not in detected_names:
                        if name not in detection_times:
                            detection_times[name] = current_time
                        elif current_time - detection_times[name] >= timedelta(seconds=1):
                            detected_names.add(name)
                            if name in student_data:
                                student_info = student_data[name]
                                csv_writer.writerow([
                                    student_info['Name'], student_info['ID'], student_info['Gender'], student_info['Degree'],
                                    student_info['Department'], student_info['Year'], student_info['Semester'], 
                                    current_time.strftime("%Y-%m-%d %H:%M:%S")
                                ])
                                print(f"Recorded: {name} at {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
                            else:
                                print(f"Name {name} not found in student_data.csv")
                            del detection_times[name]
                    else:
                        # Reset the detection time if not continuous
                        detection_times[name] = current_time

                # Always draw the bounding box and name
                if args.score:
                    frame = draw_box_name(bbox, name + '_{:.2f}'.format(score[idx]), frame)
                else:
                    frame = draw_box_name(bbox, name, frame)

            cv2.imshow(window_name, frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Video processing for {video_file_path} complete.")

    # Close CSV file
    csv_file.close()

print("Video processing complete. Attendance saved to", csv_filename)
