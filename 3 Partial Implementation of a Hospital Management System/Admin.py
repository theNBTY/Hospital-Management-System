from Doctor import Doctor
from Patient import Patient

class Admin:
    """A class that deals with the Admin operations"""
    def __init__(self, username, password, postcode=""):
        self.__username = username
        self.__password = password
        self.__postcode =  postcode

    def view(self, a_list):
        for index, item in enumerate(a_list):
            print(f"{index+1:3}|{item}")

    def login(self, username=None, password=None, mode="GUI"):
        """
        Handles login for both GUI and Terminal-based inputs.

        Args:
            username (str, optional): Username for GUI mode.
            password (str, optional): Password for GUI mode.
            mode (str): Determines whether login is 'GUI' or 'Terminal'.

        Returns:
            bool: True if login is successful, False otherwise.
        """
        # GUI Mode - Use parameters directly
        if mode.upper() == "GUI":
            return self.__username == username and self.__password == password

        # Terminal Mode - Interactive input
        elif mode.upper() == "TERMINAL":
            print("-----Login-----")
            username = input("Enter the username: ").strip()
            password = input("Enter the password: ").strip()

            if self.__username == username and self.__password == password:
                print("Login successful!")
                return True
            else:
                print("Incorrect credentials. Try again.")
                return False

        # Invalid Mode
        else:
            raise ValueError("Invalid mode! Choose either 'GUI' or 'Terminal'")

    @property                           #controlled access to username and pass
    def username(self):                 #avoids making mroe headache
        return self.__username

    @property
    def password(self):
        return self.__password


    def find_index(self, index, lst):
        if index in range(0, len(lst)):
            return True
        else:
            return False

    def get_doctor_details(self):
        print("-----Add Doctor Details-----")
        first_name = input("Enter the doctor's first name: ").strip()
        surname = input("Enter the doctor's surname: ").strip()
        speciality = input("Enter the doctor's speciality: ").strip()
        return first_name, surname, speciality

    def get_patient_details(self):
        print("-----Add Patient Details-----")
        first_name = input("Enter the patient's first name: ").strip()
        surname = input("Enter the patient's surname: ").strip()
        age = int(input("Enter the patient's age: "))
        mobile = input("Enter the patient's mobile number: ").strip()
        postcode = input("Enter the patient's postcode: ").strip()
        return first_name, surname, age, mobile, postcode

    def doctor_management(self, doctors):
        op = input("-----Doctor Management-----\nChoose the operation:\n[1] - Register\n[2] - View\n[3] - Update\n[4] - Delete\nInput: ")

        if op == "1":
            print("-----Register-----")
            first_name, surname, speciality = self.get_doctor_details()
            for doctor in doctors:
                if first_name == doctor.get_first_name() and surname == doctor.get_surname():
                    print("Name already exists.")
                    return
            doctors.append(Doctor(first_name, surname, speciality))
            print("Doctor registered.")

        elif op == "2":
            print("-----List of Doctors-----")
            self.view(doctors)

        elif op == "3":
            while True:
                print("-----Update Doctor's Details-----")
                print("ID |          Full name           |  Speciality")
                self.view(doctors)
                try:
                    index = int(input("Enter the ID of the doctor: ")) - 1
                    if self.find_index(index, doctors):
                        break
                    else:
                        print("Doctor not found")
                except ValueError:
                    print("The ID entered is incorrect")

            field = int(input("Choose the field to be updated:\n[1] First name\n[2] Surname\n[3] Speciality\nInput: "))

            if field == 1:
                doctors[index].set_first_name(input("Enter new first name: ").strip())
            elif field == 2:
                doctors[index].set_surname(input("Enter new surname: ").strip())
            elif field == 3:
                doctors[index].set_speciality(input("Enter new speciality: ").strip())
            else:
                print("Invalid option.")

        elif op == "4":
            print("-----Delete Doctor-----")
            self.view(doctors)
            try:
                index = int(input("Enter the ID of the doctor to be deleted: ")) - 1
                if self.find_index(index, doctors):
                    doctors.pop(index)
                    print("Doctor deleted.")
                else:
                    print("Invalid ID.")
            except ValueError:
                print("Invalid input.")

        else:
            print("Invalid operation chosen. Check your spelling!")

    def patient_management(self, patients):
        op = input("-----Patient Management-----\nChoose the operation:\n[1] - Register\n[2] - View\n[3] - Delete\nInput: ")

        if op == "1":
            print("-----Register-----")
            first_name, surname, age, mobile, postcode = self.get_patient_details()
            patients.append(Patient(first_name, surname, age, mobile, postcode))
            print("Patient registered.")

        elif op == "2":
            print("-----List of Patients-----")
            self.view(patients)

        elif op == "3":
            print("-----Delete Patient-----")
            self.view(patients)
            try:
                index = int(input("Enter the ID of the patient to be deleted: ")) - 1
                if self.find_index(index, patients):
                    patients.pop(index)
                    print("Patient deleted.")
                else:
                    print("Invalid ID.")
            except ValueError:
                print("Invalid input.")

        else:
            print("Invalid operation chosen. Check your spelling!")

    def assign_doctor_to_patient(self, patients, doctors):
        print("-----Assign-----")
        self.view(patients)
        try:
            patient_index = int(input("Please enter the patient ID: ")) - 1
            if patient_index not in range(len(patients)):
                print("The id entered was not found.")
                return
        except ValueError:
            print("The id entered is incorrect")
            return

        print("-----Doctors Select-----")
        patients[patient_index].print_symptoms()
        self.view(doctors)

        try:
            doctor_index = int(input("Please enter the doctor ID: ")) - 1
            if self.find_index(doctor_index, doctors):
                patients[patient_index].link(doctors[doctor_index].full_name())
                print("The patient is now assigned to the doctor.")
            else:
                print("The id entered was not found.")
        except ValueError:
            print("The id entered is incorrect")

    def view_discharge(self, discharged_patients):
        print("-----Discharged Patients-----")
        self.view(discharged_patients)

    def update_details(self):
        op = int(input("Choose the field to be updated:\n[1] Username\n[2] Password\nInput: "))

        if op == 1:
            self.__username = input("Enter the new username: ")
        elif op == 2:
            password = input("Enter the new password: ")
            if password == input("Enter the new password again: "):
                self.__password = password
        else:
            print("Invalid option.")
