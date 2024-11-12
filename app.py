import streamlit as st
import os
import tempfile
import pyttsx3
from pydub import AudioSegment
from groq import Groq
from moviepy.editor import VideoFileClip
import base64

# Initialize TTS engine
engine = pyttsx3.init()

# Check for required environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("❌ Missing required environment variables. Please check your GROQ_API_KEY.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Streamlit UI Components for Transcription and Summarization
st.title("🎙️ Meeting/Podcast Summarizer")

uploaded_file = st.file_uploader("Choose an audio or video file", type=["wav", "mp3", "mp4"])

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    background_image = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{bin_str}");
        background-size: cover;
        background-position: center top 0px;
    }}
    </style>
    """
    st.markdown(background_image, unsafe_allow_html=True)

set_background('image.png')

# Function to extract audio
def extract_audio_from_video(video_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
        with VideoFileClip(video_file) as video:
            video.audio.write_audiofile(temp_audio_file.name, codec="mp3")
        return temp_audio_file.name

# Transcription function
def transcribe_audio(audio_file):
    with open(audio_file, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(os.path.basename(audio_file), file.read()),
            model="whisper-large-v3",
            response_format="json",
            language="en",
            temperature=0.0,
        )
    return transcription.text

# Text-to-audio conversion
def text_to_audio_file(text, filename):
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)
    engine.save_to_file(text, filename)
    engine.runAndWait()
    return filename

# Custom Groq-based question-answering function
from groq import Groq

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

def groq_question_answer(question, context):
    try:
        # Set up the message structure for a question-answering task
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant. Answer the user's question based on the provided context."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}"
            }
        ]
        
        # Make the API call to create a chat completion
        response = client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192",  # Replace with the specific model required
            temperature=0.5,
            max_tokens=150
        )
        
        # Extract the answer from the response
        answer = response.choices[0].message.content.strip()
        return answer if answer else "No answer available"
    except Exception as e:
        # Handle errors and return an error message
        return f"Error in fetching answer: {str(e)}"

# State for transcription and summary
if 'transcription' not in st.session_state:
    st.session_state.transcription = ""
if 'summary' not in st.session_state:
    st.session_state.summary = ""

# Display uploaded file and conversion options
if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    if uploaded_file.type.startswith("audio"):
        st.audio(file_bytes)
    elif uploaded_file.type.startswith("video"):
        st.audio(file_bytes)

    # Transcription button
    if st.button("🎬 Transcribe"):
        with st.spinner("Transcribing..."):
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix="." + uploaded_file.name.split(".")[-1]) as temp_file:
                    temp_file.write(file_bytes)
                    temp_file_path = temp_file.name

                if uploaded_file.type.startswith("video"):
                    audio_file_path = extract_audio_from_video(temp_file_path)
                    os.unlink(temp_file_path)
                    temp_file_path = audio_file_path

                transcription = transcribe_audio(temp_file_path)
                st.session_state.transcription = transcription
                os.unlink(temp_file_path)

                st.subheader("📝 Transcription:")
                st.text_area("", value=transcription, height=300, max_chars=None, key="transcription_output")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")

# Summarization button
if st.session_state.transcription and st.button("📝 Summarize"):
    with st.spinner("Summarizing..."):
        try:
            response = client.chat.completions.create(
                messages=[ 
                    {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                    {"role": "user", "content": f"Please summarize the following transcription:\n\n{st.session_state.transcription}"}
                ],
                model="llama-3.2-90b-text-preview",
                temperature=0.5,
            )
            summary = response.choices[0].message.content
            st.session_state.summary = summary

            st.subheader("📋 Summary:")
            st.markdown(summary)
        except Exception as e:
            st.error(f"❌ An error occurred during summarization: {str(e)}")

# Convert Summary to Audio button
if st.session_state.summary:
    if st.button("Convert Summary to Audio"):
        with st.spinner("Converting summary to audio..."):
            try:
                audio_file_path = "output_audio.wav"
                audio_file_path = text_to_audio_file(st.session_state.summary, audio_file_path)
                st.audio(audio_file_path, format="audio/wav")
            except Exception as e:
                st.error(f"❌ An error occurred during conversion: {str(e)}")

# Question-answering section
if st.session_state.summary:
    st.write("### Ask a question based on the summary")
    question = st.text_input("Enter your question here:")
    if question:
        with st.spinner("Getting answer..."):
            try:
                answer = groq_question_answer(question=question, context=st.session_state.summary)
                st.write(f"**Answer:** {answer}")
            except Exception as e:
                st.error(f"❌ An error occurred while getting the answer: {str(e)}")
