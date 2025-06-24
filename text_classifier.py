import json
import pickle

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from text_preprocessing import preprocess_input

with open('data/intent_classification_data.json') as file:
    intents = json.load(file)

texts = [item['text'] for item in intents]
labels = [item['label'] for item in intents]

# splits the data
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

# vectorizes the text
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

y_pred = model.predict(X_test_tfidf)
print(y_pred)

# print(classification_report(y_test, y_pred))

def load_and_save():
    with open('vectorizer.pkl', 'wb') as file:
        pickle.dump(vectorizer, file)

    with open('model.pkl', 'wb') as file:
        pickle.dump(model, file)

def predict_class(text):
    text = preprocess_input(text)
    X_test = vectorizer.transform(text)
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)
    confidence = max(probabilities[0])
    predicted_intent = predictions[0]
    print(f"Processed Text: {text}")
    print(f"Predictions: {predictions}, Confidence: {confidence}")
    if confidence > 0.5:
        return [{'intent': predicted_intent, 'probability': confidence}]
    else:
            return [{'intent': 'unknown', 'probability': confidence}]









