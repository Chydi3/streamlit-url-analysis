import streamlit as st
import time
import pandas as pd
import os
from helpers import save_username_to_file, load_username_from_file

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

# ------------------ Check for Duplicate Name ------------------
def is_duplicate_name(name):
    if os.path.exists("quiz_results.csv"):
        df = pd.read_csv("quiz_results.csv")
        return name.strip().lower() in df["Player Name"].str.lower().str.strip().tolist()
    return False

# ------------------ Main App ------------------
def main():
    st.set_page_config(
        page_title="CyberSecure: URL Awareness",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # ------------- SYSTEM-COMPATIBLE CSS WITH GLOW EFFECTS ---------------------
    st.markdown("""
    <style>
    /* System-compatible base styles */
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Glowing title (works in both modes) */
    .big-title {
        font-size: 2.8rem;
        font-weight: 700;
        text-align: center;
        margin-top: 0.5rem;
        color: #00B4D8; /* Cyan-blue that works in both themes */
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    /* Glowing username */
    .glowing-name {
        color: #00B4D8;
        font-weight: bold;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    /* Glow animation */
    @keyframes glow {
        from {
            text-shadow: 0 0 5px #00B4D8, 0 0 10px #00B4D8;
            opacity: 0.9;
        }
        to {
            text-shadow: 0 0 15px #00B4D8, 0 0 25px #00B4D8;
            opacity: 1;
        }
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        color: var(--text-color);
    }
    
    /* Input box */
    .name-box input {
        border-radius: 5px;
        padding: 0.75rem;
        border: 1px solid var(--primary-color);
        font-size: 1.1rem;
        width: 50%;
        margin: 0 auto;
        display: block;
        background-color: var(--background-color);
    }
    
    /* Welcome text */
    .welcome-text {
        font-size: 1.8rem;
        text-align: center;
        margin: 1.5rem 0;
        color: var(--text-color);
    }
    
    /* Student section */
    .student-section {
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem auto;
        width: 80%;
        border: 1px solid var(--primary-color);
        background-color: var(--background-color);
        text-align: center;
    }
    
    /* Version badge */
    .badge {
        position: absolute;
        top: 20px;
        right: 20px;
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        border: 1px solid var(--primary-color);
        font-weight: bold;
        font-size: 1.1rem;
        background-color: var(--background-color);
    }
    
    /* Button container */
    .button-row {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin: 30px 0;
    }
    
    /* Button styles */
    .learn-btn, .quiz-btn, .button-intl, .button-german {
        padding: 0.75rem 2rem;
        font-size: 1rem;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 600;
        width: 100%;
        text-align: center;
        background-color: transparent;
    }
    
    .learn-btn { 
        border: 2px solid var(--primary-color); 
        color: var(--primary-color); 
    }
    .learn-btn:hover { 
        background-color: var(--primary-color); 
        color: white; 
        transform: scale(1.05); 
    }
    
    .quiz-btn { 
        border: 2px solid #FF6B6B; 
        color: #FF6B6B; 
    }
    .quiz-btn:hover { 
        background-color: #FF6B6B; 
        color: white; 
        transform: scale(1.05); 
    }
    
    .button-intl { 
        border: 2px solid #9B59B6; 
        color: #9B59B6; 
    }
    .button-intl:hover { 
        background-color: #9B59B6; 
        color: white; 
    }
    
    .button-german { 
        border: 2px solid #95A5A6; 
        color: #95A5A6; 
    }
    .button-german:hover { 
        background-color: #95A5A6; 
        color: white; 
    }
    
    /* Hide sidebar elements */
    [data-testid="stSidebar"],
    [data-testid="collapsedControl"],
    [data-testid="stBaseButton-headerNoPadding"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

    reset_quiz_state()

    # Add version badge
    st.markdown('<div class="badge">v2.5</div>', unsafe_allow_html=True)

    st.markdown('<div class="big-title">🔐 CyberSecure: URL Readability & Phishing Awareness</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Learn to detect phishing URLs and secure your web experience</div>', unsafe_allow_html=True)

    st.markdown("<div class='input-container'>", unsafe_allow_html=True)

    if "player_name" not in st.session_state:
        st.session_state.player_name = ""

    name = st.text_input(
        "👤 Enter your name to begin:",
        key="player_name",
        placeholder="Your Name",
        help="Required to start",
        label_visibility="collapsed"
    )

    save_username_to_file(name)

    st.markdown('</div>', unsafe_allow_html=True)

    if not name.strip():
        st.warning("⚠️ You must enter your name before proceeding.")
        return

    if is_duplicate_name(name):
        st.error("❌ This name is already taken. Please choose a different one.")
        return

    st.markdown(
        f"<div class='welcome-text'>Welcome, <span class='glowing-name'>{name}</span>!</div>", 
        unsafe_allow_html=True
    )

    st.markdown('<div class="button-row">', unsafe_allow_html=True)

    if st.button("📚 Learn About Phishing", key="learn_btn", help="Start with the learning module"):
        st.switch_page("pages/Learn.py")

    st.markdown("""
        <script>
        document.querySelector('[data-testid="baseButton-secondary"]').className = "learn-btn";
        </script>
    """, unsafe_allow_html=True)

    if st.button("🧠 Take the Quiz", key="quiz_btn", help="Test your phishing detection skills"):
        st.switch_page("pages/Quiz.py")

    st.markdown("""
        <script>
        document.querySelectorAll('[data-testid="baseButton-secondary"]')[1].className = "quiz-btn";
        </script>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div class='student-section'>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center;'>🎓 Are you an International or German student?</h4>", unsafe_allow_html=True)

    col_intl, col_german = st.columns(2)
    with col_intl:
        st.markdown(
            '<a href="/home/al/my_streamlit_project/pages/Quiz_international.py">'
            '<button class="button-intl">🌍 International Student</button></a>',
            unsafe_allow_html=True
        )
    with col_german:
        st.markdown(
            '<a href="/home/al/my_streamlit_project/pages/Quiz_german.py">'
            '<button class="button-german">🇩🇪 German Student</button></a>',
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    