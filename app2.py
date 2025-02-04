import streamlit as st
import pandas as pd

# Title of the Dashboard
st.title("URL Analysis Report")

# Sidebar for user input
st.sidebar.header("Upload URL Data")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("File uploaded successfully!")
else:
    df = None

# Section 1: Facts
st.header("Facts")
st.subheader("Domain Information")
st.write("Domain Name: example.com")
st.write("Top Search Result: https://example.com")
st.write("Google Page Rank: 3/10 (Low)")
st.write("Encryption: Basic SSL Encryption (Let's Encrypt)")
st.write("Unverified Owner: Organization owns the domain, but verification not paid for")
st.write("Website Age: 10-05-1985")

# Section 2: Tricks
st.header("Tricks")
st.write("This domain is similar to a popular organization (e.g., 'goggle.com' instead of 'google.com').")

# Section 3: Report Summary
st.header("Report Summary")
st.write("We cannot guarantee the safety or danger of this link.")
summary_data = {
    "Used Manipulation Tricks": "1",
    "Search Results Match": "No Match",
    "Domain Age": "1 month",
    "Domain Popularity": "Low",
}
st.table(pd.DataFrame(summary_data.items(), columns=["Metric", "Value"]))

# Section 4: Manipulation Tricks
st.header("Manipulation Tricks")
st.write("Examples of manipulation techniques used in the domain name:")
st.write("- Typosquatting (e.g., 'faceboook.com')")
st.write("- Homograph Attack (e.g., replacing 'o' with '0')")
st.write("- Subdomain Trick (e.g., 'paypal.com.secure-login.com')")

# Section 5: URL Facts
st.header("URL Facts")
st.write("- Hosting Location: Germany")
st.write("- IP Address: 192.168.1.1")
st.write("- WHOIS Information: Registered to John Doe, Example Inc.")

st.success("Report generated successfully!")

