import streamlit as st
import pandas as pd

# Title
st.title("URL Analysis Dashboard")

# Sidebar for chatbot
st.sidebar.title("Assistant Chatbot")
st.sidebar.write("Ask any question, and I'll try to help!")

# Placeholder for chatbot input
user_question = st.sidebar.text_input("Type your question here:")

if user_question:
    st.sidebar.write("🤖 Chatbot: This feature is under development. Stay tuned!")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Read CSV with proper encoding and delimiter
        df = pd.read_csv(uploaded_file, encoding="latin1", delimiter=";")
        
        # Check if 'URL' column exists
        if "URL" not in df.columns:
            st.error("Uploaded file must contain a 'URL' column.")
        else:
            st.success("File uploaded successfully!")
            st.write("### Preview of Uploaded Data:")
            st.write(df.head())  # Display first few rows
            
            # Search functionality
            search_query = st.text_input("Search for a URL")
            if search_query:
                filtered_df = df[df["URL"].str.contains(search_query, case=False, na=False)]
                if not filtered_df.empty:
                    st.write("### Search Results:")
                    st.write(filtered_df)
                else:
                    st.warning("No matching URLs found.")

    except Exception as e:
        st.error(f"Error reading the file: {e}")
        st.write("For assistance, please contact the admin at chismooth3@gmail.com.")

# Footer with contact information
st.markdown("---")
st.markdown("📩 Need help? Contact: [chismooth3@gmail.com](mailto:chismooth3@gmail.com)")
