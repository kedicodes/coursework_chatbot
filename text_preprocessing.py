import re
import string

import nltk
from nltk import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

# for text preprocessing/ cleans it
def preprocess_input(text):
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    tokens = [token for token in tokens if token not in string.punctuation]
    tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens if token.isalnum()]
    return ' '.join(tokens)

