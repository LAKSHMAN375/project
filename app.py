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
    return " ".join(text)

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

st.title('SMS Spam Classifier')

# Add CSS for background image and animation
st.markdown(
    """
    <style>
    body {
        background-image: url('images.jpeg');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .spam-animation {
        position: fixed;
        top: 20px;
        right: 20px;
        width: 100px; /* Adjust the size as needed */
        height: 100px; /* Adjust the size as needed */
        animation: spin 2s linear infinite;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add spam animation
st.markdown('<div class="spam-animation">🚫</div>', unsafe_allow_html=True)

input_sms = st.text_input("Enter the Message")

if st.button('Predict'):
    if input_sms == "":
        st.header('Please Enter Your Message !!!')
    else:
        # Preprocess
        transform_text = clean_text(input_sms)

        # Detect Smishing
        is_smishing = detect_smishing(transform_text)

        # Prediction
        if is_smishing:
            st.header("Smishing (SMS Phishing)")
        else:
            st.header("Not Spam")
