import streamlit as st
import string
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
import pickle

# Load the TF-IDF vectorizer and model
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

# Load your dataset
data = pd.read_excel("SMSSpamCollection.xlsx", header=None)
data.rename(columns={0: 'Category', 1: 'Email Text'}, inplace=True)
last_10_messages = data.tail(22)['Email Text'].tolist()

# Define a function to clean and preprocess the text
def clean_text(text):
    text = re.sub(r'http\S+', '', text)
    text = word_tokenize(text)  # Tokenize
    text = " ".join(text)  # Join tokens
    text = [char for char in text if char not in string.punctuation]  # Remove punctuation
    text = ''.join(text)  # Join the letters
    text = [char for char in text if char not in re.findall(r"[0-9]", text)]  # Remove numbers
    text = ''.join(text)  # Join the letters
    text = [word.lower() for word in text.split() if word.lower() not in set(stopwords.words('english'))]  # Remove stopwords
    text = ' '.join(text)  # Join the letters
    return text

# Create a Streamlit app
st.title('SMS Spam Classifier')

input_sms = st.text_input("Enter the Message")

if st.button('Predict'):
    if input_sms == "":
        st.header('Please Enter Your Message !!!')
    else:
        # Preprocess the input SMS
        cleaned_sms = clean_text(input_sms)

        # Check for keywords in the last 10 messages
        contains_keyword = any(keyword in " ".join(last_10_messages).lower() for keyword in cleaned_sms.split())

        # Vectorize the input
        vector_input = tfidf.transform([cleaned_sms])

        # Make a prediction
        result = model.predict(vector_input)

        # Display the prediction
        if contains_keyword:
            st.header("Potential Smishing Message")
        elif result == 1:
            st.header("Spam")
        else:
            st.header("Not Spam")
