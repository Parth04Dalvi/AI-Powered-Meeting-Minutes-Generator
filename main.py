import gradio as gr
import openai
import whisper
import os
import time

# You need to set your OpenAI API key as an environment variable
# export OPENAI_API_KEY='YOUR_API_KEY'
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load the Whisper model. 'base' is a good starting point for a balance of speed and accuracy.
# This will download the model the first time you run it.
try:
    whisper_model = whisper.load_model("base")
except Exception as e:
    print(f"Error loading Whisper model: {e}")
    print("Please ensure `openai-whisper` is installed correctly.")
    exit()

def transcribe_audio(audio_path):
    """Transcribes an audio file to text using the Whisper model."""
    try:
        start_time = time.time()
        result = whisper_model.transcribe(audio_path, fp16=False)
        end_time = time.time()
        print(f"Transcription took {end_time - start_time:.2f} seconds.")
        return result["text"]
    except Exception as e:
        return f"Error during transcription: {e}"

def generate_meeting_minutes(transcript):
    """Generates a summary of the transcript using OpenAI's API."""
    if not openai.api_key:
        return "Please set your OPENAI_API_KEY environment variable."
        
    prompt = f"""
    You are an AI assistant specialized in generating concise and professional meeting minutes.
    From the following meeting transcript, generate a summary that includes:
    1. A brief overview of the discussion.
    2. A list of key decisions made.
    3. A list of action items, including the person responsible and the due date if mentioned.
    4. Any important follow-up points.

    Transcript:
    {transcript}
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo-preview",  # Or 'gpt-3.5-turbo' for a cheaper alternative
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2048
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating summary: {e}"

def process_meeting(audio_file):
    """Main function to process the audio file and generate minutes."""
    if audio_file is None:
        return "Please upload an audio file first."
    
    transcript = transcribe_audio(audio_file)
    if "Error" in transcript:
        return f"Transcription failed: {transcript}"
    
    minutes = generate_meeting_minutes(transcript)
    return minutes

# Create a Gradio interface
with gr.Blocks(title="AI Meeting Minutes Generator") as demo:
    gr.Markdown("# AI Meeting Minutes Generator 🤖📝")
    gr.Markdown("Upload an audio file of your meeting to get a full transcript and a summarized meeting minutes report.")
    
    with gr.Row():
        audio_input = gr.Audio(type="filepath", label="Upload Meeting Audio File (MP3, WAV, M4A, etc.)")
        
    with gr.Row():
        process_btn = gr.Button("Generate Meeting Minutes")
    
    with gr.Column():
        output_minutes = gr.Textbox(label="Generated Meeting Minutes", lines=20, interactive=True)
    
    process_btn.click(
        fn=process_meeting,
        inputs=audio_input,
        outputs=output_minutes,
        api_name="generate_minutes"
    )

if __name__ == "__main__":
    demo.launch()
