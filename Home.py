import streamlit as st
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

# ------------------ Main App ------------------
def main():
    st.set_page_config(
        page_title="CyberSecure: URL Awareness",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # ------------- CUSTOM CSS ---------------------
    st.markdown("""
    <style>
    html, body, [class*="css"] {
        background: linear-gradient(to bottom right, #0a1929, #142a45, #1d3b5a);
        color: #f1f1f1;
        font-family: 'Segoe UI', sans-serif;
    }
    .big-title {
        font-size: 2.8rem;
        font-weight: 700;
        text-align: center;
        margin-top: 0.5rem;
        color: #00ffe0;
        animation: glow 2s ease-in-out infinite alternate;
        text-shadow: 0 0 10px #00ffe0;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #88FFFF;
        margin-bottom: 2rem;
    }
    .name-box input {
        background-color: rgba(30,30,30,0.5) !important;
        color: #f1f1f1 !important;
        border-radius: 5px;
        padding: 0.75rem;
        border: 1px solid #00ffe0;
        font-size: 1.1rem;
        width: 50%;
        margin: 0 auto;
        display: block;
    }
    .welcome-text {
        font-size: 1.8rem;
        text-align: center;
        color: #00ffe0;
        margin: 1.5rem 0;
        text-shadow: 0 0 5px #00ffe0;
    }
    .glowing-name {
        animation: glow 2s ease-in-out infinite alternate;
        color: #00FFFF;
        font-weight: bold;
    }
    .student-section {
        background-color: rgba(0,0,0,0.3);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem auto;
        width: 80%;
        border: 1px solid #00ffe0;
        box-shadow: 0 0 15px rgba(0, 255, 224, 0.2);
        text-align: center;
    }
    .badge {
        position: absolute;
        top: 20px;
        right: 20px;
        background-color: rgba(0,0,0,0.5);
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        color: #00ffe0;
        border: 1px solid #00ffe0;
        font-weight: bold;
        font-size: 1.1rem;
        box-shadow: 0 0 10px rgba(0, 255, 224, 0.3);
    }
    .input-container {
        text-align: center;
        margin: 1rem 0 2rem;
    }
    .nav-container {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 2rem 0;
    }
    /* Custom button styling */
    .learn-btn {
        padding: 0.75rem 2rem;
        font-size: 1rem;
        border: 2px solid #FFD700;
        border-radius: 8px;
        background-color: rgba(0,0,0,0.3);
        color: #FFD700;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 600;
        width: 100%;
        text-align: center;
    }
    .learn-btn:hover {
        background-color: #FFD700;
        color: #0a1929;
        transform: scale(1.05);
        box-shadow: 0 0 15px #FFD700;
    }
    .quiz-btn {
        padding: 0.75rem 2rem;
        font-size: 1rem;
        border: 2px solid #FF6B6B;
        border-radius: 8px;
        background-color: rgba(0,0,0,0.3);
        color: #FF6B6B;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 600;
        width: 100%;
        text-align: center;
    }
    .quiz-btn:hover {
        background-color: #FF6B6B;
        color: #0a1929;
        transform: scale(1.05);
        box-shadow: 0 0 15px #FF6B6B;
    }
    .button-intl {
        padding: 0.75rem 2rem;
        font-size: 1rem;
        border: 2px solid #9B59B6;
        border-radius: 8px;
        background-color: rgba(0,0,0,0.3);
        color: #9B59B6;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 600;
        width: 100%;
        text-align: center;
    }
    .button-intl:hover {
        background-color: #9B59B6;
        color: #0a1929;
        transform: scale(1.05);
        box-shadow: 0 0 15px #9B59B6;
    }
    .button-german {
        padding: 0.75rem 2rem;
        font-size: 1rem;
        border: 2px solid #95A5A6;
        border-radius: 8px;
        background-color: rgba(0,0,0,0.3);
        color: #95A5A6;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 600;
        width: 100%;
        text-align: center;
    }
    .button-german:hover {
        background-color: #95A5A6;
        color: #0a1929;
        transform: scale(1.05);
        box-shadow: 0 0 15px #95A5A6;
    }
    .button-row {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin: 30px 0;
    }
    @keyframes glow {
        from { text-shadow: 0 0 5px #00ffe0, 0 0 10px #00ffe0; }
        to   { text-shadow: 0 0 20px #00ffe0, 0 0 30px #00ffe0; }
    }
    </style>
    """, unsafe_allow_html=True)

    reset_quiz_state()

    # Add version badge
    st.markdown('<div class="badge">v2.5</div>', unsafe_allow_html=True)

    # Header Section
    st.markdown('<div class="big-title">🔐 CyberSecure: URL Readability & Phishing Awareness</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Learn to detect phishing URLs and secure your web experience</div>', unsafe_allow_html=True)

    # Name Entry Section
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
    st.markdown('</div>', unsafe_allow_html=True)

    if not name.strip():
        st.warning("⚠️ You must enter your name before proceeding.")
        return

    # Enhanced glowing name effect
    st.markdown(
        f"<div class='welcome-text'>Welcome, <span class='glowing-name'>{name}</span>!</div>", 
        unsafe_allow_html=True
    )

    # Navigation Buttons with perfect alignment and glow
    st.markdown('<div class="button-row">', unsafe_allow_html=True)
    
    # Learn Button
    if st.button("📚 Learn About Phishing", key="learn_btn", 
                help="Start with the learning module"):
        st.switch_page("pages/Learn.py")
    st.markdown(
        """
        <script>
        document.querySelector('[data-testid="baseButton-secondary"]').className = "learn-btn";
        </script>
        """,
        unsafe_allow_html=True
    )
    
    # Quiz Button
    if st.button("🧠 Take the Quiz", key="quiz_btn", 
                help="Test your phishing detection skills"):
        st.switch_page("pages/Quiz.py")
    st.markdown(
        """
        <script>
        document.querySelectorAll('[data-testid="baseButton-secondary"]')[1].className = "quiz-btn";
        </script>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Student Type Section
    st.markdown("<div class='student-section'>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center; color:#00ffe0;'>🎓 Are you an International or German student?</h4>", 
                unsafe_allow_html=True)
    
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