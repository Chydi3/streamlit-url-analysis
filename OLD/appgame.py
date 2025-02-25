import streamlit as st
import random

# Sample quiz questions
questions = [
    {"question": "Which of these URLs is likely phishing?", 
     "options": ["https://www.paypal.com", "https://paypa1.com/login", "https://secure.paypal.com"],
     "answer": "https://paypa1.com/login",
     "explanation": "The URL uses 'paypa1' instead of 'paypal', which is a common phishing trick."},
    {"question": "What should you check first in a URL?", 
     "options": ["The domain name", "The font style", "The background color"],
     "answer": "The domain name",
     "explanation": "The domain name is crucial in verifying authenticity."}
]

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0

def home():
    st.title("Welcome to the URL Phishing Quiz Game!")
    if st.button("Learn about Phishing"):
        st.session_state.page = "learn"
    if st.button("Take the Quiz"):
        st.session_state.page = "quiz"








        

def learn():
    st.title("Learn About Phishing URLs")
    st.write("Phishing attacks trick users by using fake URLs that look real.")
    st.write("Here are some common phishing tricks:")
    st.markdown("- Using similar-looking characters (e.g., paypa1 instead of paypal)")
    st.markdown("- Adding extra words (e.g., secure-paypal.com instead of paypal.com)")
    st.markdown("- Using HTTP instead of HTTPS")
    if st.button("Back to Home"):
        st.session_state.page = "home"

def quiz():
    st.title("URL Phishing Quiz")
    q_index = st.session_state.current_q
    if q_index < len(questions):
        question = questions[q_index]
        st.write(question["question"])
        choice = st.radio("Select an answer:", question["options"])
        if st.button("Submit"):
            if choice == question["answer"]:
                st.session_state.score += 1
                st.success("Correct! " + question["explanation"])
            else:
                st.error("Wrong! " + question["explanation"])
            st.session_state.current_q += 1
    else:
        st.write(f"Quiz Completed! Your final score: {st.session_state.score}/{len(questions)}")
        if st.button("Restart Quiz"):
            st.session_state.current_q = 0
            st.session_state.score = 0

def main():
    if st.session_state.page == "home":
        home()
    elif st.session_state.page == "learn":
        learn()
    elif st.session_state.page == "quiz":
        quiz()

if __name__ == "__main__":
    main()
