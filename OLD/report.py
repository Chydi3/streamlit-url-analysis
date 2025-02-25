import streamlit as st
import pandas as pd
from fpdf import FPDF
from io import BytesIO

# Load dataset
def load_data():
    return pd.DataFrame({
        "url": ["https://example.com", "https://phishing.com"],
        "category": ["Safe", "Phishing"],
        "status": ["Active", "Inactive"],
        "date_added": ["2025-01-01", "2025-02-01"],
        "bookmarked": [False, True],
        "domain_hosted": ["AWS", "GoDaddy"],  # Placeholder
        "popularity_ranking": [5, 100],  # Placeholder
        "google_pagerank": [7, 2],  # Placeholder
        "encryption_level": ["High", "Medium"],  # Placeholder
        "ownership": ["Verified", "Unverified"],  # Placeholder
        "website_age": ["5 years", "1 year"],  # Placeholder
        "manipulation_tricks": [0, 1],  # Placeholder
        "search_result": ["Match", "No Match"],  # Placeholder
        "domain_popularity": ["High", "Low"]  # Placeholder
    })

df = load_data()

# Display all URLs in the database
st.sidebar.header("Database Inspection")
if st.sidebar.button("Show All URLs"):
    st.write("### URLs in the Database")
    st.write(df["url"])

# Search Bar
st.header("URL Report Generator")
search_url = st.text_input("Enter a URL to search:")

# Display Report
if search_url:
    result = df[df["url"] == search_url]
    if not result.empty:
        st.subheader("Report for: " + search_url)
        
        # Facts About the Domain
        st.write("### Facts About the Domain")
        st.write(f"**Domain Hosted:** {result['domain_hosted'].values[0]}")
        st.write(f"**Popularity Ranking:** {result['popularity_ranking'].values[0]}")
        st.write(f"**Google PageRank:** {result['google_pagerank'].values[0]}")
        st.write(f"**Encryption Level:** {result['encryption_level'].values[0]}")
        st.write(f"**Ownership:** {result['ownership'].values[0]}")
        st.write(f"**Website Age:** {result['website_age'].values[0]}")
        
        # Tricks
        st.write("### Tricks")
        st.write(f"**Manipulation Tricks:** {result['manipulation_tricks'].values[0]}")
        
        # Report Summary
        st.write("### Report Summary")
        st.write("We cannot guarantee the safety or danger of this link.")
        st.write(f"**Search Result:** {result['search_result'].values[0]}")
        st.write(f"**Domain Popularity:** {result['domain_popularity'].values[0]}")
        
        # Download Report
        if st.button("Download Report"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Report for: {search_url}", ln=True)
            pdf.cell(200, 10, txt=f"Domain Hosted: {result['domain_hosted'].values[0]}", ln=True)
            pdf.cell(200, 10, txt=f"Popularity Ranking: {result['popularity_ranking'].values[0]}", ln=True)
            pdf.cell(200, 10, txt=f"Google PageRank: {result['google_pagerank'].values[0]}", ln=True)
            pdf.cell(200, 10, txt=f"Encryption Level: {result['encryption_level'].values[0]}", ln=True)
            pdf.cell(200, 10, txt=f"Ownership: {result['ownership'].values[0]}", ln=True)
            pdf.cell(200, 10, txt=f"Website Age: {result['website_age'].values[0]}", ln=True)
            pdf.cell(200, 10, txt=f"Manipulation Tricks: {result['manipulation_tricks'].values[0]}", ln=True)
            pdf.cell(200, 10, txt=f"Search Result: {result['search_result'].values[0]}", ln=True)
            pdf.cell(200, 10, txt=f"Domain Popularity: {result['domain_popularity'].values[0]}", ln=True)
            pdf_output = BytesIO()
            pdf.output(pdf_output, 'S')
            st.download_button(
                label="Download PDF",
                data=pdf_output.getvalue(),
                file_name="url_report.pdf",
                mime="application/pdf"
            )
    else:
        st.error("URL not found in the database.")

# Chatbot
st.sidebar.header("Chatbot")
user_query = st.sidebar.text_input("Ask me anything about the report:")
if user_query:
    if "search" in user_query.lower():
        st.sidebar.write("Enter the URL in the search bar and click 'Search' to generate a report.")
    elif "download" in user_query.lower():
        st.sidebar.write("After searching for a URL, click the 'Download Report' button to save the report as a PDF.")
    else:
        st.sidebar.write("For further support, please send a mail to support@example.com.")

# Help Section
st.sidebar.header("Help Section")
st.sidebar.write("For further support, please send a mail to support@example.com.")