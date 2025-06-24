# Most of the code below was inspired by

import pickle

import nltk
import numpy as np
import random
import json

from nltk import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split

from text_preprocessing import preprocess_input

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# loads the intents data file
with open('data/intent_classification_data.json') as file:
    intents = json.load(file)

# initialises the lemmatizer
lemmatizer = WordNetLemmatizer()


# for text preprocessing/ cleans it
def preprocess_questions(text):
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens if token.isalnum()]
    return ' '.join(tokens)


# initialise and prepare data for training
texts =[preprocess_input(item['text']) for item in intents ]
labels = [item['label'] for item in intents]

X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)





# # loops through the intents to get the correct questions from the data
# for intent in intents['intents']:
#     for question in intent['questions']:
#         processed_question = preprocess_questions(question)
#         questions.append(processed_question)
#         intent_labels.append(intent['intent'])
#     # adds a new one to the list
#     if intent['intent'] not in classes:
#         classes.append(intent['intent'])

# vectorizes the questions into numbers using TF-IDF
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)



# trains the model
model = LogisticRegression(max_iter=200)
model.fit(X_train_tfidf, y_train)

y_pred = model.predict(X_test_tfidf)
print(y_pred)


# loads and saves the model and vectorizer
def load_and_save():
    with open('vectorizer.pkl', 'wb') as file:
        pickle.dump(vectorizer, file)

    with open('model.pkl', 'wb') as file:
        pickle.dump(model, file)


def get_questions_response(intents_list, intents_json):
    # iterates through the list of intents and retrieves the list of answers for the intent
    questions_intent = intents_list[0]['intent']
    for intent in intents_json['intents']:
        if intent['intent'] == questions_intent:
            answers = intent.get('answers', [])
            # returns a random answer
            return random.choice(answers)
    return "Sorry, I don't have an answer for that right now!."

# def predict_class(text):
#     #process the input
#     text = preprocess_questions(text)
#     X_test = vectorizer.transform([text])
#     predictions = model.predict(X_test)
#     probabilities = model.predict_proba(X_test)
#     confidence = max(probabilities[0])
#     predicted_intent = predictions[0]
#     print(f"Processed Text: {text}")
#     print(f"Predictions: {predictions}, Confidence: {confidence}")
#     if confidence > 0.05:  # Adjust thresholds as needed
#         return [{'intent': predicted_intent, 'probability': confidence}]
#     else:
#         return [{'intent': 'unknown', 'probability': confidence}]
#

def check_similarity(questions_text):
    # processes the input questions
    questions_text = preprocess_questions(questions_text)
    similarity_scores = []
    for intent in intents['intents']:
        questions_vectors = vectorizer.transform(intent['questions'])
        questions_text_vector = vectorizer.transform([questions_text])
        # calculates the similarity using cosine between the input questions and questions in data
        similarity = cosine_similarity(questions_text_vector, questions_vectors).max()
        similarity_scores.append((intent['intent'], similarity))
    # gets the maximum score based on the similarity score above
    highest_score = max(similarity_scores, key=lambda x: x[1])
    if highest_score[1] > 0.5:
        return [{'intent': highest_score[0], 'similarity': highest_score[1]}]
    else:
        return [{'intent': 'unknown', 'similarity': highest_score[1]}]
