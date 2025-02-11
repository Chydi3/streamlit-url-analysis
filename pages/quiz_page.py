import streamlit as st

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

# Sample quiz questions
questions = [
    {"question": "Which of these URLs is likely phishing?", 
     "options": ["https://www.paypal.com", "https://paypa1.com/login", "https://secure.paypal.com"],
     "answer": "https://paypa1.com/login",
     "explanation": "The URL uses 'paypa1' instead of 'paypal', which is a common phishing trick."
     },
    
    {"question": "What should you check first in a URL?", 
     "options": ["The domain name", "The font style", "The background color"],
     "answer": "The domain name",
     "explanation": "The domain name is crucial in verifying authenticity."}
    
]

def quiz():
    st.title("🎯 URL Phishing Quiz")

    q_index = st.session_state["current_q"]

    if q_index < len(questions):
        question = questions[q_index]
        st.write(f"**Question {q_index + 1} of {len(questions)}**")
        st.write(question["question"])

        # User choice
        choice = st.radio("Select an answer:", question["options"], key=f"q{q_index}", disabled=st.session_state["answered"])

        # Submit button logic
        if st.button("Submit") and not st.session_state["answered"]:
            st.session_state["answered"] = True  # Mark question as answered

            if choice == question["answer"]:
                st.session_state["score"] += 1
                st.session_state["is_correct"] = True
                st.session_state["feedback"] = f"✅ Correct! {question['explanation']}"
            else:
                st.session_state["is_correct"] = False
                st.session_state["feedback"] = f"❌ Wrong! {question['explanation']}"

            st.rerun()  # Rerun to show feedback without resetting state

        # Display styled feedback if answered
        if st.session_state["answered"]:
            if st.session_state["is_correct"]:
                st.success(st.session_state["feedback"])  # Green banner for correct answer
            else:
                st.error(st.session_state["feedback"])  # Red banner for incorrect answer

            # Move to next question
            if st.button("Next Question"):
                st.session_state["current_q"] += 1
                st.session_state["answered"] = False  # Reset for next question
                st.session_state["feedback"] = ""  # Clear feedback
                st.session_state["is_correct"] = None  # Reset correctness state
                st.rerun()  # Refresh for next question

    else:
        st.subheader(f"🎉 Quiz Completed! Your final score: **{st.session_state['score']} / {len(questions)}**")

        if st.button("🔄 Restart Quiz"):
            st.session_state["current_q"] = 0
            st.session_state["score"] = 0
            st.session_state["answered"] = False
            st.session_state["feedback"] = ""  # Reset feedback
            st.session_state["is_correct"] = None  # Reset correctness state
            st.rerun()  # Restart the quiz properly

# Run the quiz function
quiz()
