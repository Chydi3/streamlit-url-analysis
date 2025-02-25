import streamlit as st
import requests
import pandas as pd
import tldextract
import whois
import openai
from fuzzywuzzy import fuzz

# API Endpoint
API_URL = "http://127.0.0.1:8000/analyze_url"

def analyze_url(url):
    response = requests.post(API_URL, json={"url": url})
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to analyze URL"}

st.title("Enhanced URL Analysis Dashboard")

# File Upload Section
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

def process_file(uploaded_file):
    df = pd.read_csv(uploaded_file, encoding='latin1', delimiter=';')  # Fixed delimiter issue
    return df

if uploaded_file is not None:
    df = process_file(uploaded_file)
    st.write("### Uploaded Data Preview")
    st.dataframe(df.head())

    if "URL" in df.columns:  # Ensure correct column name
        df["Analysis"] = df["URL"].apply(analyze_url)
        st.write("### Analyzed Data")
        st.dataframe(df)
    else:
        st.error("No 'URL' column found in uploaded file. Please check the column names.")

# Search Bar
search_query = st.text_input("Search for a URL")
if search_query:
    result = analyze_url(search_query)
    st.write("### Search Result")
    st.json(result)

# Chatbot Section
st.write("## AI Chatbot")
user_input = st.text_input("Ask the chatbot about URL security:")
if user_input:
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{user_input}",
        max_tokens=150
    )
    st.write("Chatbot Response:", response["choices"][0]["text"].strip())

# Support Section
st.write("## Support")
st.write("If you need help, contact: support@example.com")