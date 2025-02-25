import streamlit as st
import pandas as pd
import requests
import openai  # Ensure OpenAI is properly installed
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import tldextract
import whois
import re

# Streamlit Page Config
st.set_page_config(page_title="URL Analysis Dashboard", layout="wide")

# Title
st.title("URL Readability & Security Analysis Dashboard")

# File Uploader
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding='utf-8', errors='replace')
    st.write("### Uploaded Data Preview")
    st.dataframe(df.head())

    # URL Extraction
    def extract_domain(url):
        ext = tldextract.extract(url)
        return f"{ext.domain}.{ext.suffix}" if ext.suffix else ext.domain
    
    df['Domain'] = df['URL'].apply(extract_domain)

    # WHOIS Lookup
    def get_whois_info(domain):
        try:
            info = whois.whois(domain)
            return info.registrar
        except:
            return "Not Found"
    
    df['Registrar'] = df['Domain'].apply(get_whois_info)
    
    # Search Function
    search_query = st.text_input("Search for a URL or keyword")
    if search_query:
        filtered_df = df[df['URL'].str.contains(search_query, case=False, na=False)]
        st.write("### Search Results")
        st.dataframe(filtered_df)
    
    # Chatbot Section
    def ask_openai(query):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": query}]
        )
        return response['choices'][0]['message']['content']

    chat_query = st.text_area("Ask the AI about URLs or cybersecurity")
    if st.button("Get AI Response"):
        if chat_query:
            response = ask_openai(chat_query)
            st.write("### AI Response")
            st.write(response)
    
    # API Integration for Report Generation
    def fetch_api_report(url):
        api_endpoint = "https://api.phishstats.info/check_url"
        response = requests.get(api_endpoint, params={"url": url})
        return response.json() if response.status_code == 200 else {"error": "API request failed"}
    
    url_for_check = st.text_input("Enter URL for detailed report")
    if st.button("Generate Report"):
        if url_for_check:
            report = fetch_api_report(url_for_check)
            st.write("### URL Security Report")
            st.json(report)
    
    # Support Email Section
    st.write("### Need Assistance?")
    st.write("For any issues, reach out to support@example.com")