import streamlit as st
from PIL import Image
import requests
import time

def reset_quiz_state():
    st.session_state.quiz_data = []
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.streak = 0
    st.session_state.timer = time.time()
    st.session_state.user_answers = []
    st.session_state.sub_answers = []
    st.session_state.answered = False
    st.session_state.sub_answered = False
    st.session_state.quiz_active = True
    st.session_state.question_start_time = time.time()

def main():
    # Set page configuration
    st.set_page_config(page_title="URL Readability & Phishing Awareness", page_icon="🔍", layout="wide")
    
    # Reset quiz state for new user login
    reset_quiz_state()
    
    # Inject custom CSS for the student type buttons
    st.markdown("""
    <style>
    .btn {
        display: inline-block;
        font-weight: bold;
        color: white;
        text-align: center;
        padding: 14px 28px;
        font-size: 16px;
        margin: 8px 4px;
        border-radius: 8px;
        text-decoration: none;
    }
    .btn-intl {
        background-color: #007BFF;
    }
    .btn-intl:hover {
        background-color: #0056b3;
    }
    .btn-german {
        background-color: #28a745;
    }
    .btn-german:hover {
        background-color: #1e7e34;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header section
    st.title("🔍 URL Readability & Phishing Awareness")
    st.subheader("Learn to analyze URLs and identify phishing threats!")
    
    # Display a high-quality security image from the provided URL
    st.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Padlock_icon_blue.svg/1920px-Padlock_icon_blue.svg.png",
    caption="Stay Secure. Stay Informed.",
    use_container_width=True
)

    
    # Description
    st.write(
        "Welcome to the URL Readability & Phishing Awareness platform! "
        "This tool helps users understand how to read URLs correctly and detect potential phishing threats. "
        "You can learn about phishing indicators and test your knowledge with an interactive quiz."
    )
    
    # Navigation options
    st.header("🛠 Get Started")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📖 Learn About Phishing URLs"):
            st.switch_page("/home/al/my_streamlit_project/pages/Learn.py")  # Ensure correct file path
    with col2:
        if st.button("🧠 Take the Quiz"):
            st.switch_page("/home/al/my_streamlit_project/pages/Quiz.py")  # Ensure correct file path
    
    # New Section: Student Type Question with custom-styled buttons
    st.header("🎓 Student Type")
    st.write("Are you an **International** student or a **German** student?")
    col_intl, col_german = st.columns(2)
    
    with col_intl:
        st.markdown(
            '<a href="/home/al/my_streamlit_project/pages/Quiz_international.py" class="btn btn-intl">International Student</a>',
            unsafe_allow_html=True
        )
    with col_german:
        st.markdown(
            '<a href="/home/al/my_streamlit_project/pages/Quiz_german.py" class="btn btn-german">German Student</a>',
            unsafe_allow_html=True
        )


if __name__ == "__main__":
    main()


