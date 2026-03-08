import streamlit as st
from collections import Counter
from llm_chat import chain  # import your LLM chain
from audio import generate_audio_from_text
from topic_logger import log_topic
from streak_manager import update_streak
from database import get_connection

# -------------------------
# Streamlit Page Config
# -------------------------
st.set_page_config(page_title="NCERT English/Hinglish/tanglish Doubt-clearing Bot", page_icon="🤖")

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
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT topic FROM topics WHERE time >= NOW() - INTERVAL 7 DAY"
            )
            rows = cursor.fetchall()
            filtered_topics = [row[0] for row in rows]
            cursor.close()
            conn.close()
        except Exception as e:
            filtered_topics = []
            st.error(f"Database Error: {str(e)}")

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
        st.warning("Enter teacher password to access dashboard")

# =============================
# STUDENT MODE
# =============================
if mode == "Student":
    st.title("🤖 NCERT English/Tanglish/Hinglish Doubt Bot")
    st.write("Ask your Science / Maths doubts in Hinglish, Hindi, or Tanglish")

    # -------- STREAK INITIALIZATION --------
    if "streak" not in st.session_state:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT streak FROM streaks ORDER BY id DESC LIMIT 1")
            result = cursor.fetchone()
            st.session_state.streak = result[0] if result else 0
            cursor.close()
            conn.close()
        except:
            st.session_state.streak = 0

    # Display streak in sidebar (only once)
    st.sidebar.subheader("🔥 Learning Streak")
    st.sidebar.success(f"{st.session_state.streak} Day Streak")

    # -------- SESSION STATE FOR CHAT --------
    if "response" not in st.session_state:
        st.session_state.response = None
    if "question" not in st.session_state:
        st.session_state.question = None

    # -------- LOAD SYLLABUS --------
    try:
        with open("syllabus.txt", "r", encoding="utf-8") as f:
            text = f.read()
    except:
        text = ""

    # -------- CHAT INPUT --------
    question = st.chat_input("Ask your doubt...")

    if question:
        # Update streak
        st.session_state.streak = update_streak()

        st.session_state.question = question

        # -------- TOPIC LOGGING --------
        q = question.lower()
        if "photosynthesis" in q:
            log_topic("Photosynthesis")
        if "trigonometry" in q:
            log_topic("Trigonometry")
        if "electric" in q:
            log_topic("Electric Circuits")

        # -------- GET RESPONSE FROM LLM --------
        try:
            response = chain.invoke({
                "question": question,
                "text": text[:2000]  # optional syllabus context
            })
        except Exception as e:
            response = f"⚠️ AI is busy right now. ({str(e)})"

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
                if st.button("🔊"):
                    # Generate audio bytes and play directly
                    audio_bytes = generate_audio_from_text(st.session_state.response)
                    st.audio(audio_bytes, format="audio/mp3")