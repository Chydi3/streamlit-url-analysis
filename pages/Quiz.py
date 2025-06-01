import streamlit as st
import time
import os
import csv
import random
from collections import defaultdict
import pandas as pd
import plotly.express as px
from io import BytesIO
import base64
import pygame

# ------------------ Audio Setup ------------------
def audio_to_base64(file_path: str) -> str:
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# Load WAV files from same directory as this script
base_dir = os.path.dirname(__file__)
SUCCESS_SOUND = audio_to_base64(os.path.join(base_dir, "success.wav"))
ERROR_SOUND   = audio_to_base64(os.path.join(base_dir, "error.wav"))

# Streamlit audio playback via hidden HTML <audio>
def play_sound(sound_base64):
    """Embed and autoplay a Base64-encoded WAV via an HTML tag."""
    audio_html = f"""
<audio autoplay="true" style="display:none">
    <source src="data:audio/wav;base64,{sound_base64}" type="audio/wav">
</audio>
"""
    st.markdown(audio_html, unsafe_allow_html=True)

# (Optional) initialize pygame mixer if available
try:
    pygame.mixer.init()
except:
    pass

# ------------------ Custom Rerun Function ------------------
def rerun():
    try:
        st.experimental_rerun()
    except AttributeError:
        st.stop()

# ------------------ Helper Function to Reset Quiz State ------------------
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
    # *** NEW: initialize per-question timer log
    st.session_state.question_times = []

# ------------------ Custom Background & Theming ------------------
st.markdown(
    """
    <style>
    /* Main container background */
    .reportview-container, .main .block-container {
        background: url("https://images.unsplash.com/photo-1526491109311-37c7dbf2f9b3?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80") no-repeat center center fixed;
        background-size: cover;
    }
    /* Sidebar background */
    .sidebar .sidebar-content {
        background: url("https://images.unsplash.com/photo-1532283411789-43c72de429bc?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80") no-repeat center center;
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ------------------ Session State Initialization ------------------
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "player_name" not in st.session_state:
    st.session_state.player_name = "Guest"
if "score" not in st.session_state:
    st.session_state.score = 0
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "feedback" not in st.session_state:
    st.session_state.feedback = ""
if "is_correct" not in st.session_state:
    st.session_state.is_correct = None
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = []
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = defaultdict(int)
if "timer" not in st.session_state:
    st.session_state.timer = 0
if "custom_url" not in st.session_state:
    st.session_state.custom_url = ""
if "user_answers" not in st.session_state:
    st.session_state.user_answers = []
if "sub_answers" not in st.session_state:
    st.session_state.sub_answers = []  # To store sub-question responses per quiz item
if "show_timer" not in st.session_state:
    st.session_state.show_timer = False  # Not visible to gamers
if "question_start_time" not in st.session_state:
    st.session_state.question_start_time = time.time()
if "quiz_active" not in st.session_state:
    st.session_state.quiz_active = True
if "question_start_time" not in st.session_state:
    st.session_state.question_start_time = time.time()
if "question_times" not in st.session_state:
    st.session_state.question_times = []
if "sub_answered" not in st.session_state:
    st.session_state.sub_answered = False

# ------------------ Persistent Performance Tracking Functions ------------------
def save_quiz_result():
    """Save the current quiz result to a CSV file."""
    player_name = st.session_state.player_name
    score = st.session_state.score
    total_questions = len(phishing_questions)
    accuracy = st.session_state.score / total_questions * 100
    elapsed_time = time.time() - st.session_state.timer
    formatted_time = format_time(elapsed_time)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    # Serialize your per‑question timings into a semicolon‑delimited string
    times_str = ";".join(f"{t:.1f}" for t in st.session_state.question_times)
    
    file_name = "quiz_results.csv"
    file_exists = os.path.isfile(file_name)
    with open(file_name, mode="a", newline="") as csv_file:
        writer = csv.writer(csv_file)
        if not file_exists:

        # add your new header column "Per-Question Times (s)"
            writer.writerow([
                "Player Name", "Score", "Total Questions",
                "Accuracy (%)", "Time Taken",
                "Per-Question Times (s)",  # ← new header
                "Timestamp"
            ])
            writer.writerow(["Player Name", "Score", "Total Questions", "Accuracy (%)", "Time Taken", "Timestamp"])
        writer.writerow([player_name, score, total_questions, f"{accuracy:.2f}", formatted_time, timestamp])

def load_quiz_results(filter_name):
    """Load and filter quiz results from the CSV file, drop duplicates, and reset index."""
    file_name = "quiz_results.csv"
    if not os.path.exists(file_name):
        st.write("No quiz results available.")
        return None
    df = pd.read_csv(file_name)
    if filter_name:
        df = df[df["Player Name"].str.contains(filter_name, case=False, na=False)]
    df = df.drop_duplicates(subset=["Player Name"], keep="last").reset_index(drop=True)
    df.index += 1  # Serial numbering starts at 1
    return df

def reset_quiz_results():
    """Delete the CSV file to clear all stored quiz results."""
    file_name = "quiz_results.csv"
    if os.path.exists(file_name):
        os.remove(file_name)
        st.sidebar.write("Quiz results have been reset.")
    else:
        st.sidebar.write("No quiz results found to reset.")

# ------------------ Welcome Page ------------------
def welcome_page():
    # Reset quiz state for new user login
    reset_quiz_state()
    
    st.title("Welcome to the URL Quiz & Learning Game!")
    st.write("Before we begin, please enter your name or code.")
    name_input = st.text_input("Enter your name or code:", value="Guest", key="welcome_name_input")
    if st.button("Play Game"):
        st.session_state.player_name = name_input
        st.session_state.quiz_started = True

# ------------------ Quiz Functions ------------------
def start_quiz():
    st.session_state.quiz_data = phishing_questions
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.streak = 0
    st.session_state.timer = time.time()
    st.session_state.user_answers = []
    st.session_state.sub_answers = []  # Reset sub answers
    st.session_state.question_start_time = time.time()
    st.session_state.quiz_active = True
    st.session_state.answered = False
    st.session_state.sub_answered = False

def check_answer(user_answer, correct_answer):
    elapsed = time.time() - st.session_state.question_start_time
    st.session_state.question_times.append(elapsed)
    if user_answer == correct_answer:
        st.session_state.score += 1
        st.session_state.streak += 1
        st.session_state.is_correct = True
        st.session_state.feedback = f"✅ Correct! {phishing_questions[st.session_state.current_q]['explanation']}"
        play_sound(SUCCESS_SOUND)
    else:
        st.session_state.streak = 0
        st.session_state.is_correct = False
        st.session_state.feedback = f"❌ Wrong! {phishing_questions[st.session_state.current_q]['explanation']}"
        play_sound(ERROR_SOUND)
    
    st.session_state.user_answers.append({
        "question": phishing_questions[st.session_state.current_q]["question"],
        "user_answer": user_answer,
        "correct_answer": correct_answer,
        "explanation": phishing_questions[st.session_state.current_q]["explanation"]
    })
    
    st.session_state.answered = True

def check_sub_answers(sub_responses):
    st.session_state.sub_answers.append({
        "question": phishing_questions[st.session_state.current_q]["question"],
        "sub_answers": sub_responses
    })
    st.session_state.sub_answered = True

def next_question():
    st.session_state.current_q += 1
    st.session_state.answered = False
    st.session_state.feedback = ""
    st.session_state.is_correct = None
    st.session_state.sub_answered = False
    st.session_state.question_start_time = time.time()

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    sec = seconds % 60
    if hours > 0:
        return f"{hours} hr {minutes} min {sec:.0f} sec"
    elif minutes > 0:
        return f"{minutes} min {sec:.0f} sec"
    else:
        return f"{sec:.0f} sec"

def end_quiz():
    elapsed_time = time.time() - st.session_state.timer
    st.subheader("Quiz Completed! 📄")
    st.write(f"**Total Score:** {st.session_state.score} / {len(phishing_questions)}")
    st.write(f"**Accuracy:** {st.session_state.score / len(phishing_questions) * 100:.2f}%")
    st.write(f"**Time Taken:** {format_time(elapsed_time)}")
    
    save_quiz_result()

    # --- Celebration Effect Based on Performance ---
    accuracy = (st.session_state.score / len(phishing_questions)) * 100
    if accuracy >= 70:
        st.balloons()
    else:
        st.snow()

    st.write("### Summary Insights")
    if st.session_state.score == len(phishing_questions):
        st.write("🎉 Perfect score! You're a phishing detection expert!")
    else:
        st.write("🔍 Here are some tips to improve:")
        st.write("- Pay close attention to the domain and subdomain of URLs.")
        st.write("- Look for subtle differences in URLs that might indicate phishing.")
        st.write("- Practice more to improve your accuracy.")
    
    st.write("### How do you feel about your performance?")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🤔"):
            st.write("You seem unsure. Keep practicing!")
    with col2:
        if st.button("😃"):
            st.write("Great job! Keep it up!")
    with col3:
        if st.button("🎉"):
            st.write("Celebrating your success!")
    
    st.session_state.leaderboard[st.session_state.score] += 1

    # --- Review Mistakes Section ---
    st.write("### Review Mistakes")
    mistakes = [ans for ans in st.session_state.user_answers if ans["user_answer"] != ans["correct_answer"]]
    if mistakes:
        for idx, mistake in enumerate(mistakes, start=1):
            st.write(f"**Mistake {idx}:**")
            url_for_mistake = phishing_questions[st.session_state.user_answers.index(mistake)]["url"]
            st.write(f"**URL:** {url_for_mistake}")
            st.write(f"**Question:** {mistake['question']}")
            st.write(f"**Your Answer:** {mistake['user_answer']}")
            st.write(f"**Correct Answer:** {mistake['correct_answer']}")
            st.write(f"**Explanation:** {mistake['explanation']}")
            st.markdown("[Learn More about Phishing](https://example.com/phishing)")
            st.write("---")
    else:
        st.write("Excellent! You made no mistakes.")
    
    # --- Interactive Tip of the Day ---
    tips = [
        "Always check the URL carefully for misspellings.",
        "Look for HTTPS and the padlock icon, but remember that HTTPS alone does not guarantee safety.",
        "Be cautious of shortened URLs; expand them before clicking.",
        "Hover over links to see the actual URL destination.",
        "Check for unusual subdomains or extra characters in the URL."
    ]
    tip = random.choice(tips)
    st.write("### Tip of the Day")
    st.info(f"**Tip:** {tip}")
    
    # --- Navigation Buttons at End of Quiz ---
    st.write("### What would you like to do next?")
    
    # Button to go to Learn Page (redirects to Learn page)
    if st.button("Go to Learn Page"):
        st.session_state.quiz_started = False  # Reset so welcome page appears if needed
        st.switch_page("pages/Learn.py")  # ✅ Correct relative path
    
    # Restart Quiz: Reset state and go back to the welcome page (name input/start quiz)
    colA, colB = st.columns(2)
    with colA:
        if st.button("Restart Quiz"):
            st.session_state.quiz_started = False
            reset_quiz_state()
            rerun()  # This will show the welcome page again
    with colB:
        if st.button("End Quiz"):
            st.session_state.quiz_started = False
            reset_quiz_state()
            rerun()  # End quiz and return to welcome page

# ------------------ phishing_quiz Definition ------------------  
def phishing_quiz():
    if not st.session_state.quiz_active:
        st.write("Quiz has ended. Please restart to play again.")
        return

    st.title("🎯 URL Phishing Quiz")

    # --- Animated Progress Bar for Quiz Progress ---
    q_index = st.session_state.current_q
    total_questions = len(phishing_questions)
    progress_percent = int((q_index / total_questions) * 100)

    with st.container():
        st.markdown(f"**Progress:** {progress_percent}% complete")
        st.progress(progress_percent)

    # --- Display Question ---
    if q_index < total_questions:
        question = phishing_questions[q_index]
        
        st.write(f"**Question {q_index + 1} of {total_questions}**")
        
        st.markdown(
            f"""
            <div style='background-color: #d4edda; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                <h5 style='color: #155724;'>URL: {question["url"]}</h5>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.write(question["question"])

        # Main answer input
        choice = st.radio(
            "Select an answer:",
            question["options"],
            index=None,                           # ← no default selection
            key=f"q{q_index}",
            disabled=st.session_state.answered
        )
        
        if st.button("Submit", key=f"submit_{q_index}") and not st.session_state.answered:
            check_answer(choice, question["answer"])

        # Display feedback after answering
        if st.session_state.answered:
            if st.session_state.is_correct:
                st.success(st.session_state.feedback)
            else:
                st.error(st.session_state.feedback)

             # Show Next only once they've answered
            if st.button("Next Question", key=f"next_{q_index}", on_click=next_question):
                pass
        else:
            # Warn if they try to proceed without answering
            st.warning("🚨 Please select an answer before proceeding.")
    else:
        end_quiz()

def custom_quiz():
    user_url = st.text_input("Enter a URL to analyze:")
    if st.button("Analyze"):
        st.session_state.custom_url = user_url
        st.write(f"Analysis of {user_url}:")
        st.write("**Domain:** example.com")
        st.write("**Subdomain:** secure")
        st.write("**Path:** /login")

# ------------------ Full List of 14 Quiz Questions ------------------
phishing_questions = [
    {
        "url": "https://google.de",
        "question": "When you type the above link into a web browser, what website would you see?",
        "options": ["Amazon's website", "Facebook's website", "Twitter's website", "A website which is not listed", "Other"],
        "answer": "A website which is not listed",
        "explanation": "This is Google's German domain (google.de), not Amazon, Facebook, or Twitter."
    },
    {
        "url": "https://www.bahn.de",
        "question": "When you type the above link into a web browser, what website would you see?",
        "options": ["Travel Buddy's website", "Flixbus's website", "Booking's website", "Ebay's website", "A website which is not listed", "Other"],
        "answer": "A website which is not listed",
        "explanation": "This is the official website of Deutsche Bahn (German railway service)."
    },
    {
        "url": "https://maengelmelder.Grossdorfberg.de",
        "question": "When you type the above link into a web browser, what website would you see?",
        "options": ["Vogelsbrück's website", "Maengelmelder's website", "Grossdorfberg's website", "A website which is not listed", "Other"],
        "answer": "Grossdorfberg's website",
        "explanation": "Main domain: Grossdorfberg.de. 'maengelmelder' is a subdomain for their complaint service.",
        "sub_questions": [
            {
                "question": "How safe do you think it would be to click on the link above if you saw it in an email from someone you know?",
                "options": ["Not safe", "Somewhat unsafe", "Neutral", "Somewhat safe", "Very safe"]
            },
            {
                "question": "How confident are you that this URL leads to a platform where you can report problems?",
                "options": ["Very Confident", "Somewhat Confident", "Less Confident", "Not Confident at all"]
            }
        ]
    },
    {
        "url": "https://buergerbeteiligung.Kleinbachhausen.de/",
        "question": "When you type the above link into a web browser, what website would you see?",
        "options": ["Buergstadt's website", "Kleinbachhausen's website", "Buergerbeteiligung's website", "A website which is not listed", "Other"],
        "answer": "Kleinbachhausen's website",
        "explanation": "Main domain: Kleinbachhausen.de. Subdomain: buergerbeteiligung (citizen participation).",
        "sub_questions": [
            {
                "question": "How safe do you think it would be to click on the link above if you saw it in an email from someone you know?",
                "options": ["Not safe", "Somewhat unsafe", "Neutral", "Somewhat safe", "Very safe"]
            },
            {
                "question": "How confident are you that this URL leads to a platform where you can report problems?",
                "options": ["Very Confident", "Somewhat Confident", "Less Confident", "Not Confident at all"]
            }
        ]
    },
    {
        "url": "https://onlinedienste.Neukleindorf.de/",
        "question": "When you type the above link into a web browser, what website would you see?",
        "options": ["Altbrück's website", "Onlinedienste's website", "Neukleindorf's website", "A website which is not listed", "Other"],
        "answer": "Neukleindorf's website",
        "explanation": "Main domain: Neukleindorf.de. Subdomain: onlinedienste (online services).",
        "sub_questions": [
            {
                "question": "How safe do you think it would be to click on the link above if you saw it in an email from someone you know?",
                "options": ["Not safe", "Somewhat unsafe", "Neutral", "Somewhat safe", "Very safe"]
            },
            {
                "question": "How confident are you that this URL leads to a platform where you can report problems?",
                "options": ["Very Confident", "Somewhat Confident", "Less Confident", "Not Confident at all"]
            }
        ]
    },
    {
        "url": "https://waldhof.ceasy.de/",
        "question": "When you type the above link into a web browser, what website would you see?",
        "options": ["Schwanburg's website", "Waldhof's website", "Ceasy's website", "A website which is not listed", "Other"],
        "answer": "Waldhof's website",
        "explanation": "Main domain: waldhof.de. 'ceasy' is a subdomain (e.g., a service).",
        "sub_questions": [
            {
                "question": "How safe do you think it would be to click on the link above if you saw it in an email from someone you know?",
                "options": ["Not safe", "Somewhat unsafe", "Neutral", "Somewhat safe", "Very safe"]
            },
            {
                "question": "How confident are you that this URL leads to a platform where you can report problems?",
                "options": ["Very Confident", "Somewhat Confident", "Less Confident", "Not Confident at all"]
            }
        ]
    },
    {
        "url": "https://langensteinburg.emsos.de/",
        "question": "When you type the above link into a web browser, what website would you see?",
        "options": ["Langensteinburg's website", "Rosenbach's website", "Emsos's website", "A website which is not listed", "Other"],
        "answer": "Langensteinburg's website",
        "explanation": "Main domain: langensteinburg.de. 'emsos' is a subdomain.",
        "sub_questions": [
            {
                "question": "How safe do you think it would be to click on the link above if you saw it in an email from someone you know?",
                "options": ["Not safe", "Somewhat unsafe", "Neutral", "Somewhat safe", "Very safe"]
            },
            {
                "question": "How confident are you that this URL leads to a platform where you can report problems?",
                "options": ["Very Confident", "Somewhat Confident", "Less Confident", "Not Confident at all"]
            }
        ]
    },
    {
        "url": "https://dorfhausenstadt.anliegenmanagement.de/",
        "question": "When you type the above link into a web browser, what website would you see?",
        "options": ["Anliegenmanagement's website", "Dorfhausenstadt's website", "Bergfeldenheim's website", "A website which is not listed", "Other"],
        "answer": "Dorfhausenstadt's website",
        "explanation": "Main domain: dorfhausenstadt.de. 'anliegenmanagement' is a subdomain.",
        "sub_questions": [
            {
                "question": "How safe do you think it would be to click on the link above if you saw it in an email from someone you know?",
                "options": ["Not safe", "Somewhat unsafe", "Neutral", "Somewhat safe", "Very safe"]
            },
            {
                "question": "How confident are you that this URL leads to a platform where you can report problems?",
                "options": ["Very Confident", "Somewhat Confident", "Less Confident", "Not Confident at all"]
            }
        ]
    },
    {
        "url": "https://grossdorfberg.maengelmelder.de",
        "question": "When you type the above link into a web browser, what website would you see?",
        "options": ["Grossdorfberg's website", "Maengelmelder's website", "Vogelsbrück's website", "A website which is not listed", "Other"],
        "answer": "Maengelmelder's website",
        "explanation": "Main domain: maengelmelder.de. 'grossdorfberg' is a subdomain.",
        "sub_questions": [
            {
                "question": "How safe do you think it would be to click on the link above if you saw it in an email from someone you know?",
                "options": ["Not safe", "Somewhat unsafe", "Neutral", "Somewhat safe", "Very safe"]
            },
            {
                "question": "How confident are you that this URL leads to a platform where you can report problems?",
                "options": ["Very Confident", "Somewhat Confident", "Less Confident", "Not Confident at all"]
            }
        ]
    },
    {
        "url": "https://kleinbachhausen.buergerbeteiligung.de/",
        "question": "When you type the above link into a web browser, what website would you see?",
        "options": ["Kleinbachhausen's website", "Buergerbeteiligung's website", "Buergstadt's website", "A website which is not listed", "Other"],
        "answer": "A website which is not listed",
        "explanation": "Main domain: buergerbeteiligung.de (if unregistered). No valid website exists.",
        "sub_questions": [
            {
                "question": "How safe do you think it would be to click on the link above if you saw it in an email from someone you know?",
                "options": ["Not safe", "Somewhat unsafe", "Neutral", "Somewhat safe", "Very safe"]
            },
            {
                "question": "How confident are you that this URL leads to a platform where you can report problems?",
                "options": ["Very Confident", "Somewhat Confident", "Less Confident", "Not Confident at all"]
            }
        ]
    },
    {
        "url": "https://neukleindorf.onlinedienste.de/",
        "question": "When you type the above link into a web browser, what website would you see?",
        "options": ["Onlinedienste's website", "Neukleindorf's website", "Altbrück's website", "A website which is not listed", "Other"],
        "answer": "Onlinedienste's website",
        "explanation": "Main domain: onlinedienste.de. 'neukleindorf' is a subdomain.",
        "sub_questions": [
            {
                "question": "How safe do you think it would be to click on the link above if you saw it in an email from someone you know?",
                "options": ["Not safe", "Somewhat unsafe", "Neutral", "Somewhat safe", "Very safe"]
            },
            {
                "question": "How confident are you that this URL leads to a platform where you can report problems?",
                "options": ["Very Confident", "Somewhat Confident", "Less Confident", "Not Confident at all"]
            }
        ]
    },
    {
        "url": "https://ceasy.waldhof.de/",
        "question": "When you type the above link into a web browser, what website would you see?",
        "options": ["Schwanburg's website", "Waldhof's website", "Ceasy's website", "A website which is not listed", "Other"],
        "answer": "Waldhof's website",
        "explanation": "Main domain: waldhof.de. 'ceasy' is a subdomain (e.g., a service).",
        "sub_questions": [
            {
                "question": "How safe do you think it would be to click on the link above if you saw it in an email from someone you know?",
                "options": ["Not safe", "Somewhat unsafe", "Neutral", "Somewhat safe", "Very safe"]
            },
            {
                "question": "How confident are you that this URL leads to a platform where you can report problems?",
                "options": ["Very Confident", "Somewhat Confident", "Less Confident", "Not Confident at all"]
            }
        ]
    },
    {
        "url": "https://emsos.langensteinburg.de/",
        "question": "When you type the above link into a web browser, what website would you see?",
        "options": ["Langensteinburg's website", "Rosenbach's website", "Emsos's website", "A website which is not listed", "Other"],
        "answer": "Langensteinburg's website",
        "explanation": "Main domain: langensteinburg.de. 'emsos' is a subdomain.",
        "sub_questions": [
            {
                "question": "How safe do you think it would be to click on the link above if you saw it in an email from someone you know?",
                "options": ["Not safe", "Somewhat unsafe", "Neutral", "Somewhat safe", "Very safe"]
            },
            {
                "question": "How confident are you that this URL leads to a platform where you can report problems?",
                "options": ["Very Confident", "Somewhat Confident", "Less Confident", "Not Confident at all"]
            }
        ]
    },
    {
        "url": "https://anliegenmanagement.dorfhausenstadt.de/",
        "question": "When you type the above link into a web browser, what website would you see?",
        "options": ["Anliegenmanagement's website", "Dorfhausenstadt's website", "Bergfeldenheim's website", "A website which is not listed", "Other"],
        "answer": "Dorfhausenstadt's website",
        "explanation": "Main domain: dorfhausenstadt.de. 'anliegenmanagement' is a subdomain.",
        "sub_questions": [
            {
                "question": "How safe do you think it would be to click on the link above if you saw it in an email from someone you know?",
                "options": ["Not safe", "Somewhat unsafe", "Neutral", "Somewhat safe", "Very safe"]
            },
            {
                "question": "How confident are you that this URL leads to a platform where you can report problems?",
                "options": ["Very Confident", "Somewhat Confident", "Less Confident", "Not Confident at all"]
            }
        ]
    }
]

# ------------------ Main App ------------------
def main_app():
    st.title("🔐 URL Quiz & Learning Game")
    
    # ------------------ Welcome Page Handling ------------------
    if not st.session_state.quiz_started:
        welcome_page()
        st.stop()
    
    # ------------------ Sidebar: Minimal User Info for Gamers ------------------
    st.sidebar.header("Welcome!")
    st.sidebar.write(f"### Welcome, {st.session_state.player_name}!")
    
    # ------------------ Display the Quiz ------------------
    phishing_quiz()

if __name__ == "__main__":
    main_app()