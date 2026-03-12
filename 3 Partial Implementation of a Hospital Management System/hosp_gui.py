import tkinter as tk
from tkinter import messagebox
import os
import json
from datetime import datetime
from Admin import Admin
from Doctor import Doctor
from Patient import Patient

class HospitalGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("500x400")

        # The OG actors
        self.default_admin = Admin("admin", "123")
        self.default_doctors = [
            Doctor("John", "Smith", "Internal Med.", []),
            Doctor("Jone", "Smith", "Pediatrics", []),
            Doctor("Jone", "Carlos", "Cardiology", []),
        ]
        self.default_patients = [
            Patient("Sara", "Smith", 20, "07012345678", "B1 234", "High Temperature", "2025-01-01"),
            Patient("Mike", "Jones", 37, "07555551234", "L2 2AB", "Headaches and Nausea", "2025-01-02"),
            Patient("David", "Smith", 15, "07123456789", "C1 ABC", "High blood pressure", "2025-01-03"),
        ]
        self.discharged_patients = []
        self.initialise_files()
        self.load_data()
        self.current_patient_index = 0
        # Login screen to start
        self.login_screen()

    def initialise_files(self):
        """Ensure all necessary files are initialised with default data if missing or empty."""
        if not os.path.exists("admin.json") or os.stat("admin.json").st_size == 0:
            with open("admin.json", "w") as file:
                json.dump({"username": self.default_admin.username, "password": self.default_admin.password}, file)

        if not os.path.exists("doctors.json") or os.stat("doctors.json").st_size == 0:
            with open("doctors.json", "w") as file:
                doctors_data = [
                    {
                        "first_name": d.get_first_name(),
                        "last_name": d.get_surname(),
                        "speciality": d.get_speciality(),
                        "appointments_count": len(d.get_appointments())
                    }
                    for d in self.default_doctors
                ]
                json.dump(doctors_data, file)

        if not os.path.exists("patients.json") or os.stat("patients.json").st_size == 0:
            with open("patients.json", "w") as file:
                patients_data = [
                    {
                        "first_name": p.get_first_name(),
                        "last_name": p.get_surname(),
                        "age": p.get_age(),
                        "mobile": p.get_mobile(),
                        "postcode": p.get_postcode(),
                        "symptoms": p.get_symptoms(),
                        "appointment": p.get_appointment(),
                        "assigned_doctor": p.get_doctor() if hasattr(p, 'get_doctor') else "N/A"
                    }
                    for p in self.default_patients
                ]
                json.dump(patients_data, file)

        if not os.path.exists("discharged_patients.json") or os.stat("discharged_patients.json").st_size == 0:
            with open("discharged_patients.json", "w") as file:
                json.dump([], file)

        if not os.path.exists("management_report.json") or os.stat("management_report.json").st_size == 0:
            with open("management_report.json", "w") as file:
                json.dump({}, file)


    def load_data(self):
        """Load data from JSON files."""
        try:
            #  Load cred
            with open("admin.json", "r") as file:
                admin_data = json.load(file)
                self.admin = Admin(admin_data["username"], admin_data["password"])
        except FileNotFoundError:
            self.admin = Admin("admin", "123")  # original credentials
            self.save_admin_data()

        try:
            #  Loading docs
            with open("doctors.json", "r") as file:
                doctors_data = json.load(file)
                self.doctors = [
                    Doctor(
                        d["first_name"],
                        d["last_name"],
                        d["speciality"],
                        appointments=[None] * d.get("appointments_count", 0)  # make list for the number of appts
                    )
                    for d in doctors_data
                ]
        except FileNotFoundError:
            self.doctors = []
            self.save_doctors_data()

        self.load_patients_data()

        try:
            #  Load discharged patients
            with open("discharged_patients.json", "r") as file:
                discharged_data = json.load(file)
                self.discharged_patients = [
                    Patient(p["first_name"], p["last_name"], p["age"], p["mobile"], p["postcode"], p["symptoms"], p.get("appointment", "N/A"))
                    for p in discharged_data
                ]
        except FileNotFoundError:
            self.discharged_patients = []
            self.save_discharged_patients_data()

# Saving data into json
    def save_admin_data(self):
        """Save admin data to JSON."""
        with open("admin.json", "w") as file:
            json.dump({"username": self.admin.username, "password": self.admin.password}, file)

    def save_doctors_data(self):
        """Save doctor data to JSON."""
        with open("doctors.json", "w") as file:
            doctors_data = [{"first_name": d.get_first_name(), "last_name": d.get_surname(), "speciality": d.get_speciality(), "appointments_count": len(d.get_appointments())} for d in self.doctors]
            json.dump(doctors_data, file, indent = 4)

    def save_patients_data(self):
        """Saves patient data directly into JSON."""
        try:
            data = []
            for patient in self.patients:
                data.append({
                    "first_name": patient.get_first_name(),
                    "last_name": patient.get_surname(),
                    "age": patient.get_age(),
                    "mobile": patient.get_mobile(),
                    "postcode": patient.get_postcode(),
                    "symptoms": patient.get_symptoms(),
                    "appointment": patient.get_appointment(),
                    "assigned_doctor": patient.get_doctor()
                })

            with open("patients.json", "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save patient data: {str(e)}")

    def save_discharged_patients_data(self):
        """Save discharged patients data to JSON."""
        with open("discharged_patients.json", "w") as file:
            discharged_data = [
                {
                    "first_name": p.get_first_name(),
                    "last_name": p.get_surname(),
                    "age": p.get_age(),
                    "mobile": p.get_mobile(),
                    "postcode": p.get_postcode(),
                    "symptoms": p.get_symptoms(),
                    "appointment": p.get_appointment()
                }
                for p in self.discharged_patients
            ]
            json.dump(discharged_data, file)

    def load_patients_data(self):
        """Loads patient data from JSON."""
        try:
            with open("patients.json", "r") as file:
                data = json.load(file)

                self.patients = [
                    Patient(
                        patient["first_name"],
                        patient["last_name"],
                        patient["age"],
                        patient["mobile"],
                        patient["postcode"],
                        patient["symptoms"],
                        patient.get("appointment", "N/A")
                    )
                    for patient in data
                ]
        except FileNotFoundError:
            self.patients = []
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load patient data: {str(e)}")


    def report(self):
        """Generate and display a management report containing system statistics."""
        try:
            #  Loading required data
            with open("doctors.json", "r") as file:
                doctors_data = json.load(file)

            with open("patients.json", "r") as file:
                patients_data = json.load(file)

            # Initialise report structure
            report = {
                "total_doctors": len(doctors_data),
                "total_patients": len(patients_data),
                "patients_per_doctor": {},
                "appointments_per_month_per_doctor": {},
                "patients_per_illness": {}
            }

            # doctor stats
            for doctor in doctors_data:
                doctor_name = f"{doctor['first_name']} {doctor['last_name']}"
                report["patients_per_doctor"][doctor_name] = 0
                report["appointments_per_month_per_doctor"][doctor_name] = {}

            # patient stats
            for patient in patients_data:
                assigned_doctor = patient.get("assigned_doctor", "N/A")
                illness = patient.get("symptoms", "Unknown")

                # track p/d
                if assigned_doctor in report["patients_per_doctor"]:
                    report["patients_per_doctor"][assigned_doctor] += 1

                # track illness types & num
                if illness not in report["patients_per_illness"]:
                    report["patients_per_illness"][illness] = 0
                report["patients_per_illness"][illness] += 1

                # Count appointments per month per doctor
                appointment = patient.get("appointment", "N/A")
                if appointment != "N/A":
                    try:
                        date_part = appointment.split(' ')[0]  # Extract date (dd-mm-yyyy)
                        month_year = '-'.join(date_part.split('-')[1:])  # Extract month-year (mm-yyyy)
                        if assigned_doctor in report["appointments_per_month_per_doctor"]:
                            if month_year not in report["appointments_per_month_per_doctor"][assigned_doctor]:
                                report["appointments_per_month_per_doctor"][assigned_doctor][month_year] = 0
                            report["appointments_per_month_per_doctor"][assigned_doctor][month_year] += 1
                    except (IndexError, ValueError):
                        continue

            # Save report to a JSON file
            with open("management_report.json", "w") as file:
                json.dump(report, file, indent=4)

            # Disp the report in a new GUI window
            self.disp_report(report)  # Pass the generated report to the display method
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to generate report: {str(e)}")

    def login_screen(self):
        self.clear_frame()
        self.root.geometry("325x225")

        # frame to hold all the widgets
        frm_login = tk.Frame(self.root)
        frm_login.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame within the window

        # widgets
        tk.Label(frm_login, text = "Login", font=("Helvetica", 23, "bold")).grid(row=0, column=0, columnspan=2, pady = 10)
        tk.Label(frm_login, text="Username:", font=("Arial", 12)).grid(row=1, column=0, padx  = 4, pady = 10, sticky="e")  # Align right
        self.username_entry = tk.Entry(frm_login, font=("Arial", 12))
        self.username_entry.grid(row=1, column=1, padx  = 10, pady = 10)
        tk.Label(frm_login, text="Password:", font=("Arial", 12)).grid(row=2, column=0, padx  = 4, pady = 10, sticky="e")  # Align right
        self.password_entry = tk.Entry(frm_login, show="*", font=("Arial", 12))
        self.password_entry.grid(row=2, column=1, padx  = 10, pady = 10)
        tk.Button(frm_login, text="Login",  command =  self.admin_login, width =  10, font=("Arial", 12)).grid(row=3, column=0, columnspan=2, pady = 30)

    def admin_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.admin.login(username, password):
            self.main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def main_menu(self):
        self.clear_frame()
        self.root.geometry("500x400")

        # Frame for assets
        main_frame = tk.Frame(self.root)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")  # Centering v3 (frame within the window)

        tk.Label(main_frame, text = "Main Menu", font=("Helvetica", 23, "bold")).grid(row=0, column=0, columnspan=2, pady = 25)

        tk.Button(main_frame, text = "Manage Doctors", font=("Arial", 12),  command =  self.manage_doctors, width =  20).grid(row=1, column=0, pady = 10, padx  = 15)
        tk.Button(main_frame, text="Manage Patients", font=("Arial", 12),  command =  self.view_patients, width =  20).grid(row=1, column=1, pady = 10, padx  = 15)

        tk.Button(main_frame, text = "View Patient Families", font = ("Arial", 12), command = self.view_fam, width = 20).grid(row = 2, column = 0, pady = 10, padx  = 15)
        tk.Button(main_frame, text= "Assign Doctor to Patient", font=("Arial", 12),  command =  self.assign_doctor, width =  20).grid(row=2, column=1, pady = 10, padx  = 15)

        tk.Button(main_frame, text ="Discharge Patient", font=("Arial", 12),  command =  self.discharge_patient, width =  20).grid(row=3, column=0, pady = 10, padx  = 15)
        tk.Button(main_frame, text ="Update Admin Details", font=("Arial", 12),  command =  self.update_admin_page, width =  20).grid(row=3, column=1, pady = 15, padx  = 15)

        tk.Button(main_frame, text= "View Report", font=("Arial", 12),  command =  self.report, width = 20).grid(row=4, column=0, pady = 10, padx  = 15)
        tk.Button(main_frame, text ="View Discharged Patients", font=("Arial", 12),  command =  self.view_discharged_patients, width =  20).grid(row=4, column=1, pady = 10, padx  = 15)

        tk.Button(main_frame, text = "Exit", font=("Arial", 12),  command =  self.root.quit, bg="#fa969d", fg="white", width = 10).grid(row=5, column=0, columnspan=2, pady = 30)

    def update_admin_page(self):
        # Clearing existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root, text = "Update Admin Details", font=("Helvetica", 23)).pack(pady = 10)

        tk.Label(self.root, text = "New Username", font=("Arial", 10)).pack(pady = 5)
        username_entry = tk.Entry(self.root, font=("Arial", 10))
        username_entry.pack(pady = 5)

        # Password Label & entry
        tk.Label(self.root, text = "New Password", font=("Arial", 10)).pack(pady = 5)
        password_entry = tk.Entry(self.root, font=("Arial", 10), show="*")
        password_entry.pack(pady = 5)
        tk.Button(self.root, text = "Update Details", font=("Arial", 10),  command =  lambda: self.update_admin_login(username_entry.get(), password_entry.get())).pack(pady = 10)

        tk.Button(self.root, text = "Back", font=("Arial", 10), bg="#fa969d", fg="white",  command =  self.main_menu).pack(pady = 5)

    def update_admin_login(self, username, password):
        admin_file = "admin.json"
        # Validate entries
        if not username or not password:
            messagebox.showerror("Error", "Both username & password are required.")
            return
        
        # Check
        if not os.path.exists(admin_file):
            messagebox.showerror("Error", "Admin file not found.")
            return
        
        try:
            # Read & update the admin file
            with open(admin_file, "r") as file:
                data = json.load(file)
            
            data["username"] = username
            data["password"] = password
            
            with open(admin_file, "w") as file:
                json.dump(data, file, indent=4)

            messagebox.showinfo("Success", "Admin details updated successfully.")
            self.main_menu()
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error reading admin file.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")


    def manage_doctors(self):
        """Manage & display doctors from doctors.json."""
        self.clear_frame()
        self.root.geometry("500x400")
        tk.Label(self.root, text = "Doctor Management", font=("Helvetica", 23, "bold")).pack(pady = 30)

        #  Loading data from doctors.json
        try:
            with open("doctors.json", "r") as file:
                doctors_data = json.load(file)
                self.doctors = [
                    Doctor(
                        d["first_name"],
                        d["last_name"],
                        d["speciality"],
                        appointments=d.get("appointments", [])
                    )
                    for d in doctors_data
                ]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load doctors: {str(e)}")
            return

        # Disp doctor details
        for index, doctor in enumerate(self.doctors):
            tk.Label(
            self.root,
            text = f"{index + 1}. {doctor.full_name()} - {doctor.get_speciality()} "
                 f"(Appointments: {len(doctor.get_appointments())})"
            ).pack()

        # Buttons for managing doctors
        tk.Button(self.root, text = "Add Doctor",  command =  self.add_doctor, width =  15).pack(pady = 5)
        tk.Button(self.root, text = "Delete Doctor",  command =  self.delete_doctor, width =  15).pack(pady = 5)
        tk.Button(self.root, text = "Back",  command =  self.main_menu, bg="#fa969d", fg="white", width =  10).pack(pady = 30)

    def add_doctor(self):
        """Add a new doctor & update doctors.json."""
        self.clear_frame()
        self.root.geometry("400x400")
        tk.Label(self.root, text = "Add Doctor", font=("Arial", 16)).pack(pady = 10)

        tk.Label(self.root, text = "First Name:").pack()
        first_name_entry = tk.Entry(self.root)
        first_name_entry.pack()

        tk.Label(self.root, text = "Last Name:").pack()
        last_name_entry = tk.Entry(self.root)
        last_name_entry.pack()

        tk.Label(self.root, text = "Specialty:").pack()
        speciality_entry = tk.Entry(self.root)
        speciality_entry.pack()

        def save_doctor():
            first_name = first_name_entry.get().strip()
            last_name = last_name_entry.get().strip()
            speciality = speciality_entry.get().strip()

            if not all([first_name, last_name, speciality]):
                messagebox.showerror("Error", "All fields are required!")
                return

            new_doctor = Doctor(first_name, last_name, speciality)
            self.doctors.append(new_doctor)
            self.save_doctors_data()  # Update the JSON file
            messagebox.showinfo("Success", "Doctor added successfully!")
            self.manage_doctors()

        tk.Button(self.root, text = "Save",  command =  save_doctor, width =  10).pack(pady = 10)
        tk.Button(self.root, text = "Back", bg="#fa969d", fg="white",  command =  self.manage_doctors, width =  10).pack(pady = 10)

    def delete_doctor(self):
        """Delete a doctor & update doctors.json."""
        self.clear_frame()
        self.root.geometry("400x400")
        tk.Label(self.root, text = "Delete Doctor", font=("Arial", 16)).pack(pady = 10)

        # Ensure `self.doctors` is up to date
        doctor_list = [f"{index + 1}. {doctor.full_name()}" for index, doctor in enumerate(self.doctors)]
        if not doctor_list:
            messagebox.showinfo("Info", "No doctors available to delete.")
            self.manage_doctors()
            return

        self.selected_doctor = tk.StringVar(self.root)
        tk.OptionMenu(self.root, self.selected_doctor, *doctor_list).pack(pady = 10)

        def remove_doctor():
            try:
                selected_index = int(self.selected_doctor.get().split('.')[0]) - 1
                self.doctors.pop(selected_index)
                self.save_doctors_data()  # Update the JSON file
                messagebox.showinfo("Success", "Doctor removed successfully!")
                self.manage_doctors()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove doctor: {str(e)}")

        tk.Button(self.root, text = "Delete",  command =  remove_doctor, width =  10).pack(pady = 10)
        tk.Button(self.root, text = "Back", bg="#fa969d", fg="white",  command =  self.manage_doctors, width =  10).pack(pady = 10)

    def view_patients(self):
        self.clear_frame()
        self.root.geometry("500x400")
        tk.Label(self.root, text = "Patients", font=("Helvetica", 23, "bold")).pack(pady = 30)

        self.show_patient_details()

        tk.Button(self.root, text = "<",  command =  self.previous_patient, width =  5).pack(side=tk.LEFT, padx  = 20)
        tk.Button(self.root, text = ">",  command =  self.next_patient, width =  5).pack(side=tk.RIGHT, padx  = 20)
        tk.Button(self.root, text = "Add Patient",  command =  self.add_patient, width =  10).pack(pady = 10)
        tk.Button(self.root, text = "Back",  command =  self.main_menu, bg="#fa969d", fg="white", width =  10).pack(pady = 30)

    def show_patient_details(self):
        if not self.patients:
            tk.Label(self.root, text = "No patients available").pack()
            return

        patient = self.patients[self.current_patient_index]
        assigned_doctor = patient.get_doctor() if hasattr(patient, 'get_doctor') else "N/A"
        if not assigned_doctor:
            assigned_doctor = "N/A"

        tk.Label(self.root, text = f"{self.current_patient_index+1}. {patient.full_name()}, {patient.get_age()} yrs - Doctor: {assigned_doctor}").pack()
        tk.Label(self.root, text = f"Symptoms: {patient.get_symptoms()}").pack()
        tk.Label(self.root, text = f"Appointment: {patient.get_appointment()}").pack()

    # Side pointing buttons
    def next_patient(self):
        if self.current_patient_index < len(self.patients) - 1:
            self.current_patient_index += 1
            self.view_patients()

    def previous_patient(self):
        if self.current_patient_index > 0:
            self.current_patient_index -= 1
            self.view_patients()

    def add_patient(self):
        self.clear_frame()
        self.root.geometry("500x500")
        tk.Label(self.root, text = "Add New Patient", font=("Helvetica", 23, "bold")).pack(pady = 30)

        tk.Label(self.root, text = "First Name:").pack(pady = 2)
        first_name_entry = tk.Entry(self.root)
        first_name_entry.pack(pady = 2)


        tk.Label(self.root, text = "Surname:").pack(pady = 2)
        surname_entry = tk.Entry(self.root)
        surname_entry.pack(pady = 2)


        tk.Label(self.root, text = "Age:").pack(pady = 2)
        age_entry = tk.Entry(self.root)
        age_entry.pack(pady = 2)

        tk.Label(self.root, text = "Mobile:").pack(pady = 2)
        mobile_entry = tk.Entry(self.root)
        mobile_entry.pack(pady = 2)

        tk.Label(self.root, text = "Postcode:").pack(pady = 2)
        postcode_entry = tk.Entry(self.root)
        postcode_entry.pack(pady = 2)

        tk.Label(self.root, text = "Symptoms:").pack(pady = 2)
        symptoms_entry = tk.Entry(self.root)
        symptoms_entry.pack(pady = 2)

        def save_patient():
            try:
                first_name = first_name_entry.get().strip()
                surname = surname_entry.get().strip()
                age = age_entry.get().strip()
                mobile = mobile_entry.get().strip()

                postcode = postcode_entry.get().strip()
                symptoms = symptoms_entry.get().strip()


                if not all([first_name, surname, age, mobile, postcode, symptoms]):
                    raise ValueError("All fields are required.")

                if not age.isdigit():
                    raise ValueError("Age must be a number.")

                age = int(age)
                # Add validation & JSON update
                new_patient = Patient(first_name, surname, age, mobile, postcode, symptoms)
                new_patient.set_symptoms(symptoms)
                self.patients.append(new_patient)
                self.save_patients_data()
                messagebox.showinfo("Success", "Patient added successfully!")
                self.view_patients()

            except ValueError as ve:
                messagebox.showerror("Error", str(ve))
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

        tk.Button(self.root, text = "Save",  command =  save_patient, width =  10).pack(pady = 10)
        tk.Button(self.root, text = "Back", bg="#fa969d", fg="white",  command =  self.view_patients, width =  10).pack(pady = 10)


    def assign_doctor(self):
        self.clear_frame()
        self.root.geometry("500x500")
        tk.Label(self.root, text = "Assign Doctor", font=("Helvetica", 23, "bold")).pack(pady = 30)

        # temp store values
        self.selected_patient = tk.StringVar(self.root)
        self.selected_doctor = tk.StringVar(self.root)
        self.selected_time = tk.StringVar(self.root)
        self.selected_date = tk.StringVar(self.root)

        # choosing patie
        tk.Label(self.root, text = "Select Patient:").pack()
        patients_list = [f"{index + 1}. {patient.full_name()}" for index, patient in enumerate(self.patients)]
        if patients_list:
            self.selected_patient.set(patients_list[0])  # first patient
            tk.OptionMenu(self.root, self.selected_patient, *patients_list).pack(pady = 10)

        # choose doc
        tk.Label(self.root, text = "Select Doctor:").pack()
        doctors_list = [f"{index + 1}. {doctor}" for index, doctor in enumerate(self.doctors)]
        if doctors_list:
            self.selected_doctor.set(doctors_list[0])  # first doctor
            tk.OptionMenu(self.root, self.selected_doctor, *doctors_list).pack(pady = 10)

        # Time slot selection
        tk.Label(self.root, text = "Select Time Slot:").pack()
        time_slots = ["12.00pm", "2.00pm", "4.00pm", "6.00pm"]
        self.selected_time.set(time_slots[0])  # first time slot
        tk.OptionMenu(self.root, self.selected_time, *time_slots).pack(pady = 10)

        # Date input
        tk.Label(self.root, text = "Select Date (dd-mm-yy):").pack()
        current_date = datetime.now().strftime("%d-%m-%y")
        self.date_entry = tk.Entry(self.root, textvariable=self.selected_date, width =  15)
        self.date_entry.insert(0, current_date)  # set date
        self.date_entry.pack(pady = 10)

        tk.Button(self.root, text = "Assign",  command =  self.assign_doctor_to_patient, width =  10).pack(pady = 30)
        tk.Button(self.root, text="Back", bg="#fa969d", fg="white",  command =  self.main_menu, width =  10).pack(pady = 30)

    def assign_doctor_to_patient(self):
        try:
            # index of selected patient & doctor
            patient_index = int(self.selected_patient.get().split('.')[0]) - 1
            doctor_index = int(self.selected_doctor.get().split('.')[0]) - 1
            time_slot = self.selected_time.get()
            date_slot = self.selected_date.get()

            # Validate inputs
            if not time_slot or not date_slot or patient_index < 0 or doctor_index < 0:
                raise ValueError("Please fill in all fields and select valid options.")

            # Validate date format
            try:
                appointment_date = datetime.strptime(date_slot, "%d-%m-%y").strftime("%d-%m-%Y")
            except ValueError:
                tk.messagebox.showerror("Error", "Invalid date format! Use dd-mm-yy.")
                return

            # Get patient and doctor objects
            selected_patient = self.patients[patient_index]
            selected_doctor = self.doctors[doctor_index]

            # Handling old doc appt decrement
            old_doctor_name = selected_patient.get_doctor()
            if old_doctor_name != "None":
                with open("doctors.json", "r") as file:
                    doctors_data = json.load(file)
                old_doctor_index = next(
                    (index for index, doctor in enumerate(self.doctors) if doctor.full_name() == old_doctor_name),
                    None
                )
                if old_doctor_index is not None:
                    doctors_data[old_doctor_index]["appointments_count"] -= 1
                with open("doctors.json", "w") as file:
                    json.dump(doctors_data, file, indent=4)

            # Assign new doc and update patient det
            selected_patient.link(selected_doctor.full_name())
            selected_patient.set_appointment(f"{appointment_date} at {time_slot}")
            selected_doctor.add_appointment(appointment_date, time_slot)

            # Update doctor and patient JSON files
            with open("doctors.json", "r") as file:
                doctors_data = json.load(file)
            doctors_data[doctor_index]["appointments_count"] = selected_doctor.get_appointments_count()
            with open("doctors.json", "w") as file:
                json.dump(doctors_data, file, indent=4)

            with open("patients.json", "r") as file:
                patients_data = json.load(file)
            patients_data[patient_index]["assigned_doctor"] = selected_doctor.full_name()
            patients_data[patient_index]["appointment"] = f"{appointment_date} at {time_slot}"
            with open("patients.json", "w") as file:
                json.dump(patients_data, file, indent=4)

            # Success msg and return to main
            tk.messagebox.showinfo("Success", "Doctor assigned, date, and time slot booked successfully!")
            self.main_menu()

        except Exception as e:
            tk.messagebox.showerror("Error", str(e))


    def discharge_patient(self):
        self.clear_frame()
        self.root.geometry("500x400")
        tk.Label(self.root, text = "Discharge Patients", font=("Helvetica", 23, "bold")).pack(pady = 30)

        self.selected_patient = tk.StringVar(self.root)

        if self.patients:
            patients_list = [f"{index+1}. {patient.full_name()}" for index, patient in enumerate(self.patients)]
            self.selected_patient.set(patients_list[0])  # Set default selection
            self.dropdown = tk.OptionMenu(self.root, self.selected_patient, *patients_list)
            self.dropdown.pack(pady=10)

            tk.Button(self.root, text = "Discharge",  command =  self.process_discharge, width =  20).pack(pady = 30)
        else:
            tk.Label(self.root, text ="No patients to discharge.", font=("Helvetica", 14)).pack(pady = 30)

        tk.Button(self.root, text ="Back", bg="#fa969d", fg="white",  command =  self.main_menu, width =  10).pack(pady = 30)

    def process_discharge(self):
        try:
            # Extract the selected patient index
            patient_index = int(self.selected_patient.get().split('.')[0]) - 1
            discharged_patient = self.patients.pop(patient_index)
            assigned_doctor_name = discharged_patient.get_doctor

            # Update doctor's appointment count
            for doctor in self.doctors:
                if doctor.full_name() == assigned_doctor_name:
                    doctor.get_appointments_count = max(0, doctor.get_appointments_count - 1)
                    break

            # Update doctor data in JSON file
            with open("doctors.json", "r") as file:
                doctors_data = json.load(file)

            for doctor in doctors_data:
                full_name = f"{doctor['first_name']} {doctor['last_name']}"
                if full_name == assigned_doctor_name:
                    doctor['appointments_count'] = max(0, doctor['appointments_count'] - 1)
                    break

            with open("doctors.json", "w") as file:
                json.dump(doctors_data, file, indent=4)

            # Add to discharged patients and save changes
            self.discharged_patients.append(discharged_patient)
            self.save_patients_data()
            self.save_discharged_patients_data()

            messagebox.showinfo("Success", "Patient discharged successfully!")
            self.discharge_patient()  # Refresh the GUI

        except Exception as error:
            messagebox.showerror("Error", f"An error occurred: {error}")



    def view_discharged_patients(self):
        self.clear_frame()
        self.root.geometry("500x400")
        tk.Label(self.root, text="Discharged Patients", font=("Helvetica", 23, "bold")).pack(pady = 30)

        for index, patient in enumerate(self.discharged_patients):
            tk.Label(self.root, text=f"{index+1}. {patient.full_name()}, Doc: {patient.get_doctor()}, Issue: {patient.get_illness_category()}").pack()

        tk.Button(self.root, text="Back", bg="#fa969d", fg="white",  command =  self.main_menu, width =  10).pack(pady = 30)

    def disp_report(self, report):
        """Display the report"""
        report_window = tk.Toplevel(self.root)
        report_window.title("Management Report")
        report_window.geometry("400x630")

        tk.Label(report_window, text="Management Report", font=("Arial", 16, "bold")).pack(pady = 10)

        tk.Label(report_window, text=f"Total Doctors: {report['total_doctors']}", font=("Arial", 12)).pack(anchor="w", padx  = 20, pady = 5)
        tk.Label(report_window, text = f"Total Patients: {report['total_patients']}", font=("Arial", 12)).pack(anchor="w", padx  = 20, pady = 5)

        tk.Label(report_window, text = "Patients Per Doctor:", font=("Arial", 12, "underline")).pack(anchor="w", padx  = 20, pady = 5)
        for doctor, count in report["patients_per_doctor"].items():
            tk.Label(report_window, text = f"  {doctor}: {count}", font=("Arial", 12)).pack(anchor="w", padx  = 40)

        tk.Label(report_window, text = "Appointments Per Month Per Doctor:", font=("Arial", 12, "underline")).pack(anchor ="w", padx  = 20, pady = 5)
        for doctor, months in report["appointments_per_month_per_doctor"].items():
            tk.Label(report_window, text = f"  {doctor}:", font=("Arial", 12)).pack(anchor = "w", padx  = 40)
            for month, count in months.items():
                tk.Label(report_window, text = f"    {month}: {count}", font=("Arial", 12)).pack(anchor ="w", padx  = 60)

        tk.Label(report_window, text = "Patients Per Illness:", font=("Arial", 12, "underline")).pack(anchor="w", padx  = 20, pady = 5)
        for illness, count in report["patients_per_illness"].items():
            tk.Label(report_window, text = f"  {illness}: {count}", font=("Arial", 12)).pack(anchor= "w", padx  = 40)

        tk.Button(report_window, text = "Back", bg="#fa969d", fg="white", font=("Arial", 12), command =  report_window.destroy, width =  10).pack(pady = 30)


    def view_fam(self):
        self.clear_frame()
        self.root.geometry("500x400")
        tk.Label(self.root, text = "Grouped Family by Dupe Postcodes", font=("Helvetica", 23, "bold")).pack(pady = 20)

        fam = {}

        for patient in self.patients:
            postcode = patient.get_postcode() if hasattr(patient, "get_postcode") else "unknown"
            if postcode not in fam:
                fam[postcode] = []
            fam[postcode].append(patient)

        for postcode, members in fam.items():
            tk.Label(self.root, text =f"Address (Postcode): {postcode}", font = ("Arial", 16, "underline")).pack(pady = 5)
            for index, member in enumerate(members):
                tk.Label(self.root, text = f"  {index + 1}. {member.full_name()}, {member.get_age()} yrs - Symptoms: {member.get_symptoms()}").pack(anchor = "w", padx = 20)
        
        tk.Button(self.root, text = "Back",  command =  self.main_menu, bg="#fa969d", fg="white", width =  10).pack(pady = 30)
    
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":

    root = tk.Tk()
    app = HospitalGUI(root)
    root.mainloop()
