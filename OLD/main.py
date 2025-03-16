import streamlit as st
import random
from pages.Learn import learn
from pages.Quiz import quiz



 
def main():
# def homepage():

    st.title("Welcome to the URL Phishing Quiz Game!")
    if st.button("Learn about Phishing"):
        st.switch_page("pages/learn_page.py")
        # st.page_link("pages/learn_page.py", label="Learn", icon="📖")
    if st.button("Take the Quiz"):
        st.switch_page("pages/quiz_page.py")


    # st.sidebar.title("Navigation")
    # page = st.sidebar.radio("Go to", ["Homepage",  "Learn", "Quiz"])
    
    # if page == "Homepage":
    #     homepage()
    # elif page == "Learn":
    #     learn()
    # elif page == "Quiz":
    #     quiz()

if __name__ == "__main__":
    main()


