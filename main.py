import os
import re
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
        
        self.recorder.on_phrase_complete = self._process_phrase
        
        self.is_recording = False
        self.running = True
        self._media_was_playing = False

    HALLUCINATION_PHRASES = {
        "legenda por sônia ruberti",
        "legenda por sonia ruberti",
        "obrigado",
        "obrigado!",
        "thanks for watching",
        "thank you for watching",
        "inscreva-se no canal",
        "deixe seu like",
    }

    @staticmethod
    def _clean_text(text):
        if not text:
            return text
        text = re.sub(r'\.{2,}', ' ', text)
        text = re.sub(r'…+', ' ', text)
        text = re.sub(r'(?:\.\s+){2,}\.', ' ', text)
        text = re.sub(r'\s{2,}', ' ', text)
        text = text.strip()
        return text

    def _process_phrase(self, audio_path):
        print(f"Processing phrase from {audio_path}...")
        text = self.transcriber.transcribe(audio_path)
        if text:
            if text.strip().lower() in self.HALLUCINATION_PHRASES:
                print(f"Filtered hallucination: {text}")
                return
            text = self._clean_text(text)
            if text:
                print(f"Transcribed: {text}")
                self.typer.insert_text(text + " ")
                self.logger.log(text)

    def _toggle_media(self):
        try:
            from pynput.keyboard import Controller, Key
            keyboard_controller = Controller()
            keyboard_controller.press(Key.media_play_pause)
            keyboard_controller.release(Key.media_play_pause)
        except Exception as e:
            print(f"Could not toggle media: {e}")

    def _is_media_playing(self):
        result = [False]
        def _check():
            try:
                import pythoncom
                from pycaw.utils import AudioUtilities
                from pycaw.pycaw import IAudioMeterInformation

                pythoncom.CoInitialize()

                def _has_playing_session():
                    sessions = AudioUtilities.GetAllSessions()
                    for s in sessions:
                        if s.Process is None:
                            continue
                        if s.State != 1:
                            continue
                        try:
                            meter = s._ctl.QueryInterface(IAudioMeterInformation)
                            if meter.GetPeakValue() > 0.0:
                                return True
                        except Exception:
                            pass
                    return False

                first = _has_playing_session()
                if first:
                    time.sleep(0.15)
                    second = _has_playing_session()
                    result[0] = second
            except Exception as e:
                print(f"Could not check media state: {e}")
            finally:
                try:
                    pythoncom.CoUninitialize()
                except Exception:
                    pass
        t = threading.Thread(target=_check, daemon=True)
        t.start()
        t.join(timeout=1.0)
        return result[0]

    def on_press(self, key):
        if not self.running:
            return False

        if key == keyboard.Key.pause:
            if not self.is_recording:
                self._media_was_playing = self._is_media_playing()
                if self._media_was_playing:
                    print(">>> Recording started (Media Paused)")
                    self._toggle_media()
                else:
                    print(">>> Recording started (No media playing)")
                self.is_recording = True
                self.recorder.start()

    def on_release(self, key):
        if key == keyboard.Key.pause:
            if self.is_recording:
                self.is_recording = False
                self.recorder.stop()
                if self._media_was_playing:
                    print("<<< Recording stopped (Media Resumed)")
                    self._toggle_media()
                else:
                    print("<<< Recording stopped")
                self._media_was_playing = False

    def run(self):
        self.tray = TrayApp(
            on_open_log=self.logger.open_log,
            on_quit=self.quit
        )
        tray_thread = threading.Thread(target=self.tray.run, daemon=True)
        tray_thread.start()

        print("Verbatim is running. Hold the 'Pause/Break' key to speak.")
        
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
