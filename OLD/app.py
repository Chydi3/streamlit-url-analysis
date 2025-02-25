import streamlit as st
import pandas as pd

# Title of the Dashboard
st.title("URL Analysis Report")

# Sidebar for user input
st.sidebar.header("Upload URL Data")
uploaded_file = st.sidebar.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

# Initialize the dataframe
df = None

# If file is uploaded, read the data
if uploaded_file:
    # Read the file based on its type
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    
    st.sidebar.success("File uploaded successfully!")
else:
    st.info("Upload a file with URLs to proceed.")

# Only proceed if data is loaded
if df is not None:
    # Check if 'URL' column exists
    if 'URL' in df.columns:
        st.write("URLs Loaded from Excel:")
        st.write(df['URL'])

        # Let user select a URL from the list
        selected_url = st.selectbox("Select a URL to view the report", df['URL'])

        # Placeholder for the report generation function
        if selected_url:
            st.subheader(f"Report for {selected_url}")
            # Generate a simple report (replace with your custom logic)
            st.write(f"Domain: {selected_url.split('/')[2]}")  # Displaying domain name from URL
            st.write("Page Rank: Low")
            st.write("Encryption: SSL Encryption")
            st.write("Owner Verified: No")
            
            # Display your detailed report sections below (static data can remain)
            st.header("Facts")
            st.subheader("Domain Information")
            st.write("Domain Name: example.com")
            st.write("Top Search Result: https://example.com")
            st.write("Google Page Rank: 3/10 (Low)")
            st.write("Encryption: Basic SSL Encryption (Let's Encrypt)")
            st.write("Unverified Owner: Organization owns the domain, but verification not paid for")
            st.write("Website Age: 10-05-1985")

            # Add sections like "Tricks," "Report Summary," etc.
            st.header("Tricks")
            st.write("This domain is similar to a popular organization (e.g., 'goggle.com' instead of 'google.com').")

            # Continue with other sections like your existing code (Report Summary, etc.)
            st.header("Report Summary")
            st.write("We cannot guarantee the safety or danger of this link.")
            summary_data = {
                "Used Manipulation Tricks": "1",
                "Search Results Match": "No Match",
                "Domain Age": "1 month",
                "Domain Popularity": "Low",
            }
            st.table(pd.DataFrame(summary_data.items(), columns=["Metric", "Value"]))

            # Manipulation Tricks section
            st.header("Manipulation Tricks")
            st.write("Examples of manipulation techniques used in the domain name:")
            st.write("- Typosquatting (e.g., 'faceboook.com')")
            st.write("- Homograph Attack (e.g., replacing 'o' with '0')")
            st.write("- Subdomain Trick (e.g., 'paypal.com.secure-login.com')")

            # URL Facts section
            st.header("URL Facts")
            st.write("- Hosting Location: Germany")
            st.write("- IP Address: 192.168.1.1")
            st.write("- WHOIS Information: Registered to John Doe, Example Inc.")
            
            st.success("Report generated successfully!")
    else:
        st.error("The Excel/CSV file must contain a 'URL' column.")
else:
    st.info("Please upload a CSV or Excel file with URLs.")

