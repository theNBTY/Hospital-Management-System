class Patient:
    """Represents a Patient in the system."""

    def __init__(self, first_name, surname, age, mobile, postcode, symptoms, appointment="N/A"):
        """
        Args:
            first_name (str): The patient's first name. req
            surname (str): The patient's surname. req
            age (int): The patient's age. req
            mobile (str): The patient's mobile number. req
            postcode (str): The patient's postcode. req
            symptoms (str): A description of the patient's symptoms. req
            appointment (str): Appointment slot (default to nothing).
        """
        self.__first_name = first_name
        self.__surname = surname
        self.__age = age
        self.__mobile = mobile
        self.__postcode = postcode
        self.__doctor = "None"
        self.__symptoms = symptoms
        self.__appointment = appointment

    # Getters
    def get_first_name(self):
        return self.__first_name

    def get_surname(self):
        return self.__surname


    def get_age(self):
        return self.__age

    def get_mobile(self):
        return self.__mobile

    def get_postcode(self):
        return self.__postcode

    def get_doctor(self):
        return self.__doctor

    def get_symptoms(self):
        return self.__symptoms

    def get_appointment(self):
        return self.__appointment
    
    def full_name(self):
        return f"{self.__first_name} {self.__surname}"
    
    def get_illness_category(self):
        symptoms = self.get_symptoms().lower()
        # Ideas for category dictionary from
        # https://www.nhsinform.scot/illnesses-and-conditions/
        categories = {
            'Flu': ['cough', 'fever', 'chills', 'body ache', 'sore throat'],
            'Injury': ['pain', 'swelling', 'bruising', 'fracture', 'sprain'],
            'Allergy': ['rash', 'itching', 'hives', 'watery eyes', 'sneezing'],
            'Cardiovascular Issues': ['chest pain', 'shortness of breath', 'palpitations', 'high blood pressure', 'fatigue'],
            'Blood Disorders': ['anemia', 'fatigue', 'unusual bruising', 'bleeding', 'pale skin'],
            'Gastrointestinal Issues': ['nausea', 'vomiting', 'diarrhea', 'stomach pain', 'constipation'],
            'Neurological Issues': ['headache', 'dizziness', 'seizures', 'numbness', 'weakness'],
            'Respiratory Issues': ['wheezing', 'shortness of breath', 'coughing up blood', 'chest tightness'],
            'Psychological Issues': ['anxiety', 'depression', 'insomnia', 'mood swings', 'stress'],
            'Skin Issues': ['acne', 'eczema', 'dry skin', 'skin discoloration', 'lesions'],
            'Other': []
        }

        # matching symptoms to categories
        for category, associated_symptoms in categories.items():
            for symptom in associated_symptoms:
                if symptom in symptoms:
                    return category

        # Default
        return 'Other'

    # Setters
    def link(self, doctor):
        self.__doctor = doctor

    def set_symptoms(self, symptoms):
        self.__symptoms = symptoms

    def set_appointment(self, time_slot):
        self.__appointment = time_slot

    def __str__(self):
        """
        Returns a formatted string representation of the patient.

        Useful for debugging and terminal display.
        """
        return (
            f'{self.full_name():^30}|{self.__doctor:^30}|{self.__age:^5}|'
            f'{self.__mobile:^15}|{self.__postcode:^10}|{self.__appointment:^20}'
        )
