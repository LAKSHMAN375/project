import streamlit as st

# Define your other Streamlit app's file URL here
other_app_file_url = "https://smsspamdetectionusingnlp.streamlit.app/#smishing-sms-phishing"

st.title('Login and Signup')

# User registration form
if st.button('Sign Up'):
    st.subheader('User Registration')
    new_username = st.text_input('Enter a new username:')
    new_password = st.text_input('Enter a new password:', type='password')
    if st.button('Register'):
        if new_username and new_password:
            # Your registration logic here
            st.success('Registration successful. Please log in.')
        else:
            st.warning('Please enter both a username and password.')

# User login form
if st.button('Log In'):
    st.subheader('User Login')
    username = st.text_input('Enter your username:')
    password = st.text_input('Enter your password:', type='password')
    if st.button('Login'):
        if username and password:
            # Your login logic here
            if username == "your_username" and password == "your_password":
                st.success('Login successful.')
                # Add a link to the other app or file
                st.markdown(f"[Click here to access the other app]({other_app_file_url})")
            else:
                st.warning('Invalid credentials. Please try again.')
        else:
            st.warning('Please enter both a username and password.')
