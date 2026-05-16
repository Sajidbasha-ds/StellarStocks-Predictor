# chatbot.py

import streamlit as st


def faq_chatbot():
    st.subheader("🤖 Smart FAQ Assistant")

    question = st.selectbox(
        "Ask a question",
        [
            "How does prediction work?",
            "Which ML model is best?",
            "Can I use Indian stocks?",
            "Is this financial advice?"
        ]
    )

    if question == "How does prediction work?":
        st.info("The app uses historical stock data with machine learning algorithms to estimate future prices.")

    elif question == "Which ML model is best?":
        st.info("Random Forest usually performs best because it handles market patterns effectively.")

    elif question == "Can I use Indian stocks?":
         st.info("Yes. Use .NS for NSE stocks like TCS.NS or RELIANCE.NS.")

    elif question == "Is this financial advice?":
        st.warning("No. This project is for educational and analytical purposes only.")