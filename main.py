import re
import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.datasets import imdb


# Constants
max_length = 200
max_features = 5000

# Load the model
model = load_model("simple_rnn_imdb_model.h5")

# Load the word index from IMDB dataset
word_index = imdb.get_word_index()

# Function to preprocess text
def preprocess_text(text):
    # Clean text
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)

    # Convert to sequence of integers
    sequence = [word_index.get(word, 2) for word in text.split()]  # 2 is for <UNK>
    padded = pad_sequences([sequence], maxlen=max_length)
    return padded

# Function to predict sentiment
def predict_sentiment(review):
    processed_input = preprocess_text(review)
    prediction = model.predict(processed_input)
    sentiment = "Positive 😀" if prediction[0][0] > 0.5 else "Negative 😞"
    confidence = float(prediction[0][0])
    return sentiment, confidence

# Streamlit UI
st.title("🎬 Movie Review Sentiment Analysis (IMDB)")
st.write("Enter a movie review to predict if the sentiment is Positive or Negative.")

user_input = st.text_area("Review Text", height=200)

if st.button("Analyze"):
    if user_input.strip() == "":
        st.warning("Please enter a review to analyze.")
    else:
        sentiment, confidence = predict_sentiment(user_input)
        st.subheader("Sentiment Prediction:")
        st.success(f"{sentiment} (Confidence: {confidence:.2f})")









