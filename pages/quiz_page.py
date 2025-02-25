import streamlit as st
import time
from collections import defaultdict

# Initialize session state variables
if "score" not in st.session_state:
    st.session_state["score"] = 0
if "current_q" not in st.session_state:
    st.session_state["current_q"] = 0
if "answered" not in st.session_state:
    st.session_state["answered"] = False  # Track if user has answered the current question
if "feedback" not in st.session_state:
    st.session_state["feedback"] = ""  # Store feedback message
if "is_correct" not in st.session_state:
    st.session_state["is_correct"] = None  # Track if the answer is correct or not
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = []
if 'streak' not in st.session_state:
    st.session_state.streak = 0
if 'leaderboard' not in st.session_state:
    st.session_state.leaderboard = defaultdict(int)
if 'timer' not in st.session_state:
    st.session_state.timer = 0
if 'custom_url' not in st.session_state:
    st.session_state.custom_url = ""
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = []  # Track user answers for the end-of-quiz report
if 'show_timer' not in st.session_state:
    st.session_state.show_timer = False  # Toggle for timer
if 'question_start_time' not in st.session_state:
    st.session_state.question_start_time = time.time()  # Track time per question

# Sample quiz questions for phishing quiz
phishing_questions = [
    {
        "url": "https://google.de",
        "question": "When you type the above link into a web browser, what website would you see?",
        "options": ["Amazon’s website", "Facebook’s website", "Twitter’s website", "A website which is not listed", "Other"],
        "answer": "A website which is not listed",
        "explanation": "This is Google's German domain, not Amazon, Facebook, or Twitter."
    },
    {
        "url": "https://www.bahn.de",
        "question": "When you type the above link into a web browser, what website would you see?",
        "options": ["Travel Buddy's website", "Flixbus’s website", "Booking's website", "Ebay’s website", "A website which is not listed", "Other"],
        "answer": "A website which is not listed",
        "explanation": "This is the official website of Deutsche Bahn (German railway service)."
    },
    {
        "url": "https://maengelmelder.Grossdorfberg.de",
        "question": "When you type the above link into a web browser, what website would you see?",
        "options": ["Vogelsbrück’s website", "Maengelmelder’s website", "Grossdorfberg’s website", "A website which is not listed", "Other"],
        "answer": "Grossdorfberg’s website",
        "explanation": "The subdomain suggests this is a complaint-reporting service for Grossdorfberg."
    },
    {
        "url": "https://buergerbeteiligung.Kleinbachhausen.de/",
        "question": "When you type the above link into a web browser, what website would you see?",
        "options": ["Buergstadt’s website", "Kleinbachhausen’s website", "Buergerbeteiligung’s website", "A website which is not listed", "Other"],
        "answer": "Kleinbachhausen’s website",
        "explanation": "The domain structure indicates a citizen participation platform for Kleinbachhausen."
    },
    {
        "url": "https://onlinedienste.Neukleindorf.de/",
        "question": "When you type the above link into a web browser, what website would you see?",
        "options": ["Altbrück’s website", "Onlinedienste’s website", "Neukleindorf’s website", "A website which is not listed", "Other"],
        "answer": "Neukleindorf’s website",
        "explanation": "The subdomain 'onlinedienste' suggests digital services for Neukleindorf."
    },
    {
        "url": "https://waldhof.ceasy.de/",
        "question": "When you type the above link into a web browser, what website would you see?",
        "options": ["Maerker’s website", "Waldhof’s website", "Schwanburg’s website", "A website which is not listed", "Other"],
        "answer": "Waldhof’s website",
        "explanation": "The subdomain 'waldhof' indicates a service related to Waldhof on the 'ceasy' platform."
    },
    {
        "url": "https://langensteinburg.emsos.de/",
        "question": "When you type the above link into a web browser, what website would you see?",
        "options": ["Emsos’s website", "Langensteinburg’s website", "Rosenbach’s website", "A website which is not listed", "Other"],
        "answer": "Langensteinburg’s website",
        "explanation": "The subdomain 'langensteinburg' suggests a service for this city on 'emsos.de'."
    },
    {
        "url": "https://dorfhausenstadt.anliegenmanagement.de/",
        "question": "When you type the above link into a web browser, what website would you see?",
        "options": ["Dorfhausenstadt’s website", "Bergfeldenheim’s website", "Anliegenmanagement’s website", "A website which is not listed", "Other"],
        "answer": "Dorfhausenstadt’s website",
        "explanation": "The subdomain 'dorfhausenstadt' suggests a local issue-management platform for this town."
    },
    {
        "url": "https://grossdorfberg.maengelmelder.de",
        "question": "When you type the above link into a web browser, what website would you see?",
        "options": ["Grossdorfberg’s website", "Maengelmelder’s website", "Vogelsbrück’s website", "A website which is not listed", "Other"],
        "answer": "Grossdorfberg’s website",
        "explanation": "'maengelmelder' is a platform for reporting issues, and the subdomain links it to Grossdorfberg."
    },
    {
        "url": "https://kleinbachhausen.buergerbeteiligung.de/",
        "question": "When you type the above link into a web browser, what website would you see?",
        "options": ["Kleinbachhausen’s website", "Buergerbeteiligung’s website", "Buergstadt’s website", "A website which is not listed", "Other"],
        "answer": "Kleinbachhausen’s website",
        "explanation": "The structure shows it is for Kleinbachhausen’s citizen participation."
    },
    {
        "url": "https://neukleindorf.onlinedienste.de/",
        "question": "When you type the above link into a web browser, what website would you see?",
        "options": ["Onlinedienste’s website", "Neukleindorf’s website", "Altbrück’s website", "A website which is not listed", "Other"],
        "answer": "Neukleindorf’s website",
        "explanation": "'onlinedienste' indicates online services for Neukleindorf."
    },
    {
        "url": "https://ceasy.waldhof.de/",
        "question": "When you type the above link into a web browser, what website would you see?",
        "options": ["Schwanburg’s website", "Waldhof’s website", "Ceasy’s website", "A website which is not listed", "Other"],
        "answer": "Waldhof’s website",
        "explanation": "'waldhof.de' is the domain, and 'ceasy' is likely a service provider."
    },
    {
        "url": "https://emsos.langensteinburg.de/",
        "question": "When you type the above link into a web browser, what website would you see?",
        "options": ["Langensteinburg’s website", "Rosenbach’s website", "Emsos’s website", "A website which is not listed", "Other"],
        "answer": "Langensteinburg’s website",
        "explanation": "'langensteinburg.de' indicates the city, and 'emsos' could be a service provider."
    },
    {
        "url": "https://anliegenmanagement.dorfhausenstadt.de/",
        "question": "When you type the above link into a web browser, what website would you see?",
        "options": ["Anliegenmanagement’s website", "Dorfhausenstadt’s website", "Bergfeldenheim’s website", "A website which is not listed", "Other"],
        "answer": "Dorfhausenstadt’s website",
        "explanation": "The structure indicates an issue management service for Dorfhausenstadt."
    }
]

def start_quiz():
    st.session_state.quiz_data = phishing_questions  # Use phishing questions directly
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.streak = 0
    st.session_state.timer = time.time()
    st.session_state.user_answers = []  # Reset user answers
    st.session_state.question_start_time = time.time()  # Reset question timer

def check_answer(user_answer, correct_answer):
    if user_answer == correct_answer:
        st.session_state.score += 1
        st.session_state.streak += 1
        st.session_state.is_correct = True
        st.session_state.feedback = f"✅ Correct! {phishing_questions[st.session_state.current_q]['explanation']}"
    else:
        st.session_state.streak = 0
        st.session_state.is_correct = False
        st.session_state.feedback = f"❌ Wrong! {phishing_questions[st.session_state.current_q]['explanation']}"
    
    # Record user answer for end-of-quiz report
    st.session_state.user_answers.append({
        "question": phishing_questions[st.session_state.current_q]["question"],
        "user_answer": user_answer,
        "correct_answer": correct_answer,
        "explanation": phishing_questions[st.session_state.current_q]["explanation"]
    })
    
    st.session_state["answered"] = True  # Mark question as answered

def next_question():
    st.session_state["current_q"] += 1
    st.session_state["answered"] = False  # Reset for next question
    st.session_state["feedback"] = ""  # Clear feedback
    st.session_state["is_correct"] = None  # Reset correctness state
    st.session_state.question_start_time = time.time()  # Reset timer for next question

def end_quiz():
    elapsed_time = time.time() - st.session_state.timer
    st.subheader("Quiz Completed! 📄")
    st.write(f"**Total Score:** {st.session_state.score} / {len(phishing_questions)}")
    st.write(f"**Accuracy:** {st.session_state.score / len(phishing_questions) * 100:.2f}%")
    st.write(f"**Time Taken:** {elapsed_time:.2f} seconds")

    # Table Comparing User Answers vs. Correct Answers
    st.write("### Answer Comparison Table")
    st.write("| Question | Your Answer | Correct Answer | Explanation |")
    st.write("|----------|-------------|----------------|-------------|")
    for i, answer in enumerate(st.session_state.user_answers):
        st.write(f"| {answer['question']} | {answer['user_answer']} | {answer['correct_answer']} | {answer['explanation']} |")

    # Common Mistakes & Explanations
    incorrect_answers = [ans for ans in st.session_state.user_answers if ans['user_answer'] != ans['correct_answer']]
    if incorrect_answers:
        st.write("### Common Mistakes & Explanations")
        for mistake in incorrect_answers:
            st.write(f"**Question:** {mistake['question']}")
            st.write(f"**Your Answer:** {mistake['user_answer']}")
            st.write(f"**Correct Answer:** {mistake['correct_answer']}")
            st.write(f"**Explanation:** {mistake['explanation']}")
            st.write("---")

    # Summary Insights
    st.write("### Summary Insights 💡")
    if st.session_state.score == len(phishing_questions):
        st.write("🎉 Perfect score! You're a phishing detection expert!")
    else:
        st.write("🔍 Here are some tips to improve:")
        st.write("- Pay close attention to the domain and subdomain of URLs.")
        st.write("- Look for subtle differences in URLs that might indicate phishing.")
        st.write("- Practice more to improve your accuracy.")

    # Emoji Reactions
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

def custom_quiz():
    user_url = st.text_input("Enter a URL to analyze:")
    if st.button("Analyze"):
        st.session_state.custom_url = user_url
        st.write(f"Analysis of {user_url}:")
        st.write("**Domain:** example.com")
        st.write("**Subdomain:** secure")
        st.write("**Path:** /login")

def phishing_quiz():
    st.title("🎯 URL Phishing Quiz")
    q_index = st.session_state["current_q"]

    if q_index < len(phishing_questions):
        question = phishing_questions[q_index]
        st.write(f"**Question {q_index + 1} of {len(phishing_questions)}**")

        # Display the URL in bold and red (unclickable)
        st.markdown(
            f'<p style="font-weight: bold; color: red;">URL: {question["url"]}</p>',
            unsafe_allow_html=True
        )

        st.write(question["question"])

        # Timer (optional)
        if st.session_state.show_timer:
            time_elapsed = int(time.time() - st.session_state.question_start_time)
            st.markdown(f"**⏳ Time elapsed: {time_elapsed} seconds**")

        # User choice
        choice = st.radio("Select an answer:", question["options"], key=f"q{q_index}", disabled=st.session_state["answered"])

        # Submit button logic
        if st.button("Submit") and not st.session_state["answered"]:
            check_answer(choice, question["answer"])

        # Display styled feedback if answered
        if st.session_state["answered"]:
            if st.session_state["is_correct"]:
                st.success(st.session_state["feedback"])  # Green banner for correct answer
            else:
                st.error(st.session_state["feedback"])  # Red banner for incorrect answer

            # Show "Next Question" button
            if st.button("Next Question"):
                next_question()
                st.rerun()  # Refresh for next question

    else:
        end_quiz()

# Main app
st.title("🔐 URL Quiz & Learning Game")
st.sidebar.header("Quiz Settings")
if st.sidebar.button("Start Quiz"):
    start_quiz()

# Toggle for timer
st.session_state.show_timer = st.sidebar.checkbox("Enable Timer ⏳")

# Display the phishing quiz
phishing_quiz()

if st.sidebar.button("View Leaderboard"):
    st.sidebar.write("### Leaderboard 🏆")
    for score, count in sorted(st.session_state.leaderboard.items(), reverse=True):
        st.sidebar.write(f"Score {score}: {count} players")

st.sidebar.header("Custom Quiz Mode ✍️")
custom_quiz()