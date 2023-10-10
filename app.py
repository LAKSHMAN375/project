import streamlit as st
import string
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pickle

# Load the TF-IDF vectorizer and model
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

# Define the patterns
patterns = [
    r".*(bank|account|unusual activity|verify|details|unauthorized).*",
    r".*(won|prize|lottery|claim|processing fee|offer is valid|free cash).*",
    r".*(tech support|malware|infected|call|immediate assistance).*",
    r".*(urgent|bank|unusual activity|secure|transactions).*",
    r".*(tax notice|unclaimed tax refund|social security number|bank details).*",
    r".*(subscription|canceled|payment issue|update payment details|disruption).*",
    r".*(unlock|premium features|download|app|unlimited access).*"
]

# Define a function to clean and preprocess the text
def clean_text(text):
    # ... (rest of your code remains the same)
    return text

# Create a Streamlit app
st.title('SMS Spam Classifier')

input_sms = st.text_area("Enter the Message")

if st.button('Detect'):
    if input_sms == "":
        st.header('Please Enter Your Message !!!')
    else:
        # Preprocess the input SMS
        cleaned_sms = clean_text(input_sms)

        # Check for patterns
        if any(re.match(pattern, cleaned_sms, re.IGNORECASE) for pattern in patterns):
            # Vectorize the input
            vector_input = tfidf.transform([cleaned_sms])

            # Make a prediction
            result = model.predict(vector_input)

            # Display the prediction
            if result == 1:
                st.header("Spam")
            else:
                st.header("Not Spam")
        else:
            st.header("Enter Correct SMS Pattern")
