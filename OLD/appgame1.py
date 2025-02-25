import streamlit as st
import random
from pages.learn_page import learn
from pages.quiz_page import quiz

# Initialize session state
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0

def homepage():
    st.title("Welcome to the URL Phishing Quiz Game!")
    if st.button("Learn about Phishing"):
        st.session_state.page = "Learn"
    if st.button("Take the Quiz"):
        st.session_state.page = "Quiz"

def home():
    st.title("Home Page")
    st.write("Select an option from the sidebar.")

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Homepage", "Home", "Learn", "Quiz"])
    
    if page == "Homepage":
        homepage()
    elif page == "Home":
        home()
    elif page == "Learn":
        learn()
    elif page == "Quiz":
        quiz()

if __name__ == "__main__":
    main()