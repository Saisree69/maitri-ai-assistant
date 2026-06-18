import streamlit as st
import pandas as pd
import random
from datetime import datetime

# ==============================
# Page Config
# ==============================
st.set_page_config(
    page_title="MAITRI AI Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Background styling
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: url('C:\\Users\\Sai\\Desktop\\N\\images3.jpg') no-repeat center center fixed;
    background-size: cover;
}
[data-testid="stHeader"] {background: rgba(0,0,0,0);}
[data-testid="stToolbar"] {right: 2rem;}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ==============================
# Session state for logs
# ==============================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "alerts" not in st.session_state:
    st.session_state.alerts = []

# ==============================
# Helper functions
# ==============================
def add_alert(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.alerts.append(f"[{timestamp}] {message}")

# ==============================
# UI Layout
# ==============================
st.title("🚀 MAITRI : AI Assistant for Astronaut Well-Being")

tabs = st.tabs([
    "🧠 Psychological Support",
    "💬 Companion Chat",
    "🎵 Relaxation",
    "⚠️ Alerts"
])

# ==============================
# Psychological Support
# ==============================
with tabs[0]:
    st.subheader("Psychological Support")
    mood = st.selectbox(
        "Select your current state",
        ["Lonely", "Happy", "Stressed", "Tired", "Anxiety", "Depression", "Sleep disturbance"]
    )
    if st.button("Get Suggestion"):
        suggestions = {
            "Lonely": "Try connecting with your crewmates, share a light conversation 🤝",
            "Happy": "Keep up the positive energy, maybe write a log entry ✨",
            "Stressed": "Take a few deep breaths, practice short mindfulness 🧘",
            "Tired": "Consider a short power nap or light stretches 💤",
            "Anxiety": "Focus on slow breathing, listen to calming sounds 🎶",
            "Depression": "Engage in small meaningful tasks, talk to the assistant 💬",
            "Sleep disturbance": "Adjust lights, relax before bed, try soft music 🌙"
        }
        st.success(suggestions[mood])

# ==============================
# Companion Chat
# ==============================
with tabs[1]:
    st.subheader("Companion Chat")
    user_input = st.text_input("You:", "")
    if st.button("Send"):
        if user_input:
            st.session_state.chat_history.append(f"You: {user_input}")
            # Expanded astronaut-related AI responses
            responses = [
                "I understand. Tell me more.",
                "That sounds challenging. How are you coping?",
                "Remember, you are doing an amazing job up there 🚀",
                "Try taking a deep breath.",
                "Stay strong, Earth is proud of you 🌍",
                "Keep monitoring your oxygen levels closely 🫁",
                "How is your EVA prep going today?",
                "Have you checked the spacecraft telemetry data?",
                "Remember to hydrate regularly 💧",
                "How’s the microgravity affecting your exercises?",
                "Have you completed today's science experiments?",
                "Is the communication link stable with mission control?",
                "Maintain situational awareness during the spacewalk 🛠️",
                "Document your observations for the logs 📓",
                "Ensure all systems are nominal before rest 🛌",
                "Remember, teamwork is key for mission success 🤝",
                "Are the solar panels functioning optimally?",
                "Have you recalibrated the instruments recently?",
                "Take short breaks to prevent fatigue ⏱️",
                "Stay positive; your crew depends on you 🌟",
                "Did you observe any anomalies in the habitat module?",
                "Check the suit integrity before EVA ⚠️",
                "Your mental health is important; practice mindfulness 🧘",
                "Have you synced your data with mission control?",
                "Keep a log of radiation exposure levels ☢️",
                "How’s your sleep cycle on orbit?",
                "Any updates on the spacecraft trajectory?",
                "Keep monitoring CO2 levels in the cabin 🌬️",
                "Are the experiments on plant growth showing results?",
                "Remember to enjoy the view of Earth 🌎"
            ]
            reply = random.choice(responses)
            st.session_state.chat_history.append(f"MAITRI: {reply}")

    st.text_area("Conversation", value="\n".join(st.session_state.chat_history[-12:]), height=300)

# ==============================
# Relaxation
# ==============================
with tabs[2]:
    st.subheader("Relaxation Module")
    st.markdown("### Soft Music Tones")
    music_links = {
        "Calm Ocean Waves": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        "Gentle Rain": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
        "Soothing Piano": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
        "Meditation Bells": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3"
    }
    for title, link in music_links.items():
        st.markdown(f"**{title}**")
        st.audio(link)

# ==============================
# Alerts
# ==============================
with tabs[3]:
    st.subheader("Alerts")
    if st.button("Simulate Alert"):
        alert_messages = [
            "⚠️ Low oxygen detected in module A",
            "⚠️ Crew member heart rate elevated",
            "⚠️ Communication delay detected",
            "⚠️ Minor movement anomaly detected"
        ]
        add_alert(random.choice(alert_messages))

    if st.session_state.alerts:
        st.text_area("Recent Alerts", value="\n".join(st.session_state.alerts[-12:]), height=300)
    else:
        st.info("No alerts yet. Simulate to generate alerts.")
