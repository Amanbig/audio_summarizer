# Meetings Summarizer

This project is a Audio Summarizer built with **Streamlit**. It allows users to upload video or audio files, transcribe content, summarize it, ask contextual questions, and convert summaries to audio.

## Features

### Features
- **Transcription**: Extract audio from video files and transcribe it using the Groq Whisper model.
- **Summarization**: Summarize the transcription with an AI model.
- **Question Answering**: Ask contextual questions based on the transcription or summary.
- **Text-to-Speech**: Convert text summaries into audio files.
- **File Upload**: Upload videos or audio files directly from the browser.
- **Real-time Updates**: Display transcriptions, summaries, and answers dynamically.
- **Audio Playback**: Listen to AI-generated audio summaries.
- **Responsive UI**: Styled with modern UI components and animations.

## Tech Stack

### Backend
- **Streamlit**: For building and testing apps.
- **Groq API**: For transcription and AI processing.
- **Pyttsx3**: For text-to-speech.
- **MoviePy**: For extracting audio from video.
- **Pydub**: For audio processing.
- **dotenv**: For environment variable management.

## Installation

### Backend

1. Clone the repository:
   ```bash
   git clone https://github.com/Amanbig/audio_summarizer.git
   ```

2. Create a virtual environment and activate it:
    ```bash
    cd meetings_app/backend
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Set up environment variables: Create a .env file and add your Groq API key:
    ```
    GROQ_API_KEY=<your-groq-api-key>
    ```

6. Run the backend
    ```bash
    streamlit run app.py
    ```

## Contributing

1. **Fork the repository** on GitHub.
2. **Create a new branch** (`git checkout -b feature/YourFeature`).
3. **Make your changes** and commit (`git commit -am 'Add new feature'`).
4. **Push to the branch** (`git push origin feature/YourFeature`).
5. **Create a new Pull Request for the changes made**.
