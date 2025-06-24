import sqlite3

# adds a new chatbot user
def add_new_user(user_name):
    connection = sqlite3.connect('thuto_ke_lesedi.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Users (UserName) VALUES (?)", (user_name,))
    connection.commit()
    connection.close()

# gets the user from the table
def get_user():
    connection = sqlite3.connect('thuto_ke_lesedi.db')
    cursor = connection.cursor()
    cursor.execute("SELECT UserName FROM Users ORDER BY UserID DESC limit 1")
    user = cursor.fetchone()
    connection.close()
    # returns the username
    if user:
        return user[0]
    else:
        return None

def update_username(user_id):
    connection = sqlite3.connect('thuto_ke_lesedi.db')
    cursor = connection.cursor()
    new_username = input("Enter your new username: ")
    cursor.execute("UPDATE Users SET UserName = ? WHERE UserID = ?", (new_username, user_id))
    connection.commit()

    print(f" You name has been changed to {new_username}!")
    connection.close()

def display_username(user_id):
    connection = sqlite3.connect('thuto_ke_lesedi.db')
    cursor = connection.cursor()
    cursor.execute("SELECT UserName FROM Users WHERE UserID =?", (user_id, ))
    username = cursor.fetchone()
    connection.close()
    if username:
        print(f"Your username is {username}")
    else:
        print("I am sorry but there's no username")