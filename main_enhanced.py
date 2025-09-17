import gradio as gr
import openai
import whisper
import os
import time
import textwrap

# You must set your OpenAI API key as an environment variable.
# On Linux/Mac: export OPENAI_API_KEY='YOUR_API_KEY'
# On Windows: set OPENAI_API_KEY='YOUR_API_KEY'
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load the Whisper model once at the start of the program
try:
    whisper_model = whisper.load_model("base")
except Exception as e:
    print(f"Error loading Whisper model: {e}")
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

def generate_summary(text, is_final_summary=False):
    """
    Generates a summary of the provided text using OpenAI's API.
    `is_final_summary` flag adjusts the prompt for the final output.
    """
    if not openai.api_key:
        return "Please set your OPENAI_API_KEY environment variable."

    prompt_template = """
    You are an AI assistant specialized in generating concise and professional meeting minutes.
    From the following text, generate a summary that includes:
    1. A brief overview of the discussion.
    2. A list of key decisions made.
    3. A list of action items, including the person responsible and the due date if mentioned.
    4. Any important follow-up points.

    Text to summarize:
    {text}
    """
    
    if is_final_summary:
        prompt_template = """
        You are an AI assistant specialized in generating a final, consolidated meeting minutes report.
        Combine the following summaries into a single, comprehensive report. The report should be well-structured and easy to read.
        
        Summaries to consolidate:
        {text}
        """

    prompt = prompt_template.format(text=text)

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo-preview",
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

def process_meeting_with_chunking(audio_file):
    """Main function to process the audio file and generate minutes, with chunking for long files."""
    if audio_file is None:
        return "Please upload an audio file first."
    
    # 1. Transcribe the audio
    transcript = transcribe_audio(audio_file)
    if "Error" in transcript:
        return f"Transcription failed: {transcript}"

    # Define a character limit for API calls to avoid hitting token limits
    # A safe bet is around 10,000 characters, well below most model limits
    # to account for the prompt text as well.
    chunk_size = 10000 
    
    if len(transcript) > chunk_size:
        # If the transcript is too long, split it into chunks
        chunks = textwrap.wrap(transcript, chunk_size, break_long_words=False, replace_whitespace=False)
        summaries = []
        for i, chunk in enumerate(chunks):
            # Summarize each chunk
            print(f"Summarizing chunk {i+1} of {len(chunks)}...")
            chunk_summary = generate_summary(chunk)
            summaries.append(chunk_summary)
            # Add a small delay to avoid hitting rate limits
            time.sleep(1)

        # Combine and summarize the summaries
        print("Consolidating summaries...")
        final_minutes = generate_summary("\n".join(summaries), is_final_summary=True)
    else:
        # If the transcript is short, summarize it directly
        final_minutes = generate_summary(transcript)

    return final_minutes

# Create a Gradio interface
with gr.Blocks(title="AI Meeting Minutes Generator") as demo:
    gr.Markdown("# AI Meeting Minutes Generator 🤖📝")
    gr.Markdown("Upload an audio file or record a meeting live to get a full transcript and a summarized meeting minutes report.")
    
    with gr.Tab("Upload Audio"):
        audio_input_upload = gr.Audio(type="filepath", label="Upload Meeting Audio File (MP3, WAV, M4A, etc.)")
        upload_btn = gr.Button("Generate Meeting Minutes from Upload")
        upload_output = gr.Textbox(label="Generated Meeting Minutes", lines=20, interactive=True)
        upload_btn.click(fn=process_meeting_with_chunking, inputs=audio_input_upload, outputs=upload_output)
    
    with gr.Tab("Live Recording"):
        gr.Markdown("Start and stop the recording. The audio will be automatically transcribed and summarized.")
        audio_input_record = gr.Audio(sources=["microphone"], type="filepath", label="Live Recording")
        record_btn = gr.Button("Generate Minutes from Recording")
        record_output = gr.Textbox(label="Generated Meeting Minutes", lines=20, interactive=True)
        record_btn.click(fn=process_meeting_with_chunking, inputs=audio_input_record, outputs=record_output)

if __name__ == "__main__":
    demo.launch()
