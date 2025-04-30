import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime

# Sample data for the Gantt chart
data = [
    {"Task": "Literature Review", "Start": "2025-01-01", "Finish": "2025-03-30", "Status": "Ongoing"},
    {"Task": "Survey - Design", "Start": "2025-02-01", "Finish": "2025-02-28", "Status": "Pending"},
    {"Task": "Survey - Conducting", "Start": "2025-03-01", "Finish": "2025-03-31", "Status": "Ongoing"},
    {"Task": "Survey - Analysis", "Start": "2025-04-01", "Finish": "2025-04-30", "Status": "Pending"},
    {"Task": "Survey - Writing", "Start": "2025-05-01", "Finish": "2025-05-31", "Status": "Pending"},
    {"Task": "Prototype - Construction", "Start": "2025-01-01", "Finish": "2025-04-30", "Status": "Ongoing"},
    {"Task": "Prototype - Evaluation", "Start": "2025-05-01", "Finish": "2025-06-30", "Status": "Pending"},
    {"Task": "Prototype - Write-up", "Start": "2025-06-01", "Finish": "2025-06-30", "Status": "Pending"},
    {"Task": "Thesis Writing", "Start": "2025-01-01", "Finish": "2025-07-01", "Status": "Ongoing"},
    {"Task": "Results & Discussions", "Start": "2025-05-01", "Finish": "2025-06-30", "Status": "Pending"},
    {"Task": "Conclusion", "Start": "2025-06-01", "Finish": "2025-07-15", "Status": "Finalizing"},
    {"Task": "Submission (Milestone)", "Start": "2025-07-21", "Finish": "2025-07-21", "Status": "Finalizing"}
]

df = pd.DataFrame(data)
df['Start'] = pd.to_datetime(df['Start'])
df['Finish'] = pd.to_datetime(df['Finish'])

# Assign colors based on status
color_map = {"Ongoing": "#1f77b4", "Pending": "#ff7f0e", "Finalizing": "#d62728"}
df["Color"] = df["Status"].map(color_map)

# Streamlit layout adjustments
st.set_page_config(layout="wide")
st.title("📅 Project Timeline - Gantt Chart")

# Gantt Chart with Plotly
fig = px.timeline(
    df, x_start="Start", x_end="Finish", y="Task", color="Status",
    color_discrete_map=color_map, title="Project Timeline - Gantt Chart",
    labels={"Task": "Tasks", "Start": "Timeline"}
)
fig.update_yaxes(categoryorder="total ascending")
fig.update_xaxes(tickformat="%b %Y", showgrid=True, tickangle=45)
fig.update_layout(
    autosize=True,
    margin=dict(l=0, r=0, t=50, b=50),
    height=700, width=1400,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white")
)

st.plotly_chart(fig, use_container_width=True)









