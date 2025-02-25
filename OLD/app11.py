import streamlit as st
import pandas as pd
import openai
import requests
import json
from io import StringIO

# Streamlit Page Configuration
st.set_page_config(page_title="URL Analysis Dashboard", layout="wide")

# Sidebar - Support Section
st.sidebar.header("Support")
st.sidebar.info("If you need help, contact us at support@example.com")

# Sidebar - Search Bar
search_query = st.sidebar.text_input("Search URLs", "")

# Upload File
st.title("📊 URL Analysis Dashboard")
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    df = pd.read_csv(stringio)
    
    # Filter Data Based on Search Query
    if search_query:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
    
    st.write("### Uploaded Data")
    st.dataframe(df)

    # API Integration for URL Reports
    def get_url_analysis(url):
        api_url = "https://api.example.com/analyze"
        response = requests.post(api_url, json={"url": url})
        return response.json()

    if st.button("Analyze URLs"):
        results = []
        for url in df["url"]:
            result = get_url_analysis(url)
            results.append(result)
        
        report_df = pd.DataFrame(results)
        st.write("### URL Analysis Report")
        st.dataframe(report_df)

# Chatbot Feature
st.subheader("💬 Chatbot Assistance")
user_input = st.text_input("Ask me anything about URLs:")

if user_input:
    openai.api_key = "your-openai-api-key"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_input}]
    )
    st.write(response["choices"][0]["message"]["content"])