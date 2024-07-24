import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from easydict import EasyDict as edict
from pathlib import Path
import torch
from torch.nn import CrossEntropyLoss
from torchvision import transforms as trans

# Configuration settings
def get_config22(detector_name, model_name, training=True):
    conf = edict()
    conf.update_faces = False
    conf.data_path = Path('data')
    conf.work_path = Path('work_space/')
    conf.model_path = conf.work_path/'models'
    conf.log_path = conf.work_path/'log'
    conf.save_path = conf.work_path/'save'
    conf.video_path = r"videos\CAM2_MUNAM_ABDULLAH\abdul_wahab_wibu_front_cam2.mp4"
    conf.input_size = [112, 112]
    conf.embedding_size = 512
    conf.use_mobilfacenet = False
    conf.model_name = model_name  # treb_resnet, treb_mobile, Adaface, our_model
    conf.detector_name = detector_name  # mtcnn and retinaface
    conf.net_depth = 50
    conf.drop_ratio = 0.6
    conf.architecture = 'resnet18'  # resnet50/resnet18
    conf.net_mode = 'ir_se'  # or 'ir'
    conf.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    conf.test_transform = trans.Compose([
        trans.ToTensor(),
        trans.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
    ])
    conf.data_mode = 'emore'
    conf.vgg_folder = conf.data_path/'faces_vgg_112x112'
    conf.ms1m_folder = conf.data_path/'faces_ms1m_112x112'
    conf.emore_folder = conf.data_path/'faces_emore'
    conf.batch_size = 200  # mobilefacenet

    # --------------------Training Config ------------------------
    if training:
        conf.log_path = conf.work_path/'log'
        conf.save_path = conf.work_path/'save'
        conf.lr = 1e-3
        conf.milestones = [12, 15, 18]
        conf.momentum = 0.9
        conf.pin_memory = True
        conf.num_workers = 4
        conf.ce_loss = CrossEntropyLoss()
    # --------------------Inference Config ------------------------
    else:
        conf.facebank_path = Path(r'data\facebank')
        conf.threshold = 1.5
        conf.face_limit = 50
        conf.min_face_size = 15

    return conf

# Settings window function
def openSettings():
    settings_window = tk.Toplevel()
    settings_window.title("Settings")
    settings_window.geometry("600x400")
    settings_window.configure(bg="#3E3B3C")

    def save_settings():
        global conf  # Ensure we use the global config
        detector_name = detector_var.get()
        model_name = model_var.get()
        video_choice = video_var.get()
        if video_choice == "Live Feed":
            video_path = 0
        else:
            video_path = filedialog.askopenfilename()
        
        conf = get_config22(detector_name=detector_name, model_name=model_name)
        conf.video_path = video_path
        messagebox.showinfo("Settings Saved", "Your settings have been saved successfully.")
        settings_window.destroy()
    
    tk.Label(settings_window, text="Settings", fg="white", bg="#3E3B3C", font="Arial 20 bold").pack(pady=20)

    frame = tk.Frame(settings_window, bg="#3E3B3C")
    frame.pack(pady=10, padx=20, fill="both", expand=True)
    
    tk.Label(frame, text="Select Detector", fg="white", bg="#3E3B3C", font="Arial 15").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    detector_var = tk.StringVar(value=conf.detector_name)
    detector_menu = ttk.Combobox(frame, textvariable=detector_var, values=["mtcnn", "retinaface"], font="Arial 15")
    detector_menu.grid(row=0, column=1, padx=10, pady=10, sticky="e")

    tk.Label(frame, text="Select Model", fg="white", bg="#3E3B3C", font="Arial 15").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    model_var = tk.StringVar(value=conf.model_name)
    model_menu = ttk.Combobox(frame, textvariable=model_var, values=["treb_resnet", "treb_mobile", "Adaface", "our_model"], font="Arial 15")
    model_menu.grid(row=1, column=1, padx=10, pady=10, sticky="e")

    tk.Label(frame, text="Video Source", fg="white", bg="#3E3B3C", font="Arial 15").grid(row=2, column=0, padx=10, pady=10, sticky="w")
    video_var = tk.StringVar(value="Recording" if conf.video_path != 0 else "Live Feed")
    video_menu = ttk.Combobox(frame, textvariable=video_var, values=["Live Feed", "Recording"], font="Arial 15")
    video_menu.grid(row=2, column=1, padx=10, pady=10, sticky="e")

    save_button = tk.Button(settings_window, text="Save", command=save_settings, font="Arial 15", bg="#000000", fg="white")
    save_button.pack(pady=20)

# Initialize config
conf = get_config22()

# Initialize the root window and open the settings
root = tk.Tk()
root.withdraw()  # Hide the root window

openSettings()
root.mainloop()
