import streamlit as st

st.title("👩‍🏫 Teacher Dashboard")

st.subheader("Class Analytics")

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Questions", 120)

with col2:
    st.metric("Active Topics", 8)

st.divider()

st.subheader("Most Asked Topics")

data = {
    "Photosynthesis": 18,
    "Trigonometry": 12,
    "Electric Circuits": 9
}

st.bar_chart(data)