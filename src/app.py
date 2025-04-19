import streamlit as st
import model as mdl

st.set_page_config(page_title="Recipe Q&A Chatbot", page_icon="🤖", layout="centered")
st.title("Recipe Q&A Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_query = st.chat_input("Ask me a question...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})

    st.chat_message("user").markdown(user_query)

    with st.spinner("Processing..."):
        response = mdl.work(user_query)

    st.session_state.messages.append({"role": "assistant", "content": response})

    st.chat_message("assistant").markdown(response)

for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])