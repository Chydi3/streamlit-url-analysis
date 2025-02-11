import streamlit as st
import pandas as pd
import tldextract
import difflib
import whois
import datetime
import requests
import random
from fuzzywuzzy import fuzz

# Title and Introduction
st.set_page_config(page_title="Advanced URL Analyzer", layout="wide")
st.title("🔍 Advanced URL Analyzer")
st.write("Analyze URLs, check for risks, and enhance your understanding of online security.")

# Sidebar - Upload CSV
st.sidebar.header("📂 Upload File")
uploaded_file = st.sidebar.file_uploader("Upload CSV with URLs", type=["csv"])

# AI Chatbot Placeholder (Future Enhancement)
st.sidebar.header("💬 Security Chatbot")
st.sidebar.write("Coming soon: Ask security-related questions here!")

# Function to extract URL components
def analyze_url(url):
    extracted = tldextract.extract(url)
    domain = f"{extracted.domain}.{extracted.suffix}"
    subdomain = extracted.subdomain
    path = url.split(domain)[-1]
    return domain, subdomain, path

# Function to check domain reputation
def check_domain_reputation(domain):
    try:
        domain_info = whois.whois(domain)
        creation_date = domain_info.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if creation_date:
            age_days = (datetime.datetime.now() - creation_date).days
            return f"Domain Age: {age_days} days"
        else:
            return "Domain Age: Unknown"
    except Exception:
        return "Unable to fetch domain info"

# Function to check for similar domains
def check_similarity(url, known_domains):
    highest_match = max(known_domains, key=lambda x: fuzz.ratio(url, x))
    similarity_score = fuzz.ratio(url, highest_match)
    return highest_match, similarity_score

# Function to analyze security risks
def analyze_security(url):
    risk_factors = ["-", "~", "@", "login", "secure", "account", "verify"]
    risk_score = sum(url.count(factor) for factor in risk_factors)
    return f"Risk Score: {risk_score}/10"

# Processing Uploaded File
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if "URL" not in df.columns:
        st.error("Uploaded file must contain a 'URL' column.")
    else:
        df['Domain'], df['Subdomain'], df['Path'] = zip(*df['URL'].map(analyze_url))
        df['Domain Age'] = df['Domain'].apply(check_domain_reputation)
        df['Security Risk'] = df['URL'].apply(analyze_security)
        known_domains = df['Domain'].unique().tolist()
        df['Most Similar'], df['Similarity Score'] = zip(*df['URL'].map(lambda x: check_similarity(x, known_domains)))
        
        # Display results
        st.subheader("🔎 URL Analysis Results")
        st.dataframe(df)

# Gamified Learning Section
st.subheader("🎮 URL Detective: Guess the Destination!")
sample_urls = ["https://secure-login.paypal.com", "https://google.docs.fake.com", "https://manglemelder.de/report"]
random.shuffle(sample_urls)
guess_url = st.selectbox("Which URL looks most suspicious?", sample_urls)
if st.button("Submit Answer"):
    if "fake" in guess_url:
        st.success("✅ Correct! This looks like a phishing attempt.")
    else:
        st.warning("⚠️ Be careful! Recheck the domain structure.")

st.write("**Coming soon:** AI-powered chatbot, deeper security insights, and user behavior heatmaps!")