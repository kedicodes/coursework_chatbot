

import text_processing
from database_management import create_database_tables
from identity_management import get_user, add_new_user, update_username
from student_enrollment import enrol_to_university
from student_management import add_degree_programs,view_programs_offered
from text_classifier import predict_class
from text_processing import get_questions_response, check_similarity


# handles the responses based on the intents(intent matching)
# def chatbot_response(questions):
#     # gets the predicted intent for input questions
#     intents_list =check_similarity(questions)
#     answer_response = get_questions_response(intents_list, text_processing.intents)
#     return answer_response
def chatbot_response(user_input):
    predicted_intent_data = predict_class(user_input)
    predicted_intent = predicted_intent_data[0]['intent']
    confidence = predicted_intent_data[0]['probability']




def application_response(username):
    print("\n 💡 Let's get started with your application! Feel free to Type 'menu' to return")
    print("💡1. Apply to University")
    print("💡2. View the degree programs offered by Thuto Ke Lesedi")
    print("💡3. Ask questions about the University")
    user_id = get_user()

    user_option = input(f"{username}: ").strip()
    if user_option == "1":
      print("💡Let's get started with your application process!")
      enrol_to_university(user_id)
    elif user_option == "2":
        print("💡 These are the available degree programs offered by Thuto Ke Lesedi:")
        view_programs_offered()
    elif user_option == "3":
        print("💡 ")
        chatbot_response(user_option)


# main chatbot method
def main():
    create_database_tables()
    text_processing.load_and_save()

    # gets user's name from the database or add new user if they don't exist
    user_name = get_user()
    if user_name:
        print(f" 💡Welcome Back {user_name}, Our Prospective Thuto Ke Lesedi University Student!")
    else:
        print("It looks like you are new here and I would like to know you")
        user_name = input("Please tell me your name: ")
        add_new_user(user_name)
        user_name = get_user()
        print(f" 💡Happy to meet you, {user_name}! Welcome to Thuto Ke Lesedi University Application Assistant!")


    # starts the main chatbot loop
    while True:
        print('Type "quit" to quit or "application" to start with your University application')
        user_input = input(f'{user_name}: ')
        if user_input.lower() in ['exit', 'quit', 'bye']:
            # breaks out of the loop and end chat
            break
        elif user_input.lower() in ['change my name', 'update my name']:
            update_username(user_name)
            user_name = get_user()
        #     maybe remove the lower even above
        elif user_input.lower() in ['know my username', 'what is my username', 'what is my name']:
            print(f"Your name is {user_name}")
        elif user_input.lower() == "application":
            application_response(user_name)

        response = chatbot_response(user_input)
        print(response)


if __name__ == '__main__':
    main()
    add_degree_programs()
