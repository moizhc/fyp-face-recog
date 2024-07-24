import csv
import os
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from tkcalendar import Calendar, DateEntry
from datetime import datetime

# Global variable for importCsv Function 
mydata = []

class Attendance:

    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Attendance Records")

        # -----------Variables-------------------
        self.var_name = StringVar()
        self.var_id = StringVar()
        self.var_gender = StringVar()
        self.var_degree = StringVar()
        self.var_dep = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_date_time = StringVar()
        self.var_date_select = StringVar()

        # Color Theme
        self.bg_color = "#3E3B3C"
        self.btn_bg_color = "#000000"
        self.primary_text_color = "#ffffff"
        self.secondary_text_color = "#2ea3ef"
        self.btn_active_bg_color = "#3E3B3C"
        self.btn_active_fg_color = "#ffffff"

        # Title Section
        title_lb1 = Label(self.root, text="Attendance Panel", font=("verdana", 30, "bold"), bg="black", fg=self.primary_text_color)
        title_lb1.place(x=0, y=0, width=1366, height=60)

        # Main Frame
        main_frame = Frame(self.root, bd=2, bg=self.bg_color)
        main_frame.place(x=5, y=65, width=1355, height=690)

        # Left Frame
        left_frame = LabelFrame(main_frame, bd=2, bg=self.bg_color, relief=RIDGE, text="Student Details",
                                font=("verdana", 12, "bold"), fg=self.secondary_text_color)
        left_frame.place(x=10, y=10, width=660, height=670)

        # Labels and Entries
        labels = ["Name", "ID", "Gender", "Degree", "Department", "Year", "Semester", "Date and Time"]
        variables = [self.var_name, self.var_id, self.var_gender, self.var_degree, self.var_dep, self.var_year, self.var_semester, self.var_date_time]

        for i, (label, var) in enumerate(zip(labels, variables)):
            lbl = Label(left_frame, text=f"{label}:", font=("verdana", 12, "bold"), fg=self.primary_text_color, bg=self.bg_color)
            lbl.grid(row=i*2, column=0, padx=10, pady=5, sticky=W)

            entry = ttk.Entry(left_frame, textvariable=var, width=20, font=("verdana", 12, "bold"))
            entry.grid(row=i*2+1, column=0, padx=10, pady=5, sticky=W)

        # Buttons Frame
        btn_frame = Frame(left_frame, bd=2, bg=self.bg_color, relief=RIDGE)
        btn_frame.place(x=10, y=565, width=645, height=60)

        Button(btn_frame, command=self.importCsv, text="Import CSV", width=12, font=("verdana", 12, "bold"), fg=self.primary_text_color, bg=self.btn_bg_color,
               activebackground=self.btn_active_bg_color, activeforeground=self.btn_active_fg_color).grid(row=0, column=0, padx=10, pady=10)

        Button(btn_frame, command=self.update_csv, text="Update", width=12, font=("verdana", 12, "bold"), fg=self.primary_text_color, bg=self.btn_bg_color,
               activebackground=self.btn_active_bg_color, activeforeground=self.btn_active_fg_color).grid(row=0, column=1, padx=10, pady=10)

        Button(btn_frame, command=self.delete_data, text="Delete", width=12, font=("verdana", 12, "bold"), fg=self.primary_text_color, bg=self.btn_bg_color,
               activebackground=self.btn_active_bg_color, activeforeground=self.btn_active_fg_color).grid(row=0, column=2, padx=10, pady=10)

        Button(btn_frame, command=self.reset_data, text="Reset", width=12, font=("verdana", 12, "bold"), fg=self.primary_text_color, bg=self.btn_bg_color,
               activebackground=self.btn_active_bg_color, activeforeground=self.btn_active_fg_color).grid(row=0, column=3, padx=10, pady=10)

        # Right Frame
        right_frame = LabelFrame(main_frame, bd=2, bg=self.bg_color, relief=RIDGE, text="Attendance Details",
                                 font=("verdana", 12, "bold"), fg=self.secondary_text_color)
        right_frame.place(x=680, y=10, width=660, height=670)

        # Date selection button and label
        date_label = Label(right_frame, text="Select Date:", font=("verdana", 12, "bold"), fg=self.primary_text_color, bg=self.bg_color)
        date_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        self.date_entry = DateEntry(right_frame, width=15, font=("verdana", 12, "bold"), background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        Button(right_frame, command=self.load_date_data, text="Load Data", width=12, font=("verdana", 12, "bold"), fg=self.primary_text_color, bg=self.btn_bg_color,
               activebackground=self.btn_active_bg_color, activeforeground=self.btn_active_fg_color).grid(row=0, column=2, padx=10, pady=10)

        # Table Frame
        table_frame = Frame(right_frame, bd=2, bg=self.bg_color, relief=RIDGE)
        table_frame.place(x=10, y=50, width=635, height=580)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.attendanceReport = ttk.Treeview(table_frame, column=("Name", "ID", "Gender", "Degree", "Department", "Year", "Semester", "Date and Time"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.attendanceReport.xview)
        scroll_y.config(command=self.attendanceReport.yview)

        for col in self.attendanceReport["columns"]:
            self.attendanceReport.heading(col, text=col)
            self.attendanceReport.column(col, width=150)

        self.attendanceReport["show"] = "headings"
        self.attendanceReport.pack(fill=BOTH, expand=1)
        self.attendanceReport.bind("<ButtonRelease>", self.get_cursor_right)

        self.load_dates()
        self.load_date_data(None)

    def update_csv(self):
        if self.var_name.get() == "" or self.var_id.get() == "" or self.var_gender.get() == "" or self.var_degree.get() == "" or self.var_dep.get() == "" or self.var_year.get() == "" or self.var_semester.get() == "" or self.var_date_time.get() == "":
            messagebox.showerror("Error", "Please Fill All Fields are Required!", parent=self.root)
        else:
            try:
                date_str = self.var_date_time.get().split(' ')[0]
                csv_filename = self.get_attendance_file_path(date_str)
                rows = []
                if os.path.exists(csv_filename):
                    with open(csv_filename, 'r') as file:
                        reader = csv.reader(file)
                        for row in reader:
                            if len(row) > 0 and row[1] == self.var_id.get():
                                rows.append([self.var_name.get(), self.var_id.get(), self.var_gender.get(), self.var_degree.get(), self.var_dep.get(), self.var_year.get(), self.var_semester.get(), self.var_date_time.get()])
                            else:
                                rows.append(row)
                with open(csv_filename, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
                self.load_dates()
                self.load_date_data(None)
                messagebox.showinfo("Success", "Attendance Updated Successfully!", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)

    def delete_data(self):
        if self.var_id.get() == "":
            messagebox.showerror("Error", "Student Id Must be Required!", parent=self.root)
        else:
            try:
                date_str = self.var_date_time.get().split(' ')[0]
                csv_filename = self.get_attendance_file_path(date_str)
                rows = []
                if os.path.exists(csv_filename):
                    with open(csv_filename, 'r') as file:
                        reader = csv.reader(file)
                        for row in reader:
                            if len(row) > 0 and row[1] != self.var_id.get():
                                rows.append(row)
                with open(csv_filename, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
                self.load_dates()
                self.load_date_data(None)
                messagebox.showinfo("Success", "Attendance Deleted Successfully!", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)

    def get_attendance_file_path(self, date_str):
        directory = 'data/Attendance Sheets'
        if not os.path.exists(directory):
            os.makedirs(directory)
        return os.path.join(directory, f'{date_str}.csv')

    def load_dates(self):
        dates = set()
        directory = 'data/Attendance Sheets'
        if not os.path.exists(directory):
            os.makedirs(directory)
        for filename in os.listdir(directory):
            if filename.endswith('.csv'):
                date_str = filename.replace('.csv', '')
                dates.add(date_str)
        dates = sorted(dates, reverse=True)
        if dates:
            self.var_date_select.set(dates[0])

    def load_date_data(self, event=None):
        selected_date = self.date_entry.get_date().strftime('%Y-%m-%d')
        csv_filename = self.get_attendance_file_path(selected_date)
        if os.path.exists(csv_filename):
            with open(csv_filename, 'r') as file:
                reader = csv.reader(file)
                self.attendanceReport.delete(*self.attendanceReport.get_children())
                for row in reader:
                    if len(row) > 0 and row[0] != "Name":  # Skip header row
                        self.attendanceReport.insert("", END, values=row)
        else:
            self.attendanceReport.delete(*self.attendanceReport.get_children())
            messagebox.showerror("Error", f"No attendance record found for {selected_date}", parent=self.root)

    def reset_data(self):
        self.var_name.set("")
        self.var_id.set("")
        self.var_gender.set("")
        self.var_degree.set("")
        self.var_dep.set("")
        self.var_year.set("")
        self.var_semester.set("")
        self.var_date_time.set("")

    def fetchData(self, rows):
        global mydata
        mydata = rows
        self.attendanceReport.delete(*self.attendanceReport.get_children())
        for i in rows:
            self.attendanceReport.insert("", END, values=i)

    def importCsv(self):
        mydata.clear()
        fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open CSV", filetypes=(("CSV File", "*.csv"), ("All File", "*.*")), parent=self.root)
        with open(fln) as myfile:
            csvread = csv.reader(myfile, delimiter=",")
            for i in csvread:
                mydata.append(i)
        self.fetchData(mydata)
        self.load_dates()
        self.load_date_data(None)

    def get_cursor_right(self, event=""):
        cursor_focus = self.attendanceReport.focus()
        content = self.attendanceReport.item(cursor_focus)
        data = content["values"]

        self.var_name.set(data[0])
        self.var_id.set(data[1])
        self.var_gender.set(data[2])
        self.var_degree.set(data[3])
        self.var_dep.set(data[4])
        self.var_year.set(data[5])
        self.var_semester.set(data[6])
        self.var_date_time.set(data[7])

    def action(self):
        if self.var_name.get() == "" or self.var_id.get() == "" or self.var_gender.get() == "" or self.var_degree.get() == "" or self.var_dep.get() == "" or self.var_year.get() == "" or self.var_semester.get() == "" or self.var_date_time.get() == "":
            messagebox.showerror("Error", "Please Fill All Fields are Required!", parent=self.root)
        else:
            try:
                date_str = self.var_date_time.get().split(' ')[0]
                csv_filename = self.get_attendance_file_path(date_str)
                if not os.path.exists(csv_filename):
                    with open(csv_filename, 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(["Name", "ID", "Gender", "Degree", "Department", "Year", "Semester", "Date and Time"])
                with open(csv_filename, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([self.var_name.get(), self.var_id.get(), self.var_gender.get(), self.var_degree.get(), self.var_dep.get(), self.var_year.get(), self.var_semester.get(), self.var_date_time.get()])
                self.load_dates()
                self.load_date_data(None)
                messagebox.showinfo("Success", "Attendance Added Successfully!", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = Attendance(root)
    root.mainloop()
