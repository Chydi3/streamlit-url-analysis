import streamlit as st
from PIL import Image
import time

# ------------------ Quiz State Reset ------------------
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
    # Page config
    st.set_page_config(
        page_title="URL Readability & Phishing Awareness",
        page_icon="🔍",
        layout="wide"
    )
    # Always clear out any old quiz state on landing
    reset_quiz_state()

    # —– USER SIGN‑IN PROMPT —–
    if "player_name" not in st.session_state:
        st.session_state.player_name = ""
    st.title("🔍 URL Readability & Phishing Awareness")
    st.subheader("👤 Please enter your name to begin:")
    name = st.text_input("Name:", st.session_state.player_name)
    st.session_state.player_name = name

    if not name:
        st.warning("⚠️ You must enter your name before proceeding.")
        return  # stop here until name is filled

    # —– HEADER & DESCRIPTION —–
    st.subheader(f"Welcome, {name}!")
    st.write(
        "Learn to analyze URLs correctly and test your phishing‑detection skills."
    )
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Padlock_icon_blue.svg/1920px-Padlock_icon_blue.svg.png",
        caption="Stay Secure. Stay Informed.",
        use_container_width=True
    )

    # —– NAVIGATION BUTTONS —–
    st.header("🛠 Get Started")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📖 Learn About Phishing URLs"):
            st.switch_page("/home/al/my_streamlit_project/pages/Learn.py")  # assume your Learn page is named Learn.py
    with col2:
        if st.button("🧠 Take the Quiz"):
            st.switch_page("/home/al/my_streamlit_project/pages/Quiz.py")   # assume your Quiz page is named Quiz.py

    # —– OPTIONAL: Student Type Links —–
    st.markdown("---")
    st.header("🎓 Are you an International or German student?")
    col_intl, col_german = st.columns(2)
    with col_intl:
        st.markdown(
            '<a href="/home/al/my_streamlit_project/pages/Quiz_international.py" '
            'class="btn btn-intl">International Student</a>',
            unsafe_allow_html=True
        )
    with col_german:
        st.markdown(
            '<a href="/home/al/my_streamlit_project/pages/Quiz_german.py" '
            'class="btn btn-german">German Student</a>',
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
