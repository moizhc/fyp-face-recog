import tkinter as tk
from tkinter import messagebox, Toplevel, Label
from PIL import Image, ImageTk
from config import get_config
from mtcnn import MTCNN
from Learner import face_learner
from utils import prepare_facebank
from retinaface.detect_class_hr import FaceDetector
from face_aligner import FaceAligner
import json
import threading

# Configuration and model setup
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

# Argument parsing setup (if needed)
class Args:
    def __init__(self):
        self.tta = False

args = Args()

def update_facebank(detector):
    if detector == 'retinaface':
        print('Using retinaface for facebank update')
        targets, names = prepare_facebank(conf, learner.model, rface, tta=args.tta)
        
    elif detector == 'mtcnn':
        print('Using mtcnn for facebank update')
        targets, names = prepare_facebank(conf, learner.model, mtcnn, tta=args.tta)
       
    else:
        print('Detector not found for facebank update')
    loading_screen.destroy()
    messagebox.showinfo("Facebank Update", "Facebank updated successfully")

def start_update(detector):
    global loading_screen
    loading_screen = Toplevel(root)
    loading_screen.title("Updating Facebank")
    loading_screen.geometry(f"{window_width}x{window_height}+0+0")
    loading_screen.configure(bg="#3E3B3C")

    loading_label = Label(loading_screen, text="Updating facebank, please wait...", font="Arial 20 bold", fg="black", bg="#3E3B3C")
    loading_label.pack(expand=True)
    loading_screen.update()
    threading.Thread(target=update_facebank, args=(detector,)).start()

# Initialize the main window
root = tk.Tk()
root.title("Prepare Facebank")
window_width = 1366
window_height = 768
root.geometry(f"{window_width}x{window_height}+0+0")
root.configure(bg="#3E3B3C")

# Label
prepare_label = tk.Label(root, text="Prepare Facebank", fg="white", bg="#3E3B3C", font="Arial 20 bold")
prepare_label.pack(pady=20)

# Buttons frame
btn_frame = tk.Frame(root, bg="#3E3B3C")
btn_frame.pack(pady=20)

tk.Button(btn_frame, text="Use MTCNN", command=lambda: start_update('mtcnn'), font="Arial 15", bg="#000000", fg="white").pack(side="left", padx=20, pady=20)
tk.Button(btn_frame, text="Use Retinaface", command=lambda: start_update('retinaface'), font="Arial 15", bg="#000000", fg="white").pack(side="left", padx=20, pady=20)

# Icon
icon = Image.open("data/Iconoir-Team-Iconoir-Face-id.512.png")
icon = icon.resize((128, 128), Image.LANCZOS)
icon = ImageTk.PhotoImage(icon)

icon_label = tk.Label(root, image=icon, bg="#3E3B3C")
icon_label.image = icon
icon_label.pack(pady=20)

root.mainloop()
