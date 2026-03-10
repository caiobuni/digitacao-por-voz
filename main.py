import time
import threading
from pynput import keyboard
from recorder import AudioRecorder
from transcriber import GroqTranscriber
from typer import TextOut
from logger import HistoryLogger
from tray import TrayApp

class VerbatimApp:
    def __init__(self):
        self.recorder = AudioRecorder(silence_duration=0.8)
        self.transcriber = GroqTranscriber()
        self.typer = TextOut()
        self.logger = HistoryLogger()
        
        # Connect recorder to transcription and output
        self.recorder.on_phrase_complete = self._process_phrase
        
        self.is_recording = False
        self.running = True

    def _process_phrase(self, audio_path):
        """Callback from AudioRecorder when a phrase is ready."""
        print(f"Processing phrase from {audio_path}...")
        text = self.transcriber.transcribe(audio_path)
        if text:
            print(f"Transcribed: {text}")
            self.typer.paste_text(text)
            self.logger.log(text)

    def _toggle_media(self):
        """Tenta enviar o comando de Play/Pause de mídia."""
        try:
            from pynput.keyboard import Controller, Key
            keyboard_controller = Controller()
            keyboard_controller.press(Key.media_play_pause)
            keyboard_controller.release(Key.media_play_pause)
        except Exception as e:
            print(f"Could not toggle media: {e}")

    def on_press(self, key):
        if not self.running:
            return False

        # Tecla Pause/Break
        if key == keyboard.Key.pause:
            if not self.is_recording:
                print(">>> Recording started (Media Paused)")
                self._toggle_media()
                self.is_recording = True
                self.recorder.start()

    def on_release(self, key):
        # Tecla Pause/Break
        if key == keyboard.Key.pause:
            if self.is_recording:
                print("<<< Recording stopped (Media Resumed)")
                self.is_recording = False
                self.recorder.stop()
                self._toggle_media()

    def run(self):
        # Start Tray in a separate thread
        self.tray = TrayApp(
            on_open_log=self.logger.open_log,
            on_quit=self.quit
        )
        tray_thread = threading.Thread(target=self.tray.run, daemon=True)
        tray_thread.start()

        print("Verbatim is running. Hold the 'Pause/Break' key to speak.")
        
        # Start Keyboard Listener in the main thread
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            self.kb_listener = listener
            listener.join()

    def quit(self):
        print("Quitting Verbatim...")
        self.running = False
        self.recorder.stop()
        if hasattr(self, 'kb_listener'):
            self.kb_listener.stop()

if __name__ == "__main__":
    app = VerbatimApp()
    app.run()
