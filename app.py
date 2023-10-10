import streamlit as st
import re

# Define a function to detect patterns in the text
def detect_keywords(text):
    keywords = [
        "bank", "account", "unusual activity", "verify", "details", "unauthorized",
        "won", "prize", "lottery", "claim", "processing fee", "offer is valid", "free cash",
        "tech support", "malware", "infected", "call", "immediate assistance",
        "urgent", "bank", "unusual activity", "secure", "transactions",
        "tax notice", "unclaimed tax refund", "social security number", "bank details",
        "subscription", "canceled", "payment issue", "update payment details", "disruption",
        "unlock", "premium features", "download", "app", "unlimited access"
    ]
    
    for keyword in keywords:
        if keyword in text.lower():
            return True
    
    return False

# Create a Streamlit app
st.title('SMS Spam Keyword Detector')

input_sms = st.text_area("Enter the Message")

if st.button('Detect'):
    if input_sms == "":
        st.header('Please Enter Your Message !!!')
    else:
        # Check for keywords
        if detect_keywords(input_sms):
            vector_input = tfidf.transform([cleaned_sms])

            # Make a prediction
            result = model.predict(vector_input)
            # Display the prediction
            if result == 1:
                st.header("Spam")
            else:
                st.header("Not Spam")
        else:
            st.header("Enter Correct Pattern")

