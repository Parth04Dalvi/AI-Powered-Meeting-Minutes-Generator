
AI-Powered Meeting Minutes Generator 📝
This project is an AI-powered tool that automates the creation of meeting minutes. It uses a state-of-the-art speech-to-text model to transcribe meeting audio and a large language model (LLM) to summarize the transcript into a professional, well-structured report.

You can either upload a pre-recorded audio file or use the built-in feature to record a meeting live directly from your web browser.

✨ Features
🎙️ Live Audio Recording: Record your meeting directly through the web interface.

⬆️ Audio File Uploads: Process audio files in various formats (MP3, WAV, M4A, etc.).

🗣️ Accurate Transcription: Utilizes OpenAI's Whisper model for highly accurate speech-to-text transcription.

🤖 Intelligent Summarization: Employs the GPT-4 (or GPT-3.5) model to generate structured meeting minutes, including:

A brief overview of the discussion.

A list of key decisions made.

A list of action items with assigned owners.

✂️ Scalable for Long Meetings: Automatically handles long transcripts by splitting them into smaller chunks and summarizing them incrementally, ensuring you don't hit API token limits.

🌐 User-Friendly Interface: A simple web-based interface built with Gradio that requires no technical expertise to use.

🚀 Getting Started
Prerequisites
Before you begin, you'll need the following:

Python 3.8+

An OpenAI API Key for accessing the summarization model. You can get one from the OpenAI platform website.

Installation
Clone this repository:

Bash

git clone https://github.com/your-username/your-project-name.git
cd your-project-name
Create and activate a virtual environment (recommended):

Bash

python -m venv venv
# For Windows:
# venv\Scripts\activate
# For macOS/Linux:
# source venv/bin/activate
Install the required Python packages:

Bash

pip install -r requirements.txt
(Note: The requirements.txt file should contain the libraries listed in the project code: openai-whisper, openai, gradio, sounddevice, numpy, pydub, PyAudio).

API Key Configuration
Set your OpenAI API key as an environment variable. This is the most secure way to manage your key.

On macOS/Linux:

Bash

export OPENAI_API_KEY='your_api_key_here'
On Windows (Command Prompt):

Bash

set OPENAI_API_KEY='your_api_key_here'
🏃 How to Run the App
Make sure you have completed the Installation and API Key Configuration steps.

Run the main application script from your terminal:

Bash

python main_enhanced.py
The application will start, and a public URL will be displayed in your terminal. Open this URL in your web browser.

On the web page, you can either:

Upload Audio: Drag and drop an audio file into the designated box and click "Generate Meeting Minutes."

Live Recording: Go to the "Live Recording" tab, click the microphone button to start recording, and then click it again to stop. Once the recording is complete, click "Generate Minutes from Recording."

The generated meeting minutes will appear in the text box below.

⚙️ Technologies Used
Whisper: A general-purpose speech recognition model by OpenAI for audio transcription.

GPT-4-Turbo: An advanced large language model by OpenAI for generating high-quality, structured summaries.

Gradio: An open-source Python library that allows you to quickly create a web UI for your machine learning models.

sounddevice & PyAudio: Libraries for cross-platform audio input/output, enabling live microphone recording.

Python: The core programming language for the project.
