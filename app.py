
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

# Define a function to detect patterns in the text
def detect_patterns(text):
    patterns = [
        r".*(bank|account|unusual activity|verify|details|unauthorized).*",
        r".*(won|prize|lottery|claim|processing fee||offer is valid|| free cash).*",
        r".*(tech support|malware|infected|call|immediate assistance).*",
        r".*(urgent|bank|unusual activity|secure|transactions).*",
        r".*(tax notice|unclaimed tax refund|social security number|bank details).*",
        r".*(subscription|canceled|payment issue|update payment details|disruption).*",
        r".*(unlock|premium features|download|app|unlimited access).*"
    ]
    
    for pattern in patterns:
        if re.match(pattern, text, re.IGNORECASE):
            return True
    
    return False

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
        if detect_patterns(cleaned_sms):
            # Make a prediction
            result = model.predict(vector_input)
             # Display the prediction
            if result == 1:
                st.header("Spam")
            else:
                st.header("Not Spam")
        else:
          st.header("Enter Correct Pattern")
