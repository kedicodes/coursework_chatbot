# The code below was inspired by what was taught in COMP3074 Lab 0 session and just the general knowledge of sql.

import sqlite3

#create the database and the tables
def create_database_tables():
    connection = sqlite3.connect('thuto_ke_lesedi.db')
    cursor = connection.cursor()
    # create a table to store users
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (UserID INTEGER PRIMARY KEY, UserName TEXT,ApplicationProgress Text,CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP);''')

    # create a table to store students personal information
    cursor.execute('''CREATE TABLE IF NOT EXISTS Students (StudentID INTEGER PRIMARY KEY, UserID INTEGER NOT NULL, FirstName TEXT NOT NULL, LastName TEXT NOT NULL, DateOfBirth DATE NOT NULL, IdentificationNumber INTEGER NOT NULL, PassportNumber INTEGER NOT NULL,Gender TEXT,EmailAddress TEXT NOT NULL, ContactNumber INTEGER,PhysicalAddress TEXT, HighestEducationLevel TEXT , HighSchoolName TEXT, UniversityName TEXT, AchievedAverage FLOAT, ChosenDegree Text, IdDocument BLOB, ResultDocument BLOB, FOREIGN KEY(UserID) REFERENCES Users(UserID));''')

    # create a table to store requirements per degree
    cursor.execute('''CREATE TABLE IF NOT EXISTS DegreePrograms (DegreeID INTEGER PRIMARY KEY, DegreeName TEXT, FacultyName TEXT, LevelOfStudy TEXT, DegreeDuration INTEGER, AverageRequired FLOAT);''')

    # create a table to track the application progress
    cursor.execute('''CREATE TABLE IF NOT EXISTS ApplicationProgress(ApplicationProgressID INTEGER PRIMARY KEY, UserID INTEGER NOT NULL UNIQUE, StudentID INTEGER, ApplicationStep INTEGER, FOREIGN KEY(UserID) REFERENCES Users(UserID), FOREIGN KEY(StudentID) REFERENCES Students(StudentID));''')



    connection.commit()
    connection.close()

# initialise the table
create_database_tables()
