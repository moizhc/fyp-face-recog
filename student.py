from tkinter import *
from tkinter import ttk, filedialog
from tkinter import messagebox
import csv
import os
import shutil

window_width = 1366
window_height = 768

class Student:
    def __init__(self, root):
        self.root = root
        """ screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = int(screen_width * 0.9)
        window_height = int(screen_height * 0.9)
        self.root.geometry(f"{window_width}x{window_height}+100+50") """
        self.root.geometry("1366x768+0+0")
        self.root.title("Student Registration")

        # -----------Variables-------------------
        self.var_dep = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_gender = StringVar()
        self.var_degree = StringVar()
        self.var_image_path = StringVar()

        # Color Theme
        self.bg_color = "#3E3B3C"
        self.btn_bg_color = "#000000"
        self.highlight_bg_color = "#202d42"
        self.primary_text_color = "#ffffff"
        self.secondary_text_color = "#2ea3ef"
        self.btn_active_bg_color = "#3E3B3C"
        self.btn_active_fg_color = "#ffffff"

        # title section
        title_lb1 = Label(self.root, text="Welcome to Student Registration", font=("verdana", 30, "bold"),
                          bg="black", fg=self.primary_text_color)
        title_lb1.place(x=0, y=0, width=window_width, height=65)

        # Creating Frame
        main_frame = Frame(self.root, bd=2, bg=self.btn_active_bg_color)
        main_frame.place(x=2, y=65, width=window_width - 10, height=window_height - 70)

        # Left Label Frame
        left_frame = LabelFrame(main_frame, bd=2, bg=self.bg_color, relief=RIDGE, text="Student Details",
                                font=("verdana", 12, "bold"), fg=self.secondary_text_color)
        left_frame.place(x=10, y=10, width=660, height=window_height - 80)

        # Current Course
        current_course_frame = LabelFrame(left_frame, bd=2, bg=self.bg_color, relief=RIDGE, text="Current Course",
                                          font=("verdana", 12, "bold"), fg=self.secondary_text_color)
        current_course_frame.place(x=10, y=5, width=635, height=230)

        # label Department
        dep_label = Label(current_course_frame, text="Department", font=("verdana", 12, "bold"), bg=self.bg_color,
                          fg=self.primary_text_color)
        dep_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)

        # combo box
        dep_combo = ttk.Combobox(current_course_frame, textvariable=self.var_dep, width=20, font=("verdana", 12, "bold"),
                                 state="readonly")
        dep_combo["values"] = ("Select Department", "BSCS", "BSEE", "BSENG", "BSPHY", "BSMATH")
        dep_combo.current(0)
        dep_combo.grid(row=1, column=0, padx=5, pady=5, sticky=W)

        # label Year
        year_label = Label(current_course_frame, text="Year", font=("verdana", 12, "bold"), bg=self.bg_color,
                           fg=self.primary_text_color)
        year_label.grid(row=2, column=0, padx=5, pady=5, sticky=W)

        # combo box
        year_combo = ttk.Combobox(current_course_frame, textvariable=self.var_year, width=20, font=("verdana", 12, "bold"),
                                  state="readonly")
        year_combo["values"] = ("Select Year", "2019-23", "2020-24", "2021-25", "2022-26", "2023-27")
        year_combo.current(0)
        year_combo.grid(row=3, column=0, padx=5, pady=5, sticky=W)

        # label Semester
        semester_label = Label(current_course_frame, text="Semester", font=("verdana", 12, "bold"), bg=self.bg_color,
                               fg=self.primary_text_color)
        semester_label.grid(row=4, column=0, padx=5, pady=5, sticky=W)

        # combo box
        semester_combo = ttk.Combobox(current_course_frame, textvariable=self.var_semester, width=20, font=("verdana", 12, "bold"),
                                      state="readonly")
        semester_combo["values"] = ("Select Semester", "Semester-1", "Semester-2", "Semester-3", "Semester-4", "Semester-5",
                                    "Semester-6", "Semester-7", "Semester-8")
        semester_combo.current(0)
        semester_combo.grid(row=5, column=0, padx=5, pady=5, sticky=W)

        # Class Student Information
        class_Student_frame = LabelFrame(left_frame, bd=2, bg=self.bg_color, relief=RIDGE, text="Class Student Information",
                                         font=("verdana", 12, "bold"), fg=self.secondary_text_color)
        class_Student_frame.place(x=10, y=240, width=635, height=350)

        # Student ID
        studentId_label = Label(class_Student_frame, text="Std-ID:", font=("verdana", 12, "bold"), fg=self.primary_text_color,
                                bg=self.bg_color)
        studentId_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)

        studentId_entry = ttk.Entry(class_Student_frame, textvariable=self.var_std_id, width=20, font=("verdana", 12, "bold"))
        studentId_entry.grid(row=1, column=0, padx=5, pady=5, sticky=W)

        # Student Name
        student_name_label = Label(class_Student_frame, text="Std-Name:", font=("verdana", 12, "bold"), fg=self.primary_text_color,
                                   bg=self.bg_color)
        student_name_label.grid(row=2, column=0, padx=5, pady=5, sticky=W)

        student_name_entry = ttk.Entry(class_Student_frame, textvariable=self.var_std_name, width=20, font=("verdana", 12, "bold"))
        student_name_entry.grid(row=3, column=0, padx=5, pady=5, sticky=W)

        # Gender
        student_gender_label = Label(class_Student_frame, text="Gender:", font=("verdana", 12, "bold"), fg=self.primary_text_color,
                                     bg=self.bg_color)
        student_gender_label.grid(row=4, column=0, padx=5, pady=5, sticky=W)

        # combo box
        gender_combo = ttk.Combobox(class_Student_frame, textvariable=self.var_gender, width=20, font=("verdana", 12, "bold"),
                                    state="readonly")
        gender_combo["values"] = ("Male", "Female", "Others")
        gender_combo.current(0)
        gender_combo.grid(row=5, column=0, padx=5, pady=5, sticky=W)

        # Degree
        degree_label = Label(class_Student_frame, text="Degree:", font=("verdana", 12, "bold"), fg=self.primary_text_color,
                             bg=self.bg_color)
        degree_label.grid(row=6, column=0, padx=5, pady=5, sticky=W)

        # combo box
        degree_combo = ttk.Combobox(class_Student_frame, textvariable=self.var_degree, width=20, font=("verdana", 12, "bold"),
                                    state="readonly")
        degree_combo["values"] = ("BS", "MS")
        degree_combo.current(0)
        degree_combo.grid(row=7, column=0, padx=5, pady=5, sticky=W)

        # Choose Image Button
        choose_img_btn = Button(class_Student_frame, command=self.choose_image, text="Choose Image", width=20,
                                font=("verdana", 12, "bold"), fg=self.primary_text_color, bg=self.btn_bg_color,
                                activebackground=self.btn_active_bg_color, activeforeground=self.btn_active_fg_color)
        choose_img_btn.grid(row=8, column=0, padx=5, pady=10, sticky=W)

        # Button Frame
        btn_frame = Frame(left_frame, bd=2, bg=self.bg_color, relief=RIDGE)
        btn_frame.place(x=10, y=600, width=635, height=60)

        # Save button
        save_btn = Button(btn_frame, command=self.add_data, text="Save", width=10, font=("verdana", 12, "bold"),
                          fg=self.primary_text_color, bg=self.btn_bg_color, activebackground=self.btn_active_bg_color,
                          activeforeground=self.btn_active_fg_color)
        save_btn.grid(row=0, column=0, padx=5, pady=10, sticky=W)

        # Update button
        update_btn = Button(btn_frame, command=self.update_data, text="Update", width=10, font=("verdana", 12, "bold"),
                            fg=self.primary_text_color, bg=self.btn_bg_color, activebackground=self.btn_active_bg_color,
                            activeforeground=self.btn_active_fg_color)
        update_btn.grid(row=0, column=1, padx=5, pady=8, sticky=W)

        # Delete button
        del_btn = Button(btn_frame, command=self.delete_data, text="Delete", width=10, font=("verdana", 12, "bold"),
                         fg=self.primary_text_color, bg=self.btn_bg_color, activebackground=self.btn_active_bg_color,
                         activeforeground=self.btn_active_fg_color)
        del_btn.grid(row=0, column=2, padx=5, pady=10, sticky=W)

        # Reset button
        reset_btn = Button(btn_frame, command=self.reset_data, text="Reset", width=10, font=("verdana", 12, "bold"),
                           fg=self.primary_text_color, bg=self.btn_bg_color, activebackground=self.btn_active_bg_color,
                           activeforeground=self.btn_active_fg_color)
        reset_btn.grid(row=0, column=3, padx=5, pady=10, sticky=W)

        # Right Label Frame
        right_frame = LabelFrame(main_frame, bd=2, bg=self.bg_color, relief=RIDGE, text="Student Details",
                                 font=("verdana", 12, "bold"), fg=self.secondary_text_color)
        right_frame.place(x=680, y=10, width=window_width - 700, height=window_height - 75)

        # Searching System in Right Label Frame
        search_frame = LabelFrame(right_frame, bd=2, bg=self.bg_color, relief=RIDGE, text="Search System",
                                  font=("verdana", 12, "bold"), fg=self.secondary_text_color)
        search_frame.place(x=10, y=5, width=650, height=80)

        # Search Label
        search_label = Label(search_frame, text="Search:", font=("verdana", 12, "bold"), fg=self.primary_text_color,
                             bg=self.bg_color)
        search_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.var_searchTX = StringVar()
        # combo box
        search_combo = ttk.Combobox(search_frame, textvariable=self.var_searchTX, width=10, font=("verdana", 12, "bold"),
                                    state="readonly")
        search_combo["values"] = ("Select", "Std-ID", "Name")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=5, pady=15, sticky=W)

        self.var_search = StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.var_search, width=15, font=("verdana", 12, "bold"))
        search_entry.grid(row=0, column=2, padx=5, pady=5, sticky=W)

        search_btn = Button(search_frame, command=self.search_data, text="Search", width=8, font=("verdana", 12, "bold"),
                            fg=self.primary_text_color, bg=self.btn_bg_color, activebackground=self.btn_active_bg_color,
                            activeforeground=self.btn_active_fg_color)
        search_btn.grid(row=0, column=3, padx=5, pady=10, sticky=W)

        showAll_btn = Button(search_frame, command=self.fetch_data, text="Show All", width=8, font=("verdana", 12, "bold"),
                             fg=self.primary_text_color, bg=self.btn_bg_color, activebackground=self.btn_active_bg_color,
                             activeforeground=self.btn_active_fg_color)
        showAll_btn.grid(row=0, column=4, padx=5, pady=10, sticky=W)

        # Table Frame
        table_frame = Frame(right_frame, bd=2, bg=self.bg_color, relief=RIDGE)
        table_frame.place(x=10, y=90, width=650, height=window_height - 250)

        # scroll bar
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL, style="TScrollbar")
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL, style="TScrollbar")

        # create table
        self.student_table = ttk.Treeview(table_frame,
                                          column=("ID", "Name", "Gender", "Degree", "Department", "Year", "Semester", "Photo"),
                                          xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("ID", text="StudentID")
        self.student_table.heading("Name", text="Name")
        self.student_table.heading("Gender", text="Gender")
        self.student_table.heading("Degree", text="Degree")
        self.student_table.heading("Department", text="Department")
        self.student_table.heading("Year", text="Year")
        self.student_table.heading("Semester", text="Semester")
        self.student_table.heading("Photo", text="PhotoSample")
        self.student_table["show"] = "headings"

        # Set Width of Columns
        self.student_table.column("ID", width=100)
        self.student_table.column("Name", width=100)
        self.student_table.column("Gender", width=100)
        self.student_table.column("Degree", width=100)
        self.student_table.column("Department", width=100)
        self.student_table.column("Year", width=100)
        self.student_table.column("Semester", width=100)
        self.student_table.column("Photo", width=100)

        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease>", self.get_cursor)
        self.fetch_data()

    # ==================Function Declarations==============================

    def add_data(self):
        if self.var_std_id.get() == "" or self.var_std_name.get() == "" or self.var_gender.get() == "" or self.var_degree.get() == "" or self.var_image_path.get() == "":
            messagebox.showerror("Error", "Please Fill All Fields are Required!", parent=self.root)
        else:
            try:
                # Check if the CSV file exists and create it with headers if it doesn't
                if not os.path.exists("student_data.csv"):
                    with open("student_data.csv", mode="w", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow([
                            "ID", "Name", "Gender", "Degree", "Department", "Year", "Semester", "Photo"
                        ])

                # Write the student data to the CSV file
                with open("student_data.csv", mode="a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        self.var_std_id.get(),
                        self.var_std_name.get(),
                        self.var_gender.get(),
                        self.var_degree.get(),
                        self.var_dep.get(),
                        self.var_year.get(),
                        self.var_semester.get(),
                        os.path.basename(self.var_image_path.get())
                    ])

                # Save the image file in the data/facebank directory under the student's name
                student_dir = os.path.join("data", "facebank", self.var_std_name.get())
                if not os.path.exists(student_dir):
                    os.makedirs(student_dir)
                shutil.copy(self.var_image_path.get(), os.path.join(student_dir, os.path.basename(self.var_image_path.get())))

                self.fetch_data()
                messagebox.showinfo("Success", "All Records are Saved!", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)

    # ===========================Fetch data from CSV to table ================================

    def fetch_data(self):
        if not os.path.exists("student_data.csv"):
            with open("student_data.csv", mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    "ID", "Name", "Gender", "Degree", "Department", "Year", "Semester", "Photo"
                ])
        with open("student_data.csv", mode="r") as file:
            reader = csv.reader(file)
            self.student_table.delete(*self.student_table.get_children())
            for row in reader:
                if row and row[0] != "ID":  # Skip header row
                    self.student_table.insert("", END, values=row)

    # ================================Get cursor function=======================

    def get_cursor(self, event=""):
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)
        data = content["values"]

        self.var_std_id.set(data[0])
        self.var_std_name.set(data[1])
        self.var_gender.set(data[2])
        self.var_degree.set(data[3])
        self.var_dep.set(data[4])
        self.var_year.set(data[5])
        self.var_semester.set(data[6])
        self.var_image_path.set(data[7])

    # ========================================Update Function==========================
    def update_data(self):
        if self.var_std_id.get() == "" or self.var_std_name.get() == "" or self.var_gender.get() == "" or self.var_degree.get() == "" or self.var_image_path.get() == "":
            messagebox.showerror("Error", "Please Fill All Fields are Required!", parent=self.root)
        else:
            try:
                updated = False
                rows = []
                with open("student_data.csv", mode="r") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row[0] == self.var_std_id.get():
                            rows.append([
                                self.var_std_id.get(),
                                self.var_std_name.get(),
                                self.var_gender.get(),
                                self.var_degree.get(),
                                self.var_dep.get(),
                                self.var_year.get(),
                                self.var_semester.get(),
                                os.path.basename(self.var_image_path.get())
                            ])
                            updated = True
                        else:
                            rows.append(row)

                with open("student_data.csv", mode="w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)

                if updated:
                    self.fetch_data()
                    messagebox.showinfo("Success", "Successfully Updated!", parent=self.root)
                else:
                    messagebox.showinfo("Error", "Record not found!", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)

    # ==============================Delete Function=========================================
    def delete_data(self):
        if self.var_std_id.get() == "":
            messagebox.showerror("Error", "Student Id Must be Required!", parent=self.root)
        else:
            try:
                delete = messagebox.askyesno("Delete", "Do you want to Delete?", parent=self.root)
                if delete:
                    rows = []
                    with open("student_data.csv", mode="r") as file:
                        reader = csv.reader(file)
                        for row in reader:
                            if row[0] != self.var_std_id.get():
                                rows.append(row)

                    with open("student_data.csv", mode="w", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerows(rows)

                    self.fetch_data()
                    messagebox.showinfo("Delete", "Successfully Deleted!", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)

    # Reset Function
    def reset_data(self):
        self.var_std_id.set("")
        self.var_std_name.set("")
        self.var_gender.set("")
        self.var_degree.set("Select Degree")
        self.var_dep.set("Select Department")
        self.var_year.set("Select Year")
        self.var_semester.set("Select Semester")
        self.var_image_path.set("")

    # ===========================Search Data===================
    def search_data(self):
        if self.var_search.get() == "" or self.var_searchTX.get() == "Select":
            messagebox.showerror("Error", "Select Combo option and enter entry box", parent=self.root)
        else:
            try:
                found = False
                with open("student_data.csv", mode="r") as file:
                    reader = csv.reader(file)
                    self.student_table.delete(*self.student_table.get_children())
                    for row in reader:
                        if (self.var_searchTX.get() == "Std-ID" and row[0] == self.var_search.get()) or \
                           (self.var_searchTX.get() == "Name" and row[1] == self.var_search.get()):
                            self.student_table.insert("", END, values=row)
                            found = True
                if not found:
                    messagebox.showinfo("Error", "Data Not Found", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due To :{str(es)}", parent=self.root)

    # =====================Choose Image Function=======================
    def choose_image(self):
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.var_image_path.set(file_path)


# main class object
if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()
