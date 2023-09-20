import streamlit as st
import pickle
import string
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
nltk.download('stopwords')
nltk.download('punkt')
from nltk.stem import PorterStemmer
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import auth

# Initialize Firebase Admin SDK
cred = credentials.Certificate("smsspam-d94e5-firebase-adminsdk-m4lu0-5b94c7194e.json")
firebase_admin.initialize_app(cred)

# Create a function to generate cleaned data from raw text
def clean_text(text):
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
    return " ".join(text)

# Function to detect SMS smishing
def detect_smishing(text):
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
        "tax refund", "This OTP will expire in 15 minutes"
    ]
    for keyword in smishing_keywords:
        if keyword in text:
            return True
    
    # Check for smishing patterns
    for pattern in smishing_patterns:
        if pattern in text:
            return True
    
    return False

# User registration and authentication
def register_user(username, password):
    # You would typically store user information in a database
    # For simplicity, we'll use a dictionary here
    users = {"user1": "password1", "user2": "password2"}

    if username in users:
        return False  # User already exists
    else:
        users[username] = password
        return True  # User successfully registered

def login_user(username, password):
    # Check if the provided username and password match
    users = {"user1": "password1", "user2": "password2"}

    if username in users and users[username] == password:
        return True  # User successfully logged in
    else:
        return False  # Invalid credentials

# Initialize Streamlit app
st.title('SMS Spam Classifier')

# User registration and login form
if st.checkbox('Register'):
    st.subheader('User Registration')
    new_username = st.text_input('Enter a new username:')
    new_password = st.text_input('Enter a new password:', type='password')
    if st.button('Register'):
        if new_username and new_password:
            if register_user(new_username, new_password):
                st.success('Registration successful. Please log in.')
            else:
                st.warning('Username already exists. Please choose another.')

if st.checkbox('Log In'):
    st.subheader('User Login')
    username = st.text_input('Enter your username:')
    password = st.text_input('Enter your password:', type='password')
    if st.button('Login'):
        if username and password:
            if login_user(username, password):
                st.success('Login successful.')

                # SMS Spam/Smishing Detection
                input_sms = st.text_input("Enter the Message")
                if st.button('Predict'):
                    # Preprocess
                    transform_text = clean_text(input_sms)

                    # Detect Smishing
                    is_smishing = detect_smishing(transform_text)

                    # Prediction
                    if is_smishing:
                        st.header("Smishing (SMS Phishing)")
                    else:
                        st.header("Not Spam")
            else:
                st.warning('Invalid credentials. Please try again.')
