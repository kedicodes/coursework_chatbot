# load the questions and answers json
import json
import pickle

from sklearn.metrics.pairwise import cosine_similarity

from text_preprocessing import preprocess_input

