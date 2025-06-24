import sqlite3
from identity_management import get_user


# add degree programs manually into the database
def add_degree_programs():
    connection = sqlite3.connect('thuto_ke_lesedi.db')
    cursor = connection.cursor()

    degree_programs = [
        (1, 'BCom (Accounting Sciences)', 'Faculty of Economics and Management Sciences', 'Undergraduate', '3 years',
         75.00),
        (2, 'Bcom (Entrepreneurship & Business Management)', 'Faculty of Economics and Management Sciences',
         'Undergraduate', '3 years', 65.00),
        (3, 'Bcom (Economics)', 'Faculty of Economics and Management Sciences', 'Undergraduate', '3 years', 70.00),
        (4, 'Bcom (Marketing)', 'Faculty of Economics and Management Sciences', 'Undergraduate', '3 years', 65.00),
        (
        5, 'Bcom (Supply Chain Management)', 'Faculty of Economics and Management Sciences', 'Undergraduate', '3 years', 65.00),
        (6, 'Bcom Hons (Accounting Sciences)', 'Faculty of Economics and Management Sciences', 'Postgraduate', '1 year',65.00),
        (7, 'Bcom Hons (Entrepreneurship & Business Management)', 'Faculty of Economics and Management Sciences',
         'Postgraduate', '1 year', 65.00),
        (8, 'Bcom Hons (Economics)', 'Faculty of Economics and Management Sciences', 'Postgraduate', '1 year', 65.00),
        (9, 'Bcom Hons (Marketing)', 'Faculty of Economics and Management Sciences', 'Postgraduate', '1 year', 65.00),
        (10, 'Bcom Hons (Supply Chain Management)', 'Faculty of Economics and Management Sciences', 'Postgraduate',
         '1 year', 65.00),

    ]

    # populate the table with degree programs
    for program in degree_programs:
        cursor.execute(
            "INSERT OR IGNORE INTO DegreePrograms (DegreeID,DegreeName, FacultyName, LevelOfStudy, DegreeDuration, AverageRequired) VALUES (?, ?, ?, ?, ?, ?)",
            program)
    connection.commit()
    connection.close()


# displays all the programs offered according to study level
def view_programs_offered():
    # connects to the db
    connection = sqlite3.connect('thuto_ke_lesedi.db')
    cursor = connection.cursor()

    user_name = get_user()

    print("What's the desired leve of study? (e.g Undergraduate, Postgraduate)")
    level_of_study = str(input(f"{user_name}: "))
    if level_of_study.lower() == 'undergraduate':
        cursor.execute(
            " SELECT DegreeName, FacultyName, DegreeDuration, AverageRequired FROM DegreePrograms WHERE LevelOfStudy = 'Undergraduate'")
        undergraduate_degrees = cursor.fetchall()

        # display the degrees for Undergraduate
        print('Below is a list of all the available Undergraduate Degrees:')
        for degree, (DegreeName, FacultyName, DegreeDuration, AverageRequired) in enumerate(
                undergraduate_degrees, 1):
            print(
                f"{degree}. {DegreeName}, {FacultyName} - Duration: {DegreeDuration}, Required Average: {AverageRequired}")

    elif level_of_study.lower() == 'Postgraduate':
        cursor.execute(
            "SELECT DegreeName, FacultyName, DegreeDuration, AverageRequired FROM DegreePrograms WHERE LevelOfStudy = 'Postgraduate'")
        postgraduate_degrees = cursor.fetchall()

        # display the degrees for Undergraduate
        print('Below is a list of all the available Postgraduate Degrees:')
        for degree, (DegreeName, FacultyName, DegreeDuration, AverageRequired) in enumerate(
                postgraduate_degrees, 1):
            print(
                f"{degree}. {DegreeName}, {FacultyName} - Duration: {DegreeDuration}, Required Average: {AverageRequired}")

    else:
        print("Please enter a valid level of study, either 'Undergraduate' or 'Postgraduate'")
        connection.close()


# add the student details to the db
def save_personal_details(user_id, firstname, lastname, date_of_birth, identification_number,passport_number,gender, contact_number,email_address, physical_address):
    connection = sqlite3.connect('thuto_ke_lesedi.db')
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO Students (UserID, FirstName, LastName,DateOfBirth, IdentificationNumber,PassportNumber, Gender, ContactNumber, EmailAddress, PhysicalAddress) VALUES (?, ?,?,?,?,?,?,?,?,?)",
        (user_id, firstname, lastname, date_of_birth, identification_number,passport_number, gender, contact_number, email_address, physical_address))
    connection.commit()
    connection.close()


# add the education details provided by student
def save_education_details(user_id,  highest_education_Level = None, high_school_name = None, university_name = None, achieved_average = None):
    connection = sqlite3.connect('thuto_ke_lesedi.db')
    cursor = connection.cursor()
    if highest_education_Level == 'High School':
        # cursor.execute(
        #     "INSERT INTO Students (UserID, HighestEducationLevel, HighSchoolName, AchievedAverage) VALUES ( ?, ?, ?, ?)",
        #     (user_id, highest_education_Level, high_school_name, achieved_average))
        cursor.execute("UPDATE Students SET HighestEducationLevel = ?, HighSchoolName = ?, AchievedAverage = ? WHERE UserID = ? ", (highest_education_Level,high_school_name, achieved_average, user_id))
    else:
        # cursor.execute(
        #     "INSERT INTO Students (UserID, HighestEducationLevel, UniversityName, AchievedAverage) VALUES ( ?, ?, ?, ?)",
        #     (user_id, highest_education_Level, university_name, achieved_average))
        cursor.execute("UPDATE Students SET HighestEducationLevel = ?, UniversityName = ?, AchievedAverage = ? WHERE UserID = ? ", (highest_education_Level,university_name, achieved_average, user_id))


    connection.commit()
    connection.close()


# check if student qualifies to apply
def check_if_student_qualifies(average_achieved):
   connection = sqlite3.connect('thuto_ke_lesedi.db')
   cursor = connection.cursor()

   # get the requirements from degree table
   cursor.execute("SELECT DegreeID, DegreeName, FacultyName, AverageRequired FROM DegreePrograms")
   degree_programs = cursor.fetchall()

   # form suggestions based on what they qualify for
   degree_suggestions = []
   for program in degree_programs:
       degree_id, degree_name, faculty_name, average_required = program
       average_achieved = float(average_achieved)
       average_required = float(average_required)
       if average_required >= average_achieved:
           degree_suggestions.append((degree_id, degree_name, faculty_name, average_required))
   connection.close()
   return degree_suggestions


def save_progress(user_id, application_step):
    connection = sqlite3.connect('thuto_ke_lesedi.db')
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM ApplicationProgress WHERE UserID = ?", (user_id, ))
    user_exists = cursor.fetchone()[0]

    if user_exists:
        cursor.execute("UPDATE ApplicationProgress SET ApplicationStep = ? WHERE UserID = ?", (application_step, user_id))
    else:
        cursor.execute(
            "INSERT INTO ApplicationProgress (UserID, ApplicationStep) VALUES (?, ?) ON CONFLICT(UserID) DO UPDATE SET ApplicationStep =? ",
            (user_id, application_step, application_step))
    connection.commit()
    connection.close()


def get_progress(user_id):
    connection = sqlite3.connect('thuto_ke_lesedi.db')
    cursor = connection.cursor()
    cursor.execute("SELECT ApplicationStep FROM ApplicationProgress WHERE UserID = ?", (user_id,))
    application_step = cursor.fetchone()
    return int(application_step[0]) if application_step else 1

    connection.close()





add_degree_programs()
