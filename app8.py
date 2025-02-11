import streamlit as st
import pandas as pd
import tldextract
import whois
from fuzzywuzzy import fuzz

# Streamlit app setup
st.set_page_config(page_title="URL Analysis Dashboard", layout="wide")

st.title("📊 URL Analysis Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, encoding="utf-8", errors="replace")  # FIXED ENCODING ERROR
    except UnicodeDecodeError:
        df = pd.read_csv(uploaded_file, encoding="latin1")  # Alternative encoding in case of errors

    st.write("### Data Preview")
    st.dataframe(df.head())

    # Ensure the uploaded file contains a 'URL' column
    if "URL" in df.columns:
        df["Domain"] = df["URL"].apply(lambda x: tldextract.extract(x).domain)
        df["TLD"] = df["URL"].apply(lambda x: tldextract.extract(x).suffix)

        # WHOIS lookup (can be slow)
        def get_whois_info(url):
            try:
                domain_info = whois.whois(url)
                return domain_info.creation_date
            except:
                return "Unknown"

        df["WHOIS Creation Date"] = df["URL"].apply(get_whois_info)

        # Display updated data
        st.write("### Processed Data")
        st.dataframe(df)

        # Search feature
        search_query = st.text_input("Search URL or Domain:")
        if search_query:
            search_results = df[df["URL"].str.contains(search_query, case=False, na=False)]
            st.write(f"### Search Results for '{search_query}'")
            st.dataframe(search_results)

    else:
        st.error("Uploaded file must contain a 'URL' column.")
else:
    st.info("Please upload a CSV file to proceed.")
