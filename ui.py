import streamlit as st
from collections import Counter
from llm_chat import chain  # your LLM chain
from audio import generate_audio_from_text
from topic_logger import log_topic
from streak_manager import update_streak
import json
from pathlib import Path
from datetime import datetime, timedelta

# -------------------------
# Streamlit Page Config
# -------------------------
st.set_page_config(page_title="NCERT Hinglish/tanglish Doubt Bot", page_icon="🤖")

# -------------------------
# Load CSS
# -------------------------
def load_css():
    try:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass

load_css()

# -------------------------
# Sidebar
# -------------------------
st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/4712/4712109.png",
    width=80
)
st.sidebar.title("NCERT AI Tutor")

mode = st.sidebar.radio("Select Mode", ["Student", "Teacher"])

# =============================
# TEACHER MODE
# =============================
if mode == "Teacher":
    password = st.sidebar.text_input("Teacher Password", type="password")

    if password == "teacher123":
        st.title("👩‍🏫 Teacher Dashboard")

        # Load topics from JSON
        db_file = Path("db.json")
        if db_file.exists():
            data = json.loads(db_file.read_text())
            all_topics = data.get("topics", [])
        else:
            all_topics = []

        # Filter last 7 days
        week_ago = datetime.now() - timedelta(days=7)
        filtered_topics = [
            t["topic"] for t in all_topics
            if datetime.fromisoformat(t["time"]) >= week_ago
        ]

        counts = Counter(filtered_topics)
        st.subheader("📊 Most Asked Topics (Last 7 Days)")

        if counts:
            chart_data = {
                "Topic": list(counts.keys()),
                "Questions": list(counts.values())
            }
            st.bar_chart(chart_data)

            for topic, count in counts.most_common():
                st.write(f"**{topic}** → {count} questions")
        else:
            st.info("No questions asked this week.")
    else:
        st.warning("Enter the correct teacher password")

# =============================
# STUDENT MODE
# =============================
if mode == "Student":
    st.title("🤖 NCERT Hinglish/tanglish Doubt Bot")
    st.write("Ask your Science / Maths doubts in Hinglish, Hindi, or Tanglish")

    # -------- STREAK INITIALIZATION --------
    if "streak" not in st.session_state:
        st.session_state.streak = update_streak()

    # Display streak in sidebar
    st.sidebar.subheader("🔥 Learning Streak")
    st.sidebar.success(f"{st.session_state.streak} Day Streak")

    # -------- CHAT SESSION STATE --------
    if "response" not in st.session_state:
        st.session_state.response = None
    if "question" not in st.session_state:
        st.session_state.question = None

    # -------- LOAD SYLLABUS --------
    try:
        with open("syllabus.txt", "r", encoding="utf-8") as f:
            syllabus_text = f.read()
    except:
        syllabus_text = ""

    # -------- CHAT INPUT --------
    question = st.chat_input("Ask your doubt...")

    if question:
        # Update streak
        st.session_state.streak = update_streak()
        st.session_state.question = question

        # TOPIC LOGGING
        q = question.lower()
        if "photosynthesis" in q:
            log_topic("Photosynthesis")
        if "trigonometry" in q:
            log_topic("Trigonometry")
        if "electric" in q:
            log_topic("Electric Circuits")

        # LLM Prompt (with language & syllabus instructions)
        system_prompt = f"""
You are a friendly NCERT teacher for Class 9–10 students.
Step 1: Detect the language style used by the student.
Language rules:
- Tamil words in English letters → Tanglish
- Hindi/English mix → Hinglish
Step 2: Reply in the SAME language style.
Use simple explanations with examples.
Question: {question}
Explain clearly.
Answer only if question falls under this syllabus:
{syllabus_text[:2000]}
Otherwise respond that the question is out of syllabus.
"""

        # Get AI response
        try:
            response = chain.invoke({
                "question": question,
                "text": system_prompt
            })
        except Exception as e:
            response = f"⚠️ Error generating answer: {str(e)}"

        st.session_state.response = response

    # -------- DISPLAY CHAT --------
    if st.session_state.question:
        with st.chat_message("user"):
            st.write(st.session_state.question)

    if st.session_state.response:
        with st.chat_message("assistant"):
            col1, col2 = st.columns([9,1])
            with col1:
                st.write(st.session_state.response)
            with col2:
                if st.button("🔊", key="speak"):
                    audio_file = generate_audio_from_text(st.session_state.response)
                    st.audio(audio_file)



