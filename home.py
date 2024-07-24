import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import subprocess
import os
import json

config_file = 'config.json'

def save_config(config):
    with open(config_file, 'w') as f:
        json.dump(config, f)

def load_config():
    if os.path.exists(config_file):
        print(f"Config file '{config_file}' found. Loading...")
        with open(config_file, 'r') as f:
            config = json.load(f)
            print(f"Config loaded: {config}")
            return config
    else:
        print(f"Config file '{config_file}' not found. Using default config.")
    return {'detector_name': 'retinaface', 'model_name': 'treb_resnet'}

def open_settings_window():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("400x300")
    settings_window.configure(bg="#3E3B3C")

    def save_settings():
        selected_detector = detector_var.get()
        selected_model = model_var.get()
        config = {'detector_name': selected_detector, 'model_name': selected_model}
        save_config(config)
        messagebox.showinfo("Settings Saved", f"Detector: {selected_detector}\nModel: {selected_model}")
        settings_window.destroy()

    config = load_config()

    detector_var = tk.StringVar(value=config['detector_name'])
    model_var = tk.StringVar(value=config['model_name'])

    detectors = ["mtcnn", "retinaface"]
    models = ["treb_resnet", "treb_mobile", "Adaface", "our_model"]

    tk.Label(settings_window, text="Select Detector", bg="#3E3B3C", fg="white", font="Arial 14 bold").pack(pady=10)
    detector_menu = ttk.Combobox(settings_window, textvariable=detector_var, values=detectors, state="readonly")
    detector_menu.pack(pady=5)

    tk.Label(settings_window, text="Select Model", bg="#3E3B3C", fg="white", font="Arial 14 bold").pack(pady=10)
    model_menu = ttk.Combobox(settings_window, textvariable=model_var, values=models, state="readonly")
    model_menu.pack(pady=5)

    save_button = tk.Button(settings_window, text="Save", command=save_settings, bg="#000000", fg="white",
                            font="Arial 12 bold", pady=10, bd=0, highlightthickness=0, activebackground="#3E3B3C", activeforeground="white")
    save_button.pack(pady=20)

def open_help_window():
    help_window = tk.Toplevel(root)
    help_window.title("Help")
    help_window.geometry("1366x768+0+0")
    help_window.configure(bg="#3E3B3C")

    #tk.Label(help_window, text="Help Information", bg="#3E3B3C", fg="black", font="Arial 16 bold").pack(pady=10)
    tk.Label(help_window,text="Help Information", bg="black", fg="white", width="300", height="2", font=("Calibri", 25)).pack()
    tk.Label(text="", bg="#3E3B3C").pack()
    
    help_text = """
Usage Scenarios
ArcFace with ResNet
  •Scenario: Ideal for environments with consistent, good lighting. Offers high accuracy and handles slight face angle variations well.

ArcFace with MobileFaceNet
  •Scenario: Best for mobile or edge device environments with limited resources. Fast and lightweight, suitable for real-time applications under good and moderate lighting.

AdaFace
  •Scenario: Suitable for diverse facial variations and poses. Performs best in good lighting and moderately well in challenging lighting conditions.

Attention Guided Distillation Approach
  •Scenario: Designed for low-resolution images and resource-constrained environments. Maintains decent performance across all lighting conditions due to attention mechanisms.

Caution Note
   Important: Always use the Prepare Facebank functionality when adding a new user to the student panel. This step is crucial for accurate recognition and authentication, ensuring system integrity and reliability.

    """
    
    tk.Label(help_window, text=help_text, bg="#3E3B3C", fg="black", font="Arial 18", justify="left", wraplength=950).pack(pady=10)
    
    close_button = tk.Button(help_window, text="Close", command=help_window.destroy, bg="#000000", fg="white",
                             font="Arial 20 bold", pady=10, bd=0, highlightthickness=0, activebackground="#3E3B3C", activeforeground="white")
    close_button.pack(pady=20)

root = tk.Tk()
root.geometry("1366x768+0+0")

pages = []
for i in range(5):
    pages.append(tk.Frame(root, bg="#3E3B3C"))
    pages[i].pack(side="top", fill="both", expand=True)
    pages[i].place(x=0, y=0, relwidth=1, relheight=1)

def goBack():
    global active_page, thread_event, webcam

    if active_page == 4 and not thread_event.is_set():
        thread_event.set()
        webcam.release()

    for widget in pages[active_page].winfo_children():
        widget.destroy()

    pages[0].lift()
    active_page = 0

def basicPageSetup(pageNo):
    global left_frame, right_frame, heading

    back_img = tk.PhotoImage(file=r"C:\Users\Uzi\Downloads\Facial-Recognition-for-Crime-Detection-master\Facial-Recognition-for-Crime-Detection-master\img\back.png")
    back_button = tk.Button(pages[pageNo], image=back_img, bg="#3E3B3C", bd=0, highlightthickness=0,
                            activebackground="#3E3B3C", command=goBack)
    back_button.image = back_img
    back_button.place(x=10, y=10)

    heading = tk.Label(pages[pageNo], fg="white", bg="#3E3B3C", font="Arial 20 bold", pady=10)
    heading.pack()

    content = tk.Frame(pages[pageNo], bg="#3E3B3C", pady=20)
    content.pack(expand="true", fill="both")

    left_frame = tk.Frame(content, bg="#3E3B3C")
    left_frame.grid(row=0, column=0, sticky="nsew")

    right_frame = tk.LabelFrame(content, text="Detected Criminals", bg="#3E3B3C", font="Arial 20 bold", bd=4,
                                foreground="#2ea3ef", labelanchor="n")
    right_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    content.grid_columnconfigure(0, weight=1, uniform="group1")
    content.grid_columnconfigure(1, weight=1, uniform="group1")
    content.grid_rowconfigure(0, weight=1)

def openPrepareFacebankWindow():
    subprocess.run(["python", "prep_facebank.py"])

def getPage3():
    subprocess.run(["python", "infer_on_video.py"])

def selectvideo1():
    subprocess.run(["python", "attendance.py"])

def getPage1():
    subprocess.run(["python", "student.py"])

def getPage2():
    subprocess.run(["python", "inferio.py"])

######################################## Home Page ####################################
tk.Label(pages[0], text="FACIAL RECOGNITION ATTENDANCE SYSTEM", fg="white", bg="black",
         font="Arial 25 bold", pady=30).pack(fill='x')

img = Image.open(r"C:\Users\Uzi\Downloads\Facial-Recognition-for-Crime-Detection-master\Facial-Recognition-for-Crime-Detection-master\img\ai_r.png")
img = img.resize((512, 403), Image.LANCZOS)
img = ImageTk.PhotoImage(img)

main_frame = tk.Frame(pages[0], bg="#3E3B3C")
main_frame.pack(expand=True, fill='both', padx=20, pady=20)

img_label = tk.Label(main_frame, image=img, bg="#3E3B3C")
img_label.pack(side='left', padx=60, pady=20)

btn_frame = tk.Frame(main_frame, bg="#3E3B3C", pady=30)
btn_frame.pack(side='right', padx=60, pady=20, expand=True)

tk.Button(btn_frame, text="Attendance Records", command=selectvideo1).pack(pady=15)
tk.Button(btn_frame, text="Student Registration", command=getPage1).pack(pady=15)
tk.Button(btn_frame, text="Surveillance", command=getPage3).pack(pady=15)
tk.Button(btn_frame, text="Prepare Facebank", command=openPrepareFacebankWindow).pack(pady=15)

for btn in btn_frame.winfo_children():
    btn.configure(font="Arial 20", width=20, bg="#000000", fg="white",
                  pady=15, bd=0, highlightthickness=0, activebackground="#3E3B3C", activeforeground="white")

settings_img = Image.open("data/settingxx.png")
settings_img = settings_img.resize((70, 70), Image.LANCZOS)
settings_img = ImageTk.PhotoImage(settings_img)

settings_button = tk.Button(pages[0], image=settings_img, bg="black", bd=0, highlightthickness=0,
                            activebackground="black", command=open_settings_window)
settings_button.image = settings_img
settings_button.place(relx=0.90, rely=0.02, anchor='ne')

help_img = Image.open(r"data\HELPBUTTON65.png")
help_img = help_img.resize((80, 80), Image.LANCZOS)
help_img = ImageTk.PhotoImage(help_img)

help_button = tk.Button(pages[0], image=help_img, bg="black", bd=0, highlightthickness=0,
                        activebackground="black", command=open_help_window)
help_button.image = help_img
help_button.place(relx=0.97, rely=0.014, anchor='ne')

pages[0].lift()
root.mainloop()
