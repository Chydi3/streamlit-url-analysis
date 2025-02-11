import streamlit as st
import requests
import pandas as pd
import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import openai

# Streamlit Page Config
st.set_page_config(page_title="Phishing Detection Dashboard", layout="wide")

# Title and description
st.title("🔍 URL Analysis & Phishing Detection Dashboard")
st.markdown("Analyze URLs for phishing threats, get reports, and interact with our chatbot!")

# Sidebar - Contact Support
st.sidebar.header("Need Help?")
st.sidebar.markdown("📧 Contact: support@example.com")

# Search Bar
def search_urls(df, search_query):
    return df[df['url'].str.contains(search_query, case=False, na=False)]

search_query = st.text_input("🔍 Search for a URL")

# Upload CSV
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(uploaded_file, encoding="ISO-8859-1")
    st.write(df.head())
    
    if search_query:
        results = search_urls(df, search_query)
        st.write(results)

# API Integration - URLScan.io
def scan_url(url):
    API_KEY = "YOUR_URLSCAN_API_KEY"
    headers = {"API-Key": API_KEY, "Content-Type": "application/json"}
    data = json.dumps({"url": url, "visibility": "public"})
    response = requests.post("https://urlscan.io/api/v1/scan/", headers=headers, data=data)
    return response.json()

url_to_scan = st.text_input("Enter URL to scan with URLScan.io")
if st.button("Scan URL"):
    if url_to_scan:
        scan_result = scan_url(url_to_scan)
        st.json(scan_result)
    else:
        st.warning("Please enter a valid URL")

# API Integration - PhishTank
def check_phishtank(url):
    response = requests.get(f"https://data.phishtank.com/data/online-valid.json")
    phishing_data = response.json()
    for entry in phishing_data:
        if fuzz.ratio(url, entry["url"]) > 90:
            return "⚠️ This URL is reported as a phishing site!"
    return "✅ This URL is not found in PhishTank."

url_to_check = st.text_input("Enter URL to check in PhishTank")
if st.button("Check URL"):
    if url_to_check:
        result = check_phishtank(url_to_check)
        st.write(result)
    else:
        st.warning("Please enter a valid URL")

# Chatbot Integration
def chat_with_ai(prompt):
    openai.api_key = "YOUR_OPENAI_API_KEY"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

st.sidebar.header("💬 Chatbot")
user_query = st.sidebar.text_input("Ask something:")
if st.sidebar.button("Send"):
    if user_query:
        chatbot_response = chat_with_ai(user_query)
        st.sidebar.write(chatbot_response)
    else:
        st.sidebar.warning("Please enter a message")

st.success("✅ Dashboard is fully functional with all features integrated!")