import streamlit as st
import json

def admin_login():
    st.title("Admin Panel - Quiz Settings")
    st.write("Please enter your admin credentials to access quiz settings.")
    username = st.text_input("Username", value="")
    password = st.text_input("Password", type="password", value="")
    if st.button("Login"):
        # Hard-coded credentials for demonstration
        if username == "admin" and password == "admin123":
            st.session_state.admin_authenticated = True
            st.success("Login successful!")
        else:
            st.error("Invalid credentials. Please try again.")

def admin_panel():
    st.title("Admin Panel - Quiz Settings")
    st.write("Welcome, Admin! Use the panel below to view and modify quiz settings.")
    
    # For demonstration, we'll assume the quiz questions are stored as JSON in session state.
    # In a real-world scenario, these might be loaded from a database or a file.
    if "phishing_questions" not in st.session_state:
        # Initialize with an empty list or load defaults.
        st.session_state.phishing_questions = []  
    
    st.write("### Current Quiz Questions:")
    # Show the current quiz questions as a JSON string for editing.
    quiz_json = json.dumps(st.session_state.phishing_questions, indent=2)
    edited_quiz = st.text_area("Edit Quiz Questions (in JSON format):", value=quiz_json, height=300)
    
    if st.button("Save Changes"):
        try:
            # Try to load the edited JSON; if successful, update the session state.
            st.session_state.phishing_questions = json.loads(edited_quiz)
            st.success("Quiz questions updated successfully!")
        except Exception as e:
            st.error("Error updating quiz questions: " + str(e))
    
    st.write("You can add, modify, or remove questions as needed. Changes will apply immediately.")

def main():
    # Check if admin is authenticated; if not, show the login form.
    if "admin_authenticated" not in st.session_state or not st.session_state.admin_authenticated:
        admin_login()
    else:
        admin_panel()

if __name__ == "__main__":
    main()
