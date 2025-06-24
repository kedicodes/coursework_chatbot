import os
import sqlite3


from student_management import save_personal_details, view_programs_offered, save_education_details, save_progress, \
    get_progress, check_if_student_qualifies


# add student personal details and call on the save method to the db
def add_personal_details(user_id):
    print("Let's Add Your Personal Details:")

    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    date_of_birth = input("Enter your date of birth: ")
    identification_number = input("Enter your identification number: ")
    passport_number = input("Enter your passport number: ")
    gender = input("Enter your gender: ")
    contact_number = input("Enter your contact number: ")
    email = input("Enter your email address: ")
    physical_address = input("Enter your physical address: ")

    save_personal_details(user_id, first_name, last_name, date_of_birth, identification_number, passport_number,gender,contact_number, email, physical_address)
    print("Your personal details have been successfully saved!")

def add_education_details(user_id):
    connection = sqlite3.connect('thuto_ke_lesedi.db')
    cursor = connection.cursor()
    print("Let's Add Your Education Details:")

    school_level = input("Enter your school level (High School/Undergraduate/Postgraduate): ").strip().lower()
    if school_level == "high school":
        high_school_name = input("Enter your high school name (i.e Waterberg High School): ")
        view_programs_offered()
        average_achieved = input("Enter your overall average achieved (i.e 70%): ")
        save_education_details(user_id, high_school_name, average_achieved, school_level)
    else:
        university_name = input("Enter your university name (i.e University of Pretoria): ")
        view_programs_offered()
        average_achieved = float(input("Enter your overall average achieved (i.e 70%): "))
        save_education_details(user_id,university_name, average_achieved, school_level)

    # suggest the degree programs
    degree_suggestions = check_if_student_qualifies(average_achieved)
    print("Provided below are the degree suggestions based on your Achievements:")
    for degree_id in degree_suggestions:
       print(f"{degree_id}")

    chosen_degree_name = int(input("Please choose the Degree ID you would like to apply for (i.e 1): "))
    cursor.execute("SELECT DegreeID FROM DegreePrograms WHERE DegreeID = ?", (chosen_degree_name,))
    selected_degree_id = cursor.fetchone()

    if selected_degree_id:
        print(f" You have selected to apply for {selected_degree_id[0]}")
    print("Your education details have been successfully saved!")


def submit_university_application(user_id):
    print("Let's Submit Your University Application:")

    connection = sqlite3.connect('thuto_ke_lesedi.db')
    cursor = connection.cursor()

# check if everything has been filled out
    cursor.execute("SELECT IdDocument, ResultDocument FROM Students WHERE UserID = ?", (user_id, ))
    document = cursor.fetchone()
    if not document or any(doc is None for doc in document):
        print("Missing Required Documents! Please upload all required documents.")
        return

    print("Are you ready to submit your application?")
    print("1. Yes")
    print("2. No")
    submit = input("Are you ready to submit your application? (yes/no): ")
    if submit == "yes":
        cursor.execute("INSERT INTO ApplicationProgress (UserID, ApplicationStatus) VALUES (?, ?)", (user_id, 'Submitted'))
        connection.commit()
        print("Your application has been successfully submitted!")
    else:
        print("Application not submitted!")
        return
    connection.close()


def enrol_to_university(user_id):
    current_application_step = get_progress(user_id)
    print(f"Starting application at {current_application_step}")

    while current_application_step <= 4:
        if current_application_step == 1:
            add_personal_details(user_id)
            current_application_step += 1
            save_progress(user_id, current_application_step)
        elif current_application_step == 2:
            add_education_details(user_id)
            current_application_step += 1
            save_progress(user_id, current_application_step)
        elif current_application_step == 3:
            check_if_student_qualifies(current_application_step)
            current_application_step += 1
            save_progress(user_id, current_application_step)
        elif current_application_step == 4:
            submit_university_application(user_id)
            save_progress(user_id, None)
            print("Your application has been successfully submitted!")

   # if current_application_step is None:
    #     current_application_step = 1

    # if current_application_step is not None:
    #     current_application_step = int(current_application_step)
    # else:
    #     current_application_step = 1











