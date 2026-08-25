import os
import queue
import threading
import numpy as np
import sounddevice as sd
import soundfile as sf
import tempfile
import time

class AudioRecorder:
    def __init__(self, sample_rate=16000, channels=1, silence_threshold=0.01, silence_duration=1.0):
        self.sample_rate = sample_rate
        self.channels = channels
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        self.audio_queue = queue.Queue()
        self.recording = False
        self.stream = None
        self.chunks = []
        self.last_speech_time = time.time()
        self.on_phrase_complete = None # Callback function(file_path)

    def _audio_callback(self, indata, frames, time_info, status):
        if status:
            print(f"Error in audio stream: {status}")
        self.audio_queue.put(indata.copy())

    def start(self):
        if self.recording:
            return
        
        self.recording = True
        self.chunks = []
        self.last_speech_time = time.time()
        try:
            sd.stop()
        except Exception:
            pass
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=self._audio_callback
        )
        self.stream.start()
        self.recording_thread = threading.Thread(target=self._process_audio)
        self.recording_thread.start()

    def stop(self):
        if not self.recording:
            return
        
        self.recording = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
        
        if self.recording_thread.is_alive():
            self.recording_thread.join()
        
        # Save any remaining audio as the final phrase
        if self.chunks:
            self._save_and_callback()

    def _process_audio(self):
        while self.recording:
            try:
                data = self.audio_queue.get(timeout=0.1)
                self.chunks.append(data)
                
                # Simple VAD based on amplitude
                if np.max(np.abs(data)) > self.silence_threshold:
                    self.last_speech_time = time.time()
                else:
                    # Check for silence duration
                    if time.time() - self.last_speech_time > self.silence_duration and len(self.chunks) > 10:
                        # Significant silence detected after some audio
                        self._save_and_callback()
            except queue.Empty:
                continue

    def _save_and_callback(self):
        if not self.chunks:
            return
        
        audio_data = np.concatenate(self.chunks, axis=0)
        self.chunks = [] # Reset for next phrase
        
        # Discard audio if it's entirely silence
        if np.max(np.abs(audio_data)) <= self.silence_threshold:
            print("Audio contains only silence. Discarding to prevent hallucination.")
            return
        
        # Save to temp file
        fd, path = tempfile.mkstemp(suffix=".wav")
        os.close(fd)
        
        sf.write(path, audio_data, self.sample_rate)
        
        if self.on_phrase_complete:
            self.on_phrase_complete(path)

# Manual test usage:
if __name__ == "__main__":
    def my_callback(path):
        print(f"Phrase complete! Saved to {path}")
        # Here we would send to Groq
    
    recorder = AudioRecorder(silence_duration=0.8)
    recorder.on_phrase_complete = my_callback
    
    print("Recording manual test (5 seconds)...")
    recorder.start()
    time.sleep(5)
    recorder.stop()
    print("Recording stopped.")
