import streamlit as st
import sklearn
import pickle
import string
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
nltk.download('stopwords')
nltk.download('punkt')
from nltk.stem import PorterStemmer

port_stemmer = PorterStemmer()

tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

# Create a function to generate cleaned data from raw text
def clean_text(text):
    # Remove URLs using regular expression
    text = re.sub(r'http\S+', '', text)
    
    text = word_tokenize(text) # Create tokens
    text = " ".join(text) # Join tokens
    text = [char for char in text if char not in string.punctuation] # Remove punctuations
    text = ''.join(text) # Join the letters
    text = [char for char in text if char not in re.findall(r"[0-9]", text)] # Remove Numbers
    text = ''.join(text) # Join the letters
    text = [word.lower() for word in text.split() if word.lower() not in set(stopwords.words('english'))] # Remove common English words (I, you, we,...)
    text = ' '.join(text) # Join the letters
    text = list(map(lambda x: port_stemmer.stem(x), text.split()))
    return " ".join(text)   # error word

def detect_smishing(text):
    # Define smishing keywords or patterns
    smishing_keywords = ["bank", "account", "password", "verify", "urgent"]
    smishing_patterns = ["click here", "call this number", "win a prize"]
    
    # Check for smishing keywords
    for keyword in smishing_keywords:
        if keyword in text:
            return True
    
    # Check for smishing patterns
    for pattern in smishing_patterns:
        if pattern in text:
            return True
    
    return False

st.title('SMS Spam Classifier')

input_sms = st.text_input("Enter the Message")

if st.button('Predict'):
    if input_sms == "":
        st.header('Please Enter Your Message !!!')
    else:
        # 1. Preprocess
        transform_text = clean_text(input_sms)

        # 2. Detect Smishing
        is_smishing = detect_smishing(transform_text)

        # 3. Vectorize
        vector_input = tfidf.transform([transform_text])

        # 4. Prediction
        if is_smishing:
            st.header("Smishing (SMS Phishing)")
        else:
            result = model.predict(vector_input)
            if result == 1:
                st.header("Spam")
            else:
                st.header("Not Spam")
