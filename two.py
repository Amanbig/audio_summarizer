import streamlit as st
import os
import tempfile
import pyttsx3
from pydub import AudioSegment
from groq import Groq
from dotenv import load_dotenv

# Initialize TTS engine
engine = pyttsx3.init()

# Load environment variables
load_dotenv()

# Check for required environment variables
HF_TOKEN = os.getenv("HF_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not HF_TOKEN or not GROQ_API_KEY:
    st.error("❌ Missing required environment variables. Please check your HF_TOKEN and GROQ_API_KEY.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Initialize the tools (assuming you have tools like ImageCaptionTool, ObjectDetectionTool, etc.)
# If these tools aren't available, you can remove or adjust accordingly.
from tools import ImageCaptionTool, ObjectDetectionTool, VisualQuestionAnsweringTool

image_caption_tool = ImageCaptionTool()
object_detection_tool = ObjectDetectionTool()
vqa_tool = VisualQuestionAnsweringTool()

# Set up Streamlit app style
st.markdown(
    """
<style>
    /* Main background and text colors */
    body {
        color: #E0E0E0;
        background-color: #1E1E1E;
    }
    .stApp {
        background-color: #1E1E1E;
    }
    /* Headings */
    h1, h2, h3 {
        color: #BB86FC;
    }
    /* Buttons */
    .stButton>button {
        color: #1E1E1E;
        background-color: #BB86FC;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #A66EFC;
    }
    /* File uploader */
    .stFileUploader {
        background-color: #2E2E2E;
        border: 1px solid #BB86FC;
        border-radius: 4px;
        padding: 1rem;
    }
    /* Audio player */
    .stAudio {
        background-color: #2E2E2E;
        border-radius: 4px;
        padding: 0.5rem;
    }
    /* Text areas (for transcription output) */
    .stTextArea textarea {
        background-color: #2E2E2E;
        color: #E0E0E0;
        border: 1px solid #BB86FC;
        border-radius: 4px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Function to convert text to audio and return the file path
def text_to_audio_file(text, filename):
    # Set properties for TTS
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)

    # Save the audio to a file
    engine.save_to_file(text, filename)
    engine.runAndWait()  # Ensure the speech is saved
    print(f"Audio saved as {filename}")
    
    return filename  # Return the file path of the saved audio file

# Streamlit UI Components for Transcription and Summarization
st.title("🎙️ Meeting/Podcast Summarizer")

# File uploader for audio or video file
uploaded_file = st.file_uploader("Choose an audio or video file", type=["wav", "mp3", "mp4"])

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    if uploaded_file.type.startswith("audio"):
        st.audio(file_bytes)
    elif uploaded_file.type.startswith("video"):
        st.audio(file_bytes)

# Buttons for actions
col1, col2, col3 = st.columns(3)
with col1:
    transcribe_button = st.button("🎬 Transcribe")
with col2:
    summarize_button = st.button("📝 Summarize")
with col3:
    convert_button = st.button("Convert")

col_summary = st.container()

# Handle transcription logic
if transcribe_button:
    # (Transcription logic goes here, possibly using Whisper or another service)
    pass

# Handle summarization logic
if summarize_button:
    # (Summarization logic goes here, possibly using GPT-3 or another model)
    pass

# Convert text summary to audio and play it
if convert_button:
    if "summary" in st.session_state:  # Check if the summary exists in session state
        with st.spinner("Converting summary to audio..."):
            try:
                summary = st.session_state.summary  # Retrieve summary from session state
                audio_file_path = "output_audio.wav"  # Define path for the saved audio file

                # Convert the summary to audio
                audio_file_path = text_to_audio_file(summary, audio_file_path)

                # Play the audio using Streamlit
                st.audio(audio_file_path, format="audio/wav")

            except Exception as e:
                st.error(f"❌ An error occurred during conversion: {str(e)}")
    else:
        st.warning("Please summarize the transcription first.")
