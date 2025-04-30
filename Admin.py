import streamlit as st
import json
import pandas as pd
import os
import plotly.express as px

def admin_login():
    st.title("Admin Panel - Quiz Settings and Results")
    st.write("Please enter your admin credentials to access admin features.")
    username = st.text_input("Username", key="admin_username")
    password = st.text_input("Password", type="password", key="admin_password")
    if st.button("Login"):
        # Hard-coded credentials for demonstration purposes
        if username == "Chydi" and password == "Fox1":
            st.session_state.admin_authenticated = True
            st.success("Login successful!")
        else:
            st.error("Invalid credentials. Please try again.")

def reset_quiz_results():
    """Delete the CSV file to clear all stored quiz results."""
    file_name = "quiz_results.csv"
    if os.path.exists(file_name):
        os.remove(file_name)
        st.success("Quiz results have been reset.")
    else:
        st.info("No quiz results found to reset.")

def admin_panel():
    st.title("Admin Panel - Quiz Settings and Player Results")
    st.write("Welcome, Admin! Use the panel below to view and modify quiz settings and review player history.")

    # --- Quiz Questions Editing Section ---
    st.subheader("Quiz Questions")
    if "phishing_questions" not in st.session_state:
        st.session_state.phishing_questions = []  # Initialize if not already present
    quiz_json = json.dumps(st.session_state.phishing_questions, indent=2)
    edited_quiz = st.text_area("Edit Quiz Questions (in JSON format):", value=quiz_json, height=300)
    if st.button("Save Changes"):
        try:
            st.session_state.phishing_questions = json.loads(edited_quiz)
            st.success("Quiz questions updated successfully!")
        except Exception as e:
            st.error("Error updating quiz questions: " + str(e))
    
    # --- Player History and Results Section ---
    st.subheader("Player History and Results")
    file_name = "quiz_results.csv"
    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
        # Remove duplicate records by Player Name, keeping only the latest entry per player.
        df_unique = df.drop_duplicates(subset=["Player Name"], keep="last").reset_index(drop=True)
        df_unique.index += 1  # Serial numbering starts at 1
        st.dataframe(df_unique)
        csv = df_unique.to_csv(index=False).encode('utf-8')
        st.download_button("Download Results as CSV", data=csv, file_name="quiz_results.csv", mime="text/csv")
    else:
        st.write("No quiz results available.")
    
    if st.button("Reset Quiz Results"):
        reset_quiz_results()
    
    # --- Leaderboard Section ---
    st.subheader("Leaderboard")
    if "leaderboard" in st.session_state and st.session_state.leaderboard:
        leaderboard_data = [{"Score": score, "Players": count} for score, count in st.session_state.leaderboard.items()]
        df_lb = pd.DataFrame(leaderboard_data)
        fig = px.bar(df_lb, x="Score", y="Players", title="Leaderboard")
        st.plotly_chart(fig)
    else:
        st.write("No leaderboard data available.")

def main():
    if "admin_authenticated" not in st.session_state or not st.session_state.admin_authenticated:
        admin_login()
    else:
        admin_panel()

if __name__ == "__main__":
    main()

