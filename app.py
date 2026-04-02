import streamlit as st
import sounddevice as sd
import numpy as np
import tempfile
import wave
from googletrans import Translator
import pandas as pd
import os

# Initialize translator
translator = Translator()

# Function to record audio using sounddevice
def record_audio(duration=5, fs=16000):
    st.info("Recording... Please speak your complaint.")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    return np.squeeze(audio)

# Save audio to temporary WAV file
def save_audio(audio, fs=16000):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    with wave.open(temp_file.name, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(fs)
        wf.writeframes(audio.tobytes())
    return temp_file.name

# Dummy speech-to-text (replace with Whisper/Vosk for real STT)
def speech_to_text(audio_file):
    # For now, just return a placeholder
    # You can integrate Whisper or Vosk here
    return "This is a placeholder transcription of your voice input."

# Complaint processing
def process_complaint(input_text, src_lang="auto", target_lang="en"):
    translated = translator.translate(input_text, src=src_lang, dest=target_lang).text
    structured_data = {
        "Original Complaint": input_text,
        "Translated Complaint": translated,
        "Category": "General",  # Placeholder
        "Urgency": "Normal"     # Placeholder
    }
    return structured_data

# Streamlit UI
st.title("AI-Powered Multilingual Complaint Portal")
st.write("Breaking Language Barriers for Faster Justice")

option = st.radio("Choose input method:", ["Text", "Voice"])

if option == "Text":
    user_input = st.text_area("Enter your complaint in any language:")
    if st.button("Submit Complaint") and user_input.strip() != "":
        result = process_complaint(user_input)
        st.success("Complaint processed successfully!")
        st.write(pd.DataFrame([result]))

elif option == "Voice":
    duration = st.slider("Recording duration (seconds)", 3, 10, 5)
    if st.button("Record Complaint"):
        audio = record_audio(duration=duration)
        audio_file = save_audio(audio)
        voice_text = speech_to_text(audio_file)
        os.remove(audio_file)  # cleanup temp file
        result = process_complaint(voice_text)
        st.success("Complaint processed successfully!")
        st.write(pd.DataFrame([result]))

# Future scope sidebar
st.sidebar.header("Future Scope")
st.sidebar.write("- Mobile App Integration")
st.sidebar.write("- Real-Time Alerts to Police")
st.sidebar.write("- Support for More Languages")
st.sidebar.write("- Smart City System Integration")