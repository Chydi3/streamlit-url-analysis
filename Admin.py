import streamlit as st
import json
import pandas as pd
import os
import plotly.express as px
from datetime import datetime

# ── HELPER: Load Learn Logs ────────────────────────────────────────────────────────
def load_learn_logs():
    file_name = "learn_logs.csv"
    if not os.path.exists(file_name):
        return None
    df = pd.read_csv(file_name)
    df.index += 1  # start indexing at 1
    return df

# ── RESET FUNCTIONS ───────────────────────────────────────────────────────────────
def reset_quiz_results():
    """Delete the CSV file to clear all stored quiz results."""
    file_name = "quiz_results.csv"
    if os.path.exists(file_name):
        os.remove(file_name)
        st.success("✅ Quiz results have been reset.")
    else:
        st.info("ℹ️ No quiz results found to reset.")

def reset_learn_logs():
    """Delete the CSV file to clear all stored learn session logs."""
    file_name = "learn_logs.csv"
    if os.path.exists(file_name):
        os.remove(file_name)
        st.success("✅ Learn logs have been reset.")
    else:
        st.info("ℹ️ No learn logs found to reset.")

# ── DASHBOARD METRIC HELPERS ───────────────────────────────────────────────────────
def get_unique_players():
    """Return count of unique player names from quiz results."""
    quiz_file = "quiz_results.csv"
    if os.path.exists(quiz_file):
        df = pd.read_csv(quiz_file)
        return df["Player Name"].nunique()
    return 0

def calculate_avg_score():
    """Calculate average quiz score across all attempts."""
    quiz_file = "quiz_results.csv"
    if os.path.exists(quiz_file):
        df = pd.read_csv(quiz_file)
        return round(df["Score"].mean(), 2) if not df.empty else 0
    return 0

def get_active_sessions():
    """Placeholder for active sessions count (could be extended)."""
    # Right now, we just show 1 as a placeholder.
    return 1

def get_recent_activity():
    """Return a list of recent admin activities (static examples)."""
    return [
        {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"), "activity": "System login", "user": "Admin"},
        {"timestamp": "2023-11-15 14:30", "activity": "Updated quiz questions", "user": "Admin"},
        {"timestamp": "2023-11-15 13:45", "activity": "Reset learn logs", "user": "Admin"}
    ]

# ── CUSTOM CSS FOR “OPS CENTER” DASHBOARD ──────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Global Dark Theme */
    html, body, [class*="css"] {
        background: #0A0A10 !important;
        color: #EDEDED !important;
        font-family: 'Source Code Pro', monospace !important;
    }

    /* Sidebar styling */
    .stSidebar {
        background-color: #101118 !important;
        border-right: 2px solid #00FF7F !important;
    }
    .stSidebar .css-1d391kg {
        color: #00FF7F !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        text-align: center !important;
        margin-bottom: 1rem !important;
    }
    .stSidebar .css-1aw77m0 {
        color: #EDEDED !important;
    }
    .stSidebar .stRadio label {
        color: #00FF7F !important;
        font-family: 'Source Code Pro', monospace !important;
    }
    .stSidebar .stRadio input:checked + label {
        color: #FF6B00 !important;
    }
    .stSidebar button {
        background-color: #00FF7F !important;
        color: #101118 !important;
        border-radius: 5px !important;
        font-weight: bold !important;
        margin-top: 1rem !important;
        width: 100% !important;
    }

    /* Ops Center Title */
    .ops-title {
        text-align: center;
        font-family: 'VT323', monospace !important;
        color: #FF6B00 !important;
        text-shadow: 0 0 10px #FF6B00 !important;
        font-size: 2.8rem !important;
        margin-bottom: 0.2rem !important;
    }
    .ops-subtitle {
        text-align: center;
        font-family: 'Source Code Pro', monospace !important;
        color: #00FF7F !important;
        margin-top: 0 !important;
        margin-bottom: 2rem !important;
    }

    /* Full-width metric cards */
    .metric-card {
        background-color: rgba(16,17,24,0.7) !important;
        border: 2px solid #00FF7F !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        text-align: center !important;
        box-shadow: 0 0 10px #00FF7F !important;
        margin-bottom: 1rem !important;
    }
    .metric-value {
        color: #00FF7F !important;
        font-family: 'VT323', monospace !important;
        font-size: 2.5rem !important;
        margin: 0 !important;
    }
    .metric-label {
        color: #EDEDED !important;
        font-family: 'Source Code Pro', monospace !important;
        margin: 0 !important;
        font-size: 1rem !important;
    }

    /* Subheader styling */
    h2 {
        font-family: 'Source Code Pro', monospace !important;
        color: #00FF7F !important;
        border-bottom: 1px solid #00FF7F !important;
        padding-bottom: 4px !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    h3 {
        font-family: 'Source Code Pro', monospace !important;
        color: #EDEDED !important;
        margin-top: 1rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Expandable Player Details Table */
    .player-row {
        cursor: pointer;
        transition: background 0.3s ease;
    }
    .player-row:hover {
        background-color: rgba(0,255,127,0.1) !important;
    }

    /* DataFrame styling */
    .stDataFrame > div {
        background-color: rgba(16,17,24,0.6) !important;
        border: 1px solid #00FF7F !important;
        border-radius: 10px !important;
        padding: 0.5rem !important;
    }
    .stDataFrame th {
        background-color: #00FF7F !important;
        color: #101118 !important;
        font-weight: bold !important;
    }
    .stDataFrame td {
        background-color: rgba(16,17,24,0.4) !important;
        color: #EDEDED !important;
    }

    /* Download button styling */
    .stDownloadButton > button {
        background-color: #00FF7F !important;
        color: #101118 !important;
        border-radius: 5px !important;
        font-family: 'Source Code Pro', monospace !important;
        font-weight: bold !important;
    }
    .stDownloadButton > button:hover {
        background-color: #101118 !important;
        color: #00FF7F !important;
        border: 2px solid #00FF7F !important;
    }

    /* Reset buttons styling */
    .stButton > button {
        background-color: rgba(0, 0, 0, 0.4) !important;
        border: 2px solid #FF6B00 !important;
        color: #FF6B00 !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.5rem !important;
        transition: all 0.3s ease !important;
        font-family: 'Source Code Pro', monospace !important;
        font-weight: bold !important;
        margin-top: 1rem !important;
    }
    .stButton > button:hover {
        background-color: #FF6B00 !important;
        color: #101118 !important;
        transform: scale(1.05) !important;
        box-shadow: 0 0 15px #FF6B00 !important;
    }

    /* Badge for version */
    .badge {
        position: absolute;
        top: 15px;
        right: 15px;
        background-color: rgba(0, 0, 0, 0.6) !important;
        padding: 0.4rem 1rem !important;
        border-radius: 15px !important;
        color: #00FF7F !important;
        border: 1px solid #00FF7F !important;
        font-family: 'VT323', monospace !important;
        font-weight: bold !important;
        box-shadow: 0 0 10px rgba(0, 255, 127, 0.3) !important;
        z-index: 999 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ── ADMIN LOGIN SECTION ────────────────────────────────────────────────────────────
def admin_login():
    st.title("🛡️ Admin Panel - Login")
    st.write("Enter your admin credentials to proceed.")
    st.markdown("")  # blank line spacing

    username = st.text_input("Username", key="admin_username")
    password = st.text_input("Password", type="password", key="admin_password")

    if st.button("🔐 Login"):
        if username == "Chydi" and password == "Fox1":
            st.session_state.admin_authenticated = True
            st.session_state.admin_nav = "Dashboard"
            st.success("✅ Login successful!")
        else:
            st.error("❌ Invalid credentials. Please try again.")

# ── DASHBOARD OVERVIEW ─────────────────────────────────────────────────────────────
def show_dashboard():
    st.markdown('<div class="badge">v1.0</div>', unsafe_allow_html=True)
    st.markdown('<p class="ops-title">OPERATIONAL OPS CENTER</p>', unsafe_allow_html=True)
    st.markdown('<p class="ops-subtitle">Real-Time Metrics & Activity</p>', unsafe_allow_html=True)

    # Full-width metric cards
    col1, col2, col3 = st.columns([1,1,1], gap="medium")
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        total_players = get_unique_players()
        st.markdown(f'<p class="metric-value">{total_players}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="metric-label">Total Players</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        avg_score = calculate_avg_score()
        st.markdown(f'<p class="metric-value">{avg_score}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="metric-label">Avg Quiz Score</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        active = get_active_sessions()
        st.markdown(f'<p class="metric-value">{active}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="metric-label">Active Sessions</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Recent Activity Timeline
    st.subheader("⏱️ Recent Activity")
    activities = get_recent_activity()
    for act in activities[:5]:
        st.markdown(f"- **{act['timestamp']}**: {act['activity']} (by *{act['user']}*)")

    # Quick Actions Buttons
    st.subheader("⚡ Quick Actions")
    qcol1, qcol2 = st.columns(2, gap="large")
    with qcol1:
        if st.button("🔄 Reset Quiz Results", use_container_width=True):
            reset_quiz_results()
    with qcol2:
        if st.button("🗑️ Reset Learn Logs", use_container_width=True):
            reset_learn_logs()

# ── ADMIN PANEL MAIN ─────────────────────────────────────────────────────────────────
def admin_panel():
    st.title("🛠️ Admin Panel")
    st.write("Welcome, **Admin**! Use the sidebar to navigate.")

    # Sidebar navigation
    with st.sidebar:
        st.markdown("### ▶ Command Console")
        nav_options = ["Dashboard", "Quiz Questions", "Player History", "Learn Logs", "Leaderboard"]
        st.radio("Navigate", options=nav_options, key="admin_nav", label_visibility="collapsed")
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.admin_authenticated = False

    # ROUTE SECTIONS
    if st.session_state.admin_nav == "Dashboard":
        show_dashboard()

    elif st.session_state.admin_nav == "Quiz Questions":
        st.subheader("📝 Quiz Questions Editor")
        if "phishing_questions" not in st.session_state:
            st.session_state.phishing_questions = []
        quiz_json = json.dumps(st.session_state.phishing_questions, indent=2)
        edited_quiz = st.text_area("Edit Quiz Questions (JSON):", value=quiz_json, height=300)
        if st.button("💾 Save Changes"):
            try:
                st.session_state.phishing_questions = json.loads(edited_quiz)
                st.success("✅ Quiz questions updated successfully!")
            except Exception as e:
                st.error(f"❌ Error updating quiz questions: {e}")

    elif st.session_state.admin_nav == "Player History":
        st.subheader("📜 Player History & Quiz Results")
        quiz_file = "quiz_results.csv"
        if os.path.exists(quiz_file):
            df_all = pd.read_csv(quiz_file)
            df_all.index += 1

            # Show full table of all attempts
            st.dataframe(df_all)

            # Download button
            csv_data = df_all.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download Quiz Results CSV",
                data=csv_data,
                file_name="quiz_results.csv",
                mime="text/csv"
            )

            # Build collapsible per‐player details
            unique_players = df_all["Player Name"].unique().tolist()
            st.markdown("---")
            st.markdown("#### 🔎 View Individual Player Details")
            for player in unique_players:
                with st.expander(f"▶ {player}", expanded=False):
                    player_df = df_all[df_all["Player Name"] == player].copy()
                    player_df = player_df.reset_index(drop=True)
                    player_df.index += 1
                    st.write(f"**Records for {player}:**")
                    st.dataframe(player_df)
        else:
            st.info("ℹ️ No quiz results available.")

        if st.button("🗑️ Reset Quiz Results"):
            reset_quiz_results()

    elif st.session_state.admin_nav == "Learn Logs":
        st.subheader("📚 Learn Session Logs")
        df_learn = load_learn_logs()
        if df_learn is not None:
            df_learn.index += 1
            st.dataframe(df_learn)
            csv_learn = df_learn.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download Learn Logs CSV",
                data=csv_learn,
                file_name="learn_logs.csv",
                mime="text/csv"
            )
        else:
            st.info("ℹ️ No learn session logs available.")

        if st.button("🗑️ Reset Learn Logs"):
            reset_learn_logs()

    elif st.session_state.admin_nav == "Leaderboard":
        st.subheader("🏆 Leaderboard")
        if "leaderboard" in st.session_state and st.session_state.leaderboard:
            leaderboard_data = [
                {"Score": score, "Players": count}
                for score, count in st.session_state.leaderboard.items()
            ]
            df_lb = pd.DataFrame(leaderboard_data)
            fig = px.bar(
                df_lb,
                x="Score",
                y="Players",
                title="Leaderboard",
                template="plotly_dark",
                color_discrete_sequence=["#00FF7F"]
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("ℹ️ No leaderboard data available.")

# ── MAIN EXECUTION ─────────────────────────────────────────────────────────────────
def main():
    if "admin_authenticated" not in st.session_state or not st.session_state.admin_authenticated:
        admin_login()
    else:
        admin_panel()

if __name__ == "__main__":
    main()
