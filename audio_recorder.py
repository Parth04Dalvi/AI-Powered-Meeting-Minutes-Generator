import sounddevice as sd
import numpy as np
import wave
import threading
import time

class AudioRecorder:
    def __init__(self):
        self.is_recording = False
        self.frames = []
        self.thread = None
        self.sample_rate = 44100
        self.channels = 1
        self.filename = "meeting_audio.wav"

    def _record_audio(self):
        """Internal method to record audio in a separate thread."""
        with sd.InputStream(samplerate=self.sample_rate, channels=self.channels, dtype='int16') as stream:
            while self.is_recording:
                data, overflowed = stream.read(1024)
                if overflowed:
                    print("Audio buffer overflowed!")
                self.frames.append(data.copy())
                time.sleep(0.01)

    def start_recording(self):
        """Starts a new recording session."""
        if not self.is_recording:
            self.is_recording = True
            self.frames = []
            self.thread = threading.Thread(target=self._record_audio)
            self.thread.start()
            return "Recording started... 🎙️"
        return "Already recording!"

    def stop_recording(self):
        """Stops the recording and saves the audio file."""
        if self.is_recording:
            self.is_recording = False
            if self.thread:
                self.thread.join()
            
            # Save the recorded data to a WAV file
            wf = wave.open(self.filename, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(sd.default.dtype['int16'].itemsize)
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            return f"Recording stopped and saved to {self.filename}. 🛑"
        return "Not currently recording!"

    def get_audio_file(self):
        """Returns the path to the saved audio file."""
        return self.filename

if __name__ == '__main__':
    recorder = AudioRecorder()
    print(recorder.start_recording())
    time.sleep(5)  # Record for 5 seconds
    print(recorder.stop_recording())
