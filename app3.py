import streamlit as st
import pandas as pd

# Title of the Dashboard
st.title("URL Analysis Report")

# Sidebar for user input
st.sidebar.header("Upload URL Data")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

# Check if the file is uploaded
if uploaded_file:
    try:
        # Read the uploaded CSV file and handle encoding issues
        df = pd.read_csv(uploaded_file, encoding='utf-8', on_bad_lines='skip')  # Handles encoding and bad lines
        st.sidebar.success("File uploaded successfully!")
        
        # Check if 'URL' column exists
        if 'URL' not in df.columns:
            st.error("Uploaded file must contain a 'URL' column.")
        else:
            # Proceed with data analysis or display
            st.header("Uploaded URLs")
            st.write(df.head())  # Display the first few rows of the file as a preview
            
            # You can now loop through the rows and generate reports for each URL
            for index, row in df.iterrows():
                url = row['URL']
                st.subheader(f"Report for: {url}")
                # (Insert logic to generate reports based on each URL here)
                # Example:
                st.write(f"Domain Name: {url}")
                st.write("Top Search Result: https://example.com")
                st.write("Google Page Rank: 3/10 (Low)")
                st.write("Encryption: Basic SSL Encryption (Let's Encrypt)")
                st.write("Unverified Owner: Organization owns the domain, but verification not paid for")
                st.write("Website Age: 10-05-1985")
                st.write("Manipulation Tricks: Typosquatting (e.g., 'faceboook.com')")
                st.write("Hosting Location: Germany")
                st.write("IP Address: 192.168.1.1")
                st.write("WHOIS Information: Registered to John Doe, Example Inc.")
                st.write("---")  # Add a separator between reports
            
    except Exception as e:
        st.error(f"Error: {e}")

else:
    st.warning("Please upload a CSV file containing URL data.")

