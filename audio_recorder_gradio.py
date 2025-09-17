import sounddevice as sd
import numpy as np
import wave
import os

class GradioAudioRecorder:
    """A class to handle audio recording for Gradio applications."""
    
    def __init__(self, filename="meeting_audio.wav"):
        self.filename = filename
        self.sample_rate = 44100
        self.channels = 1
        self.recording_stream = None
        self.frames = []

    def start_recording(self):
        """Starts the audio recording."""
        self.frames = []
        self.recording_stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype='int16',
            callback=self._callback
        )
        self.recording_stream.start()
        return "Recording started... 🎙️"

    def _callback(self, indata, frames, time, status):
        """Callback function to append recorded frames."""
        if status:
            print(f"Recording status: {status}")
        self.frames.append(indata.copy())

    def stop_recording(self):
        """Stops the audio recording and saves the file."""
        if self.recording_stream and self.recording_stream.active:
            self.recording_stream.stop()
            self.recording_stream.close()
            
            # Save the recorded data to a WAV file
            with wave.open(self.filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(sd.default.dtype['int16'].itemsize)
                wf.setframerate(self.sample_rate)
                wf.writeframes(b''.join(self.frames))
            
            return f"Recording stopped and saved to {self.filename}. 🛑"
        return "No active recording found!"

    def get_file_path(self):
        """Returns the path of the saved audio file."""
        return self.filename

# Note: This class is designed to be used by the main Gradio app,
# so running it directly as a standalone script isn't the primary use case.
