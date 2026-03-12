class Doctor:
    """
    A class that deals with Doctor operations.
    """

    def __init__(self, first_name, surname, speciality, appointments=None):
        """
        Initialize a Doctor object.

        Args:
            first_name (str): First name of the doctor.
            surname (str): Surname of the doctor.
            speciality (str): Doctor's speciality.
            appointments (list, optional): List of appointments. Defaults to an empty list.
        """
        self.__first_name = first_name
        self.__surname = surname
        self.__speciality = speciality
        self.__appointments = appointments if appointments is not None else []

    def full_name(self):
        return f"{self.__first_name} {self.__surname}"

    def get_first_name(self):
        return self.__first_name

    def set_first_name(self, new_first_name):
        self.__first_name = new_first_name

    def get_surname(self):
        return self.__surname

    def set_surname(self, new_surname):
        self.__surname = new_surname

    def get_speciality(self):
        return self.__speciality

    def set_speciality(self, new_speciality):
        self.__speciality = new_speciality

    def get_appointments(self):
        return self.__appointments

    def add_appointment(self, date_slot, time_slot):
        self.__appointments.append((date_slot, time_slot))

    def remove_appointment(self, appointment):
        if appointment in self.__appointments:
            self.__appointments.remove(appointment)

    def get_appointments_count(self):
        return len(self.__appointments)
    
    def get_appointments_by_month(self, month): # counting appts in specific month with format mm-yyyy
        return sum(1 for date, _ in self.__appointments if date.split('-')[1] == month)


    def __str__(self):
        return f'{self.full_name():^20} | {self.__speciality:^15} | Appointments: {self.get_appointments_count():^15}'
