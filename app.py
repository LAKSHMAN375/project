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
    smishing_keywords = [
        "bank", "account", "password", "verify", "urgent",
        "healthcare", "insurance", "appointment", "patient",
        "retail", "discount", "sale", "order", "product",
        "government", "tax", "benefits", "citizenship",
        "charity", "donation", "aid", "relief",
        "education", "student", "school", "scholarship",
        "technology", "security", "hack", "cyber",
        "travel", "flight", "reservation", "hotel",
        "social", "dating", "romance", "relationship",
        "employment", "job", "resume", "career"
    ]
    
    smishing_patterns = [
        "click here", "call this number", "win a prize",
        "COVID-19", "vaccine", "testing", "relief fund",
        "package delivery", "shipping confirmation",
        "government agency", "IRS", "immigration",
        "tax refund","This OTP will expire in 15 minutes"
    ]
    
    # Check for smishing keywords
    for keyword in smishing_keywords:
        if keyword in text:
            return True
    
    # Check for smishing patterns
    for pattern in smishing_patterns:
        if pattern in text:
            return True
    
    return False

def detect_fake_otp(text):
    # Define a list of OTP patterns
    otp_patterns = [
        "Your OTP is:", "Enter OTP:", "Verification code:", "OTP: 123456",
        "OTP: 1234", "OTP: 0000", "One-Time Password:", "Your code is:",
        "Authentication code:", "Security code:", "OTP is: 5678", "OTP - 98765",
        "OTP code:", "OTP# 9876", "Code: 4321", "OTP 987654",
        "Confirmation code:", "Access code: 8765", "Validation code:",
        "Code for verification:", "Pin code: 9999", "Key is: 7654",
        "2345 is your OTP","345678 is your OTP","234567 is the OTP",
        "1234 is the OTP",r'\b\d{4,6}\b',  
        r'\b[0-9]{6}\b',  
        r'\bcode\s*[:#]?\s*[0-9]{4,6}\b',  
        r'\botp\s*[:#]?\s*[0-9]{4,6}\b',   
        r'\bverification\s*[:#]?\s*[0-9]{4,6}\b',  
        r'\bsecurity\s*[:#]?\s*[0-9]{4,6}\b', 
    ]
    
    # Check for OTP patterns
    for pattern in otp_patterns:
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

        # 3. Detect Fake OTP
        is_fake_otp = detect_fake_otp(transform_text)

        # 4. Vectorize
        vector_input = tfidf.transform([transform_text])

        # 5. Prediction
        if is_fake_otp:
            st.header("Fake OTP")
        elif is_smishing:
            st.header("Smishing (SMS Phishing)")
        else:
            result = model.predict(vector_input)
            if result == 1:
                st.header("Spam")
            else:
                st.header("Not Spam")
