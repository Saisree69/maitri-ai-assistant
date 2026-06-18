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
