import streamlit as st
import pickle
import re
import nltk

nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Load model and vectorizer
import os

BASE_DIR = os.path.dirname(__file__)

model = pickle.load(
    open(os.path.join(BASE_DIR, "sentiment_model.pkl"), "rb")
)

vectorizer = pickle.load(
    open(os.path.join(BASE_DIR, "tfidf_vectorizer.pkl"), "rb")
)

# Initialize stemmer
port_stem = PorterStemmer()

# Preprocessing function
def stemming(content):
    stemmed_content = re.sub('[^a-zA-Z]', ' ', content)
    stemmed_content = stemmed_content.lower()
    stemmed_content = stemmed_content.split()

    stemmed_content = [
        port_stem.stem(word)
        for word in stemmed_content
        if word not in stopwords.words('english')
    ]

    stemmed_content = ' '.join(stemmed_content)

    return stemmed_content

# Streamlit UI
st.title("Twitter Sentiment Analysis")

st.write("Enter a tweet and predict whether the sentiment is Positive or Negative.")

user_input = st.text_area("Enter Tweet Text")

if st.button("Predict Sentiment"):

    if user_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        processed_text = stemming(user_input)

        input_data = vectorizer.transform([processed_text])

        prediction = model.predict(input_data)

        if prediction[0] == 0:
            st.error("Negative Sentiment 😔")
        else:
            st.success("Positive Sentiment 😊")
