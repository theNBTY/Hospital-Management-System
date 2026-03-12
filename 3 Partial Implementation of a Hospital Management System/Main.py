# Imports
from Admin import Admin
from Doctor import Doctor
from Patient import Patient

# Main.py deemed redundant, my focus on GUI-based instead of terminal-based

# Main.py deemed redundant, my focus on GUI-based instead of terminal-based

# Main.py deemed redundant, my focus on GUI-based instead of terminal-based

# Main.py deemed redundant, my focus on GUI-based instead of terminal-based

# Main.py deemed redundant, my focus on GUI-based instead of terminal-based

# Main.py deemed redundant, my focus on GUI-based instead of terminal-based

# Main.py deemed redundant, my focus on GUI-based instead of terminal-based

# Main.py deemed redundant, my focus on GUI-based instead of terminal-based

# Main.py deemed redundant, my focus on GUI-based instead of terminal-based

# Main.py deemed redundant, my focus on GUI-based instead of terminal-based

# Main.py deemed redundant, my focus on GUI-based instead of terminal-based

# Main.py deemed redundant, my focus on GUI-based instead of terminal-based

# Main.py deemed redundant, my focus on GUI-based instead of terminal-based

def main():
    """
    the main function to be ran when the program runs
    """

    # actors
    admin = Admin("admin","123") # username is "admin", password is "123"
    doctors = [Doctor("John","Smith","Internal Med."), Doctor("Jone","Smith","Pediatrics"), Doctor("Jone","Carlos","Cardiology")]
    patients = [Patient("Sara","Smith", 20, "07012345678","B1 234"), Patient("Mike","Jones", 37,"07555551234","L2 2AB"), Patient("Daivd","Smith", 15, "07123456789","C1 ABC")]
    discharged_patients = []

    # keep trying to login till the login details are correct
    while True:
        if admin.login():
            running = True # allow the program to run
            break
        else:
            print("Incorrect username or password.")

    while running:
        # print the menu
        op = int(input("Choose the operation:\n[1] Register/view/update/delete doctor\n[2] View or discharge patients\n[3] View discharged patient\n[4] Assign doctor to a patient\n[5] Update admin details\n[6] Quit\nInput: "))

        if op == 1:
            # 1- Register/view/update/delete doctor
            admin.doctor_management(doctors)

        elif op == 2:
            # 2- View or discharge patients
            admin.view(patients)

            while True:
                op = int(input("Do you want to discharge a patient?\n[1] Yes\n[2] No\nInput: "))

                if op == 1:
                    admin.discharge(patients, discharged_patients)

                elif op == 2:
                    break

                # unexpected entry
                else:
                    print("Please answer with 1 or 2.")

        elif op == 3:
            # 3 - view discharged patients
            admin.view(discharged_patients)

        elif op == 4:
            # 4- Assign doctor to a patient
            admin.assign_doctor_to_patient(patients, doctors)

        elif op == 5:
            # 5- Update admin details
            admin.update_details()

        elif op == 6:
            # 6 - Quit
            print("Exiting program. Goodbye!")
            running = False

        else:
            # the user did not enter an option that exists in the menu
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
