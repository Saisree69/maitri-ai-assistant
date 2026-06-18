# maitri_multipage_singlefile.py
# Single-file simulated multi-page Streamlit app
# Includes your two original referral code blocks verbatim (unchanged),
# then adds a multi-page UI wrapper (sidebar navigation + astronaut theme).

# ----------------------------
# ORIGINAL REFERRAL CODE BLOCK 1 (VERBATIM)
# ----------------------------
import streamlit as st
from PIL import Image
import numpy as np
from fer import FER
from pydub import AudioSegment
import io
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder

# --- Initialize session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Language selection ---
st.sidebar.title("Language Selection")
selected_language = st.sidebar.selectbox("Choose your language", ["English", "Hindi", "Telugu"])

# --- Header ---
st.title("🚀 MAITRI: Astronaut Mood & Activity Assistant")

# --- Camera input ---
st.subheader("📸 Take a picture to analyze your mood")
camera_image = st.camera_input("Capture your face")

if camera_image:
    img = Image.open(camera_image)
    img_array = np.array(img)
    detector = FER(mtcnn=True)
    emotions = detector.detect_emotions(img_array)

    if emotions:
        top_emotion, score = detector.top_emotion(img_array)
        st.session_state.messages.append(
            ("bot", f"😊 Detected Emotion: *{top_emotion}* ({round(score*100,2)}%)")
        )

        # --- Activity suggestions ---
        activity_suggestions = {
            "English": {
                "sad": ["🎮 Play a game", "Breathing exercises", "🎵 Listen to music"],
                "angry": ["🧘 Meditation", "📝 Stress relief quiz"],
                "happy": ["Share positivity", "❓ Fun quiz", "🎬 Light movie"],
                "neutral": ["📖 Explore resources", "🤸 Stretching", "✍ Journaling"],
            },
            "Hindi": {
                "sad": ["🎮 गेम खेलें", "🌬 श्वास अभ्यास", "🎵 संगीत सुनें"],
                "angry": ["🧘 ध्यान करें", "📝 तनाव कम करने वाला क्विज़"],
                "happy": ["सकारात्मकता साझा करें", "❓ मज़ेदार क्विज़", "🎬 हल्की फिल्म देखें"],
                "neutral": ["📖 संसाधन देखें", "🤸 स्ट्रेचिंग", "✍ जर्नलिंग"],
            },
            "Telugu": {
                "sad": ["🎮 గేమ్ ఆడండి", "🌬 శ్వాస వ్యాయామం", "🎵 సంగీతం వినండి"],
                "angry": ["🧘 ధ్యానం", "📝 స్ట్రెస్ రీلیف క్విజ్"],
                "happy": ["సానుకూలతను పంచుకోండి", "❓ ఫన్ క్విజ్", "🎬 లైట్ మూవీ"],
                "neutral": ["📖 వనరులు పరిశీలించండి", "🤸 స్ట్రెచింగ్", "✍ జర్నలింగ్"],
            },
        }

        suggestions = activity_suggestions[selected_language].get(
            top_emotion, activity_suggestions[selected_language]["neutral"]
        )

        st.session_state.messages.append(
            ("bot", f"💬 Suggestions: {', '.join(suggestions)}")
        )

    else:
        st.warning("⚠ No face detected. Please try again.")

# --- Voice input ---
st.subheader("🎤 Speak with MAITRI")
audio = mic_recorder(start_prompt="🎙 Start Recording", stop_prompt="⏹ Stop", key="recorder")

if audio and "bytes" in audio:
    st.audio(audio["bytes"], format="audio/webm")
    webm_audio = io.BytesIO(audio["bytes"])
    sound = AudioSegment.from_file(webm_audio, format="webm")
    sound.export("temp_audio.wav", format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile("temp_audio.wav") as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="en-IN")
            st.session_state.messages.append(("user", text))
            st.success(f"✅ You said: {text}")
        except sr.UnknownValueError:
            st.warning("⚠ Could not understand audio.")
        except sr.RequestError:
            st.error("⚠ Could not request results from Google Speech Recognition service.")

# --- Display chat messages ---
st.subheader("💬 Conversation")
for sender, message in st.session_state.messages:
    if sender == "user":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**Bot:** {message}")

# ----------------------------
# ORIGINAL REFERRAL CODE BLOCK 2 (VERBATIM)
# ----------------------------
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

# ----------------------------
# END OF ORIGINAL REFERRAL CODE BLOCKS
# ----------------------------

# =============================
# MULTI-PAGE (SIMULATED) WRAPPER
# =============================
# We will provide a sidebar page selector to let judges navigate a multi-page style app.
# Note: Your original code blocks remain verbatim above (unchanged).
# The following code adds a clean astronaut-themed menu and optional extra presentation,
# but DOES NOT remove or alter any of your original lines.

# ---- Astronaut-themed CSS for wrapper (light bg, dark text) ----
st.markdown("""
<style>
/* App background and colors */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #f7fbff 0%, #eef6ff 100%);
    color: #072033;
}

/* Sidebar style */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff, #f1f8ff) !important;
    color: #072033;
}

/* Simple top navbar like appearance for headings */
.page-title {
    background: linear-gradient(90deg, rgba(10,87,161,0.06), rgba(30,144,255,0.04));
    padding: 10px 14px;
    border-radius: 10px;
    box-shadow: 0 6px 18px rgba(3,67,120,0.04);
    margin-bottom: 12px;
}

/* Card style */
.card {
    background: white;
    border-radius: 12px;
    padding: 14px;
    box-shadow: 0 6px 20px rgba(6,30,55,0.04);
    color: #072033;
    margin-bottom: 12px;
}

/* Footer */
.footer {
    text-align:center;
    color:#0b2b3a;
    margin-top:14px;
    font-size:13px;
}
</style>
""", unsafe_allow_html=True)

# ---- Sidebar: simulated pages ----
st.sidebar.markdown("## 📂 Navigation")
page = st.sidebar.radio("", [
    "Home",
    "Face & Emotion Detection",
    "Voice Analysis",
    "Companion Chat",
    "Relaxation",
    "Alerts",
    "All Original (verbatim) — Scroll Up"
])

# ---- Page: Home ----
if page == "Home":
    st.markdown("<div class='page-title'><h2>🚀 MAITRI — Dashboard Home</h2></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'><h3>Welcome</h3><p>This single-file multi-page app displays MAITRI modules. Use the navigation on the left to view each module.</p></div>", unsafe_allow_html=True)
    # show quick metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Mood Logs", len(st.session_state.get("messages", [])))
    with col2:
        st.metric("Chat Exchanges", len(st.session_state.get("chat_history", [])))
    with col3:
        st.metric("Alerts", len(st.session_state.get("alerts", [])))

# ---- Page: Face & Emotion Detection ----
elif page == "Face & Emotion Detection":
    st.markdown("<div class='page-title'><h2>📸 Face & Emotion Detection</h2></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("This page uses the original emotion detection logic (FER + camera).")
    # replicate the exact camera capture block (same logic/lines as original; we call camera_input again to run in this page)
    camera_image_page = st.camera_input("Capture your face (Page)")
    if camera_image_page:
        img_p = Image.open(camera_image_page)
        img_arr_p = np.array(img_p)
        detector_p = FER(mtcnn=True)
        emotions_p = detector_p.detect_emotions(img_arr_p)
        if emotions_p:
            top_em_p, score_p = detector_p.top_emotion(img_arr_p)
            st.success(f"Detected Emotion: {top_em_p} ({round(score_p*100,2)}%)")
            # reuse suggestions dict (exact lines mirrored)
            activity_suggestions_page = {
                "English": {
                    "sad": ["🎮 Play a game", "Breathing exercises", "🎵 Listen to music"],
                    "angry": ["🧘 Meditation", "📝 Stress relief quiz"],
                    "happy": ["Share positivity", "❓ Fun quiz", "🎬 Light movie"],
                    "neutral": ["📖 Explore resources", "🤸 Stretching", "✍ Journaling"],
                },
                "Hindi": {
                    "sad": ["🎮 गेम खेलें", "🌬 श्वास अभ्यास", "🎵 संगीत सुनें"],
                    "angry": ["🧘 ध्यान करें", "📝 तनाव कम करने वाला क्विज़"],
                    "happy": ["सकारात्मकता साझा करें", "❓ मज़ेदार क्विज़", "🎬 हल्की फिल्म देखें"],
                    "neutral": ["📖 संसाधन देखें", "🤸 स्ट्रेचिंग", "✍ जर्नलिंग"],
                },
                "Telugu": {
                    "sad": ["🎮 గేమ్ ఆడండి", "🌬 శ్వాస వ్యాయామం", "🎵 సంగీతం వినండి"],
                    "angry": ["🧘 ధ్యానం", "📝 స్ట్రెస్ రీల్ క్విజ్"],
                    "happy": ["సానుకూలతను పంచుకోండి", "❓ ఫన్ క్విజ్", "🎬 లైట్ మూవీ"],
                    "neutral": ["📖 వనరులు పరిశీలించండి", "🤸 స్ట్రెచింగ్", "✍ జర్నలింగ్"],
                },
            }
            suggs = activity_suggestions_page[selected_language].get(top_em_p, activity_suggestions_page[selected_language]["neutral"])
            st.info("Suggestions: " + ", ".join(suggs))
        else:
            st.warning("No face detected on this page. Try again.")
    st.markdown("</div>", unsafe_allow_html=True)

# ---- Page: Voice Analysis ----
elif page == "Voice Analysis":
    st.markdown("<div class='page-title'><h2>🎤 Voice Analysis</h2></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("This page uses the original voice-recording + speech-recognition logic.")
    audio_page = mic_recorder(start_prompt="🎙 Start Recording", stop_prompt="⏹ Stop", key="recorder_page")
    if audio_page and "bytes" in audio_page:
        st.audio(audio_page["bytes"], format="audio/webm")
        webm_audio_p = io.BytesIO(audio_page["bytes"])
        sound_p = AudioSegment.from_file(webm_audio_p, format="webm")
        sound_p.export("temp_audio_page.wav", format="wav")
        recognizer_page = sr.Recognizer()
        with sr.AudioFile("temp_audio_page.wav") as source_p:
            audio_data_p = recognizer_page.record(source_p)
            try:
                text_p = recognizer_page.recognize_google(audio_data_p, language="en-IN")
                st.success(f"✅ You said: {text_p}")
            except sr.UnknownValueError:
                st.warning("⚠ Could not understand audio.")
            except sr.RequestError:
                st.error("⚠ Could not request results from Google Speech Recognition service.")
    st.markdown("</div>", unsafe_allow_html=True)

# ---- Page: Companion Chat ----
elif page == "Companion Chat":
    st.markdown("<div class='page-title'><h2>💬 Companion Chat</h2></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    chat_in = st.text_input("You (Companion Page):", key="companion_singlefile")
    if st.button("Send", key="companion_send_singlefile"):
        if chat_in:
            st.session_state.chat_history.append(f"You: {chat_in}")
            responses_page = [
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
            reply_page = random.choice(responses_page)
            st.session_state.chat_history.append(f"MAITRI: {reply_page}")
    st.text_area("Conversation (companion)", value="\n".join(st.session_state.chat_history[-12:]), height=260)
    st.markdown("</div>", unsafe_allow_html=True)

# ---- Page: Relaxation ----
elif page == "Relaxation":
    st.markdown("<div class='page-title'><h2>🎵 Relaxation</h2></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Soft Music Tones")
    music_links_page = {
        "Calm Ocean Waves": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        "Gentle Rain": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
        "Soothing Piano": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
        "Meditation Bells": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3"
    }
    for title_p, link_p in music_links_page.items():
        st.markdown(f"**{title_p}**")
        st.audio(link_p)
    st.markdown("</div>", unsafe_allow_html=True)

# ---- Page: Alerts ----
elif page == "Alerts":
    st.markdown("<div class='page-title'><h2>⚠️ Alerts</h2></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    if st.button("Simulate Alert (page)"):
        alert_messages_page = [
            "⚠️ Low oxygen detected in module A",
            "⚠️ Crew member heart rate elevated",
            "⚠️ Communication delay detected",
            "⚠️ Minor movement anomaly detected"
        ]
        add_alert(random.choice(alert_messages_page))

    if st.session_state.alerts:
        st.text_area("Recent Alerts", value="\n".join(st.session_state.alerts[-12:]), height=260)
    else:
        st.info("No alerts yet. Simulate to generate alerts.")
    st.markdown("</div>", unsafe_allow_html=True)

# ---- Page: All Original (verbatim) prompt ----
# This reminds judges that the original code blocks appear above unchanged.
if page == "All Original (verbatim) — Scroll Up":
    st.markdown("<div class='page-title'><h2>📜 Original Code Blocks (verbatim)</h2></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'><p>The two original referral code blocks are preserved verbatim at the top of this file. Scroll up to see them exactly as provided.</p></div>", unsafe_allow_html=True)

# -------------------------
# Footer
# -------------------------
st.markdown("<div class='footer'>MAITRI • Astronaut Dashboard — Single-file Multi-page (simulated) · All original code preserved</div>", unsafe_allow_html=True)
