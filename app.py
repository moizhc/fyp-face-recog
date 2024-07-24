############################################# IMPORTING ################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2,os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
from retinaface.detect_class_hr import FaceDetector
from config import get_config
from face_aligner import FaceAligner
from Learner import face_learner
import argparse
from utils import load_facebank, draw_box_name, prepare_facebank
from mtcnn import MTCNN
import torch
import torchvision
from model import l2_norm
from torchvision import transforms as trans

############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

##################################################################################

def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200,tick)

###################################################################################

def contact():
    mess._show(title='Contact us', message="Please contact us on : 'xxxxxxxxxxxxx@gmail.com' ")

###################################################################################

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some file missing', message='Please contact us for help')
        window.destroy()

###################################################################################

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("TrainingImageLabel\psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()

###################################################################################

def change_pass():
    global master
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False,False)
    master.title("Change Password")
    master.configure(background="white")
    lbl4 = tk.Label(master,text='    Enter Old Password',bg='white',font=('times', 12, ' bold '))
    lbl4.place(x=10,y=10)
    global old
    old=tk.Entry(master,width=25 ,fg="black",relief='solid',font=('times', 12, ' bold '),show='*')
    old.place(x=180,y=10)
    lbl5 = tk.Label(master, text='   Enter New Password', bg='white', font=('times', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="black",relief='solid', font=('times', 12, ' bold '),show='*')
    new.place(x=180, y=45)
    lbl6 = tk.Label(master, text='Confirm New Password', bg='white', font=('times', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid',font=('times', 12, ' bold '),show='*')
    nnew.place(x=180, y=80)
    cancel=tk.Button(master,text="Cancel", command=master.destroy ,fg="black"  ,bg="red" ,height=1,width=25 , activebackground = "white" ,font=('times', 10, ' bold '))
    cancel.place(x=200, y=120)
    save1 = tk.Button(master, text="Save", command=save_pass, fg="black", bg="#3ece48", height = 1,width=25, activebackground="white", font=('times', 10, ' bold '))
    save1.place(x=10, y=120)
    master.mainloop()

#####################################################################################

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == key):
        TrainImages(conf=get_config())
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')

######################################################################################

def clear():
    txt.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

#######################################################################################

def TakeImages():
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("StudentDetails/StudentDetails.csv")
    if exists:
        with open("StudentDetails/StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial += 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("StudentDetails/StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()

    Id = (txt.get())
    name = (txt2.get())
    if (name.isalpha() or (' ' in name)):
        cam = cv2.VideoCapture(r'videos/CAM2_MUNAM_ABDULLAH/balaj_mir_front_cam2.mp4')
        detector = FaceDetector()  # Initialize the RetinaFace detector
        sampleNum = 0
        while True:
            ret, img = cam.read()
            if not ret:
                break
            
            landmarks, bbox, prob = detector.detect_landmarks(img)
            
            for (box, confidence) in zip(bbox, prob):
                x, y, w, h = box[0], box[1], box[2] - box[0], box[3] - box[1]
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum += 1
                gray_face = cv2.cvtColor(img[y:y + h, x:x + w], cv2.COLOR_BGR2GRAY)
                cv2.imwrite(f"TrainingImage/{name}.{serial}.{Id}.{sampleNum}.jpg", gray_face)
                cv2.imshow('Taking Images', img)
            
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum > 100:
                break
        
        cam.release()
        cv2.destroyAllWindows()
        res = f"Images Taken for ID : {Id}"
        row = [serial, '', Id, '', name]
        with open('StudentDetails/StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
    else:
        res = "Enter Correct name"
        message.configure(text=res)

########################################################################################

detector = FaceDetector()
rface = FaceAligner(detector.detect_landmarks, desiredFaceWidth=112, desiredFaceHeight=112)

def getImagesAndLabels(path, detector_name):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    faceSamples = []
    ids = []
    detector = detector_name

    for imagePath in imagePaths:
        img = Image.open(imagePath).convert('RGB')
        id = int(os.path.split(imagePath)[-1].split(".")[1])

        # Detect faces
        faces, _ = rface.align_multi(img)

        # Assuming the first detected face is the target
        if faces is not None and len(faces) > 0:
            face = faces[0]
            faceSamples.append(face)
            ids.append(id)

    return faceSamples, ids

def TrainImages(conf):
    def assure_path_exists(path):
        if not os.path.exists(path):
            os.makedirs(path)

    assure_path_exists("TrainingImageLabel/")

    # Load images and labels
    faces, ids = getImagesAndLabels("TrainingImage", conf.detector_name)

    if len(faces) == 0:
        print('Please Register someone first!!!')
        return

    embeddings = []
    for face in faces:
        face_tensor = conf.test_transform(face).to(conf.device).unsqueeze(0)
        with torch.no_grad():
            embedding = conf.model_name(face_tensor)
        embeddings.append(embedding)

    embeddings = torch.cat(embeddings).cpu().detach().numpy()
    ids = np.array(ids)

    # Save the embeddings and IDs
    np.save("TrainingImageLabel/embeddings.npy", embeddings)
    np.save("TrainingImageLabel/ids.npy", ids)

    print("Profile Saved Successfully")
    print('Total Registrations till now:', len(ids))

def TrackImages(    conf,   tta=False):
    def assure_path_exists(path):
        if not os.path.exists(path):
            os.makedirs(path)

    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")

    # Load embeddings and IDs
    embeddings = np.load("TrainingImageLabel/embeddings.npy")
    ids = np.load("TrainingImageLabel/ids.npy")

    # Load student details
    student_details_path = "StudentDetails/StudentDetails.csv"
    if not os.path.isfile(student_details_path):
        print('Students details are missing, please check!')
        return
    
    df = pd.read_csv(student_details_path)

    cam = cv2.VideoCapture(r'videos/CAM2_MUNAM_ABDULLAH/balaj_mir_front_cam2.mp4')
    font = cv2.FONT_HERSHEY_SIMPLEX

    while True:
        ret, im = cam.read()
        if not ret:
            break

        faces, _ = conf.detector_name.detect(im)
        
        for face in faces:
            x, y, w, h = face['box']
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)

            face_img = Image.fromarray(im[y:y+h, x:x+w])
            face_tensor = conf.test_transform(face_img).to(conf.device).unsqueeze(0)

            with torch.no_grad():
                if tta:
                    mirror = trans.functional.hflip(face_img)
                    emb = conf.model_name(face_tensor)
                    emb_mirror = conf.model_name(conf.test_transform(mirror).to(conf.device).unsqueeze(0))
                    face_embedding = l2_norm(emb + emb_mirror)
                else:
                    face_embedding = conf.model_name(face_tensor)

            face_embedding = face_embedding.cpu().detach().numpy()

            distances = np.linalg.norm(embeddings - face_embedding, axis=1)
            min_distance = np.min(distances)
            min_index = np.argmin(distances)

            if min_distance < conf.threshold:
                serial = ids[min_index]
                ts = time.time()
                date = datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                name = df.loc[df['SERIAL NO.'] == serial]['NAME'].values[0]
                id_str = str(df.loc[df['SERIAL NO.'] == serial]['ID'].values[0])
                attendance = [id_str, '', name, '', date, '', timeStamp]
            else:
                name = 'Unknown'

            cv2.putText(im, name, (x, y + h), font, 1, (255, 255, 255), 2)

        cv2.imshow('Taking Attendance', im)
        if cv2.waitKey(1) == ord('q'):
            break

    ts = time.time()
    date = datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    attendance_path = f"Attendance/Attendance_{date}.csv"

    if os.path.isfile(attendance_path):
        with open(attendance_path, 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)
    else:
        with open(attendance_path, 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(['Id', '', 'Name', '', 'Date', '', 'Time'])
            writer.writerow(attendance)

    cam.release()
    cv2.destroyAllWindows()
######################################## USED STUFFS ############################################
    
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }

######################################## GUI FRONT-END ###########################################

window = tk.Tk()
window.geometry("1280x720")
window.resizable(True,False)
window.title("Attendance System")
window.configure(background='#262523')

frame1 = tk.Frame(window, bg="lightgray")
frame1.place(relx=0.11, rely=0.17, relwidth=0.39, relheight=0.80)

frame2 = tk.Frame(window, bg="lightgray")
frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)

message3 = tk.Label(window, text="Face Recognition Based Attendance System" ,fg="white",bg="#262523" ,width=55 ,height=1,font=('times', 29, ' bold '))
message3.place(x=10, y=10)

frame3 = tk.Frame(window, bg="lightgray")
frame3.place(relx=0.52, rely=0.09, relwidth=0.09, relheight=0.07)

frame4 = tk.Frame(window, bg="lightgray")
frame4.place(relx=0.36, rely=0.09, relwidth=0.16, relheight=0.07)

datef = tk.Label(frame4, text = day+"-"+mont[month]+"-"+year+"  |  ", fg="orange",bg="#262523" ,width=55 ,height=1,font=('times', 22, ' bold '))
datef.pack(fill='both',expand=1)

clock = tk.Label(frame3,fg="orange",bg="#262523" ,width=55 ,height=1,font=('times', 22, ' bold '))
clock.pack(fill='both',expand=1)
tick()

head2 = tk.Label(frame2, text="                       For New Registrations                       ", fg="black",bg="steelblue" ,font=('times', 17, ' bold ') )
head2.grid(row=0,column=0)

head1 = tk.Label(frame1, text="                       For Already Registered                       ", fg="black",bg="steelblue" ,font=('times', 17, ' bold ') )
head1.place(x=0,y=0)

lbl = tk.Label(frame2, text="Enter ID",width=20  ,height=1  ,fg="black"  ,bg="steelblue" ,font=('times', 17, ' bold ') )
lbl.place(x=80, y=55)

txt = tk.Entry(frame2,width=32 ,fg="black",font=('times', 15, ' bold '))
txt.place(x=30, y=88)

lbl2 = tk.Label(frame2, text="Enter Name",width=20  ,fg="black"  ,bg="steelblue" ,font=('times', 17, ' bold '))
lbl2.place(x=80, y=140)

txt2 = tk.Entry(frame2,width=32 ,fg="black",font=('times', 15, ' bold ')  )
txt2.place(x=30, y=173)

message1 = tk.Label(frame2, text="1)Take Images  >>>  2)Save Profile" ,bg="steelblue" ,fg="black"  ,width=39 ,height=1, activebackground = "yellow" ,font=('times', 15, ' bold '))
message1.place(x=7, y=230)

message = tk.Label(frame2, text="" ,bg="steelblue" ,fg="black"  ,width=39,height=1, activebackground = "yellow" ,font=('times', 16, ' bold '))
message.place(x=7, y=450)

lbl3 = tk.Label(frame1, text="Attendance",width=20  ,fg="black"  ,bg="steelblue"  ,height=1 ,font=('times', 17, ' bold '))
lbl3.place(x=100, y=115)

res=0
exists = os.path.isfile("StudentDetails\StudentDetails.csv")
if exists:
    with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2) - 1
    csvFile1.close()
else:
    res = 0
message.configure(text='Total Registrations till now  : '+str(res))

##################### MENUBAR #################################

menubar = tk.Menu(window,relief='ridge')
filemenu = tk.Menu(menubar,tearoff=0)
filemenu.add_command(label='Change Password', command = change_pass)
filemenu.add_command(label='Contact Us', command = contact)
filemenu.add_command(label='Exit',command = window.destroy)
menubar.add_cascade(label='Help',font=('times', 29, ' bold '),menu=filemenu)

################## TREEVIEW ATTENDANCE TABLE ####################

tv= ttk.Treeview(frame1,height =13,columns = ('name','date','time'))
tv.column('#0',width=82)
tv.column('name',width=130)
tv.column('date',width=133)
tv.column('time',width=133)
tv.grid(row=2,column=0,padx=(0,0),pady=(150,0),columnspan=4)
tv.heading('#0',text ='ID')
tv.heading('name',text ='NAME')
tv.heading('date',text ='DATE')
tv.heading('time',text ='TIME')

###################### SCROLLBAR ################################

scroll=ttk.Scrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)

###################### BUTTONS ##################################

clearButton = tk.Button(frame2, text="Clear", command=clear  ,fg="black"  ,bg="indianred"  ,width=11 ,activebackground = "white" ,font=('times', 11, ' bold '))
clearButton.place(x=335, y=86)
clearButton2 = tk.Button(frame2, text="Clear", command=clear2  ,fg="black"  ,bg="indianred"  ,width=11 , activebackground = "white" ,font=('times', 11, ' bold '))
clearButton2.place(x=335, y=172)    
takeImg = tk.Button(frame2, text="Take Images", command=TakeImages  ,fg="white"  ,bg="steelblue"  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
takeImg.place(x=30, y=300)
trainImg = tk.Button(frame2, text="Save Profile", command=psw ,fg="white"  ,bg="steelblue"  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
trainImg.place(x=30, y=380)
trackImg = tk.Button(frame1, text="Take Attendance", command=TrackImages  ,fg="black"  ,bg="cadetblue"  ,width=35  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
trackImg.place(x=30,y=50)
quitWindow = tk.Button(frame1, text="Quit", command=window.destroy  ,fg="black"  ,bg="indianred"  ,width=35 ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
quitWindow.place(x=30, y=450)

##################### END ######################################

window.configure(menu=menubar)
window.mainloop()

####################################################################################################
