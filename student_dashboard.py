import streamlit as st

st.title("🎓 Student Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Questions Asked", 12)

with col2:
    st.metric("Topics Covered", 5)

with col3:
    st.metric("Learning Streak", "4 Days")

st.divider()

st.header("🤖 Ask Your Doubt")

question = st.chat_input("Type your question...")

if question:

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        st.write("AI answer will appear here")