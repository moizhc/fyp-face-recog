# import modules

from tkinter import *
from PIL import Image, ImageTk
import os
import subprocess

# Designing window for registration

def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    # Get screen dimensions
    screen_width = 1366
    screen_height = 768
    register_screen.geometry(f"{screen_width}x{screen_height}+0+0")



    
    register_screen.configure(bg="#3E3B3C")

    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()


    Label(register_screen,text="Please enter details below", bg="black", fg="white", width="300", height="2", font=("Calibri", 13)).pack()
    Label(register_screen,text="", bg="#3E3B3C").pack()

    
    username_label = Label(register_screen, text="Username * ", bg="#3E3B3C", fg="white", font=("Arial", 12))
    username_label.pack()
    username_entry = Entry(register_screen, textvariable=username, font=("Arial", 12))
    username_entry.pack()
    password_label = Label(register_screen, text="Password * ", bg="#3E3B3C", fg="white", font=("Arial", 12))
    password_label.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*', font=("Arial", 12))
    password_entry.pack()
    Label(register_screen, text="", bg="#3E3B3C").pack()
    Button(register_screen, text="Register", width=10, height=1, bg="#000000", fg="white", command=register_user).pack()


# Designing window for login 

def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    
    screen_width = 1366
    screen_height = 768
    login_screen.geometry(f"{screen_width}x{screen_height}+0+0")
    login_screen.configure(bg="#3E3B3C")



    Label(login_screen,text="Please enter details below to login", bg="black", fg="white", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="", bg="#3E3B3C").pack()

    #Label(login_screen, text="Please enter details below to login", bg="#3E3B3C", fg="white", font=("Arial", 16)).pack(pady=20)

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    form_frame = Frame(login_screen, bg="#3E3B3C")
    form_frame.pack(pady=10, padx=10)

    Label(form_frame, text="Username   ", bg="#3E3B3C", fg="white", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky=E)
    username_login_entry = Entry(form_frame, textvariable=username_verify, font=("Arial", 12))
    username_login_entry.grid(row=0, column=1, padx=10, pady=10)

    Label(form_frame, text="Password   ", bg="#3E3B3C", fg="white", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky=E)
    password_login_entry = Entry(form_frame, textvariable=password_verify, show='*', font=("Arial", 12))
    password_login_entry.grid(row=1, column=1, padx=10, pady=10)

    button_frame = Frame(login_screen, bg="#3E3B3C")
    button_frame.pack(pady=20)

    Button(button_frame, text="Login", width=10, height=1, bg="#000000", fg="white", font=("Arial", 12), command=login_verify).grid(row=0, column=0, padx=10)
    Button(button_frame, text="Cancel", width=10, height=1, bg="#000000", fg="white", font=("Arial", 12), command=login_screen.destroy).grid(row=0, column=1, padx=10)



# Implementing event on register button

def register_user():
    username_info = username.get()
    password_info = password.get()

    file = open(username_info, "w")
    file.write(username_info + "\n")
    file.write(password_info)
    file.close()

    username_entry.delete(0, END)
    password_entry.delete(0, END)

    Label(register_screen, text="Registration Success", fg="green", bg="#3E3B3C", font=("calibri", 11)).pack()


# Implementing event on login button 

def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    list_of_files = os.listdir()
    if username1 in list_of_files:
        file1 = open(username1, "r")
        verify = file1.read().splitlines()
        if password1 in verify:
            login_success()
        else:
            password_not_recognised()
    else:
        user_not_found()


# Designing popup for login success

def login_success():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    # Get screen dimensions
    screen_width = 1366
    screen_height = 768
    login_success_screen.geometry(f"{screen_width}x{screen_height}+0+0")
    
    login_success_screen.configure(bg="#3E3B3C")
    
    Label(login_success_screen, text="LOGIN SUCCESS", bg="black", fg="white", width="300", height="2", font=("Calibri", 13)).pack(pady=20)
    Label(login_success_screen, text="", bg="#3E3B3C").pack()

    button_frame = Frame(login_success_screen, bg="#3E3B3C")
    button_frame.pack(expand=True)

    Button(button_frame, text="OK", width=10, height=1, bg="black", fg="white", font=("Arial", 12), command=delete_login_success).pack(pady=20)

# Designing popup for invalid password

def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Error")
    password_not_recog_screen.geometry("150x100")
    password_not_recog_screen.configure(bg="#3E3B3C")
    Label(password_not_recog_screen, text="Invalid Password", bg="#3E3B3C", fg="white").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()

# Designing popup for user not found

def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Error")
    user_not_found_screen.geometry("150x100")
    user_not_found_screen.configure(bg="#3E3B3C")
    Label(user_not_found_screen, text="User Not Found", bg="#3E3B3C", fg="white").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()

# Deleting popups

def delete_login_success():
    login_success_screen.destroy()
    subprocess.call(['python', 'home.py'])

def delete_password_not_recognised():
    password_not_recog_screen.destroy()

def delete_user_not_found_screen():
    user_not_found_screen.destroy()

# Designing Main(first) window

def main_account_screen():
    global main_screen
    main_screen = Tk()
    screen_width = 1366
    screen_height = 768
    main_screen.geometry(f"{screen_width}x{screen_height}+0+0")
    main_screen.title("FACIAL RECOGNITION ATTENDANCE SYSTEM")
    main_screen.configure(bg="#3E3B3C")

    Label(text="ADMIN LOGIN", bg="black", fg="white", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="", bg="#3E3B3C").pack()

    # Load and display the image
    img_path = r"C:\Users\Uzi\Downloads\Facial-Recognition-for-Crime-Detection-master\personn.png"
    img = Image.open(img_path)
    img = img.resize((150, 150), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    Label(main_screen, image=img, bg="#3E3B3C").pack()

    Label(text="", bg="#3E3B3C").pack()

    Button(text="Login", height="2", width="30", command=login).pack()
    Label(text="", bg="#3E3B3C").pack()
    Button(text="Register", height="2", width="30", command=register).pack()

    main_screen.mainloop()

main_account_screen()
