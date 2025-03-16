import streamlit as st
import plotly.figure_factory as ff
from datetime import datetime

# Define project tasks with updated details
tasks = [
    {"Task": "Literature Review", "Start": "2025-01-01", "End": "2025-04-30", "Status": "Ongoing"},
    
    {"Task": "Survey Design", "Start": "2025-01-01", "End": "2025-02-28", "Status": "Ongoing"},
    {"Task": "Conducting the Survey", "Start": "2025-03-01", "End": "2025-03-31", "Status": "Pending"},
    {"Task": "Analyzing the Survey", "Start": "2025-03-01", "End": "2025-03-31", "Status": "Pending"},
    {"Task": "Survey Writing", "Start": "2025-04-01", "End": "2025-04-30", "Status": "Pending"},
    
    {"Task": "Prototype Construction", "Start": "2025-01-01", "End": "2025-03-31", "Status": "Ongoing"},
    {"Task": "Evaluation", "Start": "2025-03-01", "End": "2025-03-31", "Status": "Pending"},
    {"Task": "Prototype Write-up", "Start": "2025-04-01", "End": "2025-04-30", "Status": "Pending"},
    
    {"Task": "Thesis Writing", "Start": "2025-01-01", "End": "2025-07-01", "Status": "Ongoing"},
    {"Task": "Results and Discussions", "Start": "2025-04-01", "End": "2025-04-30", "Status": "Pending"},
    {"Task": "Conclusion", "Start": "2025-04-01", "End": "2025-04-30", "Status": "Pending"},
    
    {"Task": "Submission", "Start": "2025-07-21", "End": "2025-07-21", "Status": "Finalizing"},
]

# Convert tasks to Gantt chart format
gantt_data = [
    dict(Task=task["Task"], Start=datetime.strptime(task["Start"], "%Y-%m-%d"),
         Finish=datetime.strptime(task["End"], "%Y-%m-%d"), Resource=task["Status"]) for task in tasks
]

# Define color coding for task statuses
colors = {"Ongoing": "#1f77b4", "Pending": "#ff7f0e", "Finalizing": "#2ca02c"}

# Create the Gantt chart
fig = ff.create_gantt(gantt_data, index_col="Resource", colors=colors, show_colorbar=True, group_tasks=True)

# Streamlit UI
st.set_page_config(page_title="Project Timeline", layout="wide")
st.title("📅 Project Timeline - Gantt Chart")
st.plotly_chart(fig)









