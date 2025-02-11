import streamlit as st

def learn():
    st.title("Learn About Phishing URLs")
    st.write("Phishing attacks trick users by using fake URLs that look real.")
    st.write("Here are some common phishing tricks:")
    st.markdown("- Using similar-looking characters (e.g., paypa1 instead of paypal)")
    st.markdown("- Adding extra words (e.g., secure-paypal.com instead of paypal.com)")
    st.markdown("- Using HTTP instead of HTTPS")

    # Back to Home Button
    if st.button("🔙 Back to Home"):
        st.switch_page("main.py")

# Run the function
learn()
