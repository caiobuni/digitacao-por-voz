import os
from groq import Groq
from dotenv import load_dotenv

# Load key from .env
load_dotenv()

class GroqTranscriber:
    def __init__(self, api_key=None, model="whisper-large-v3", vocabulary=None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment or arguments.")
        self.client = Groq(api_key=self.api_key, timeout=30.0)
        self.model = model
        
        self.system_prompt = (
            "Olá! Tudo bem? Esta é uma transcrição em português do Brasil com "
            "excelente gramática, pontuação perfeita e clareza. Letras maiúsculas, "
            "vírgulas e pontos finais são usados corretamente."
        )
        if vocabulary:
            self.system_prompt += " Vocabulário frequente: " + ", ".join(vocabulary) + "."

    def transcribe(self, audio_file_path):
        """Transcribes the given audio file using Groq's Whisper API."""
        try:
            with open(audio_file_path, "rb") as file:
                transcription = self.client.audio.transcriptions.create(
                    file=(audio_file_path, file.read()),
                    model=self.model,
                    prompt=self.system_prompt,
                    response_format="json",
                    language="pt",
                    temperature=0.0
                )
            return transcription.text
        except Exception as e:
            print(f"Error during transcription: {e}")
            try:
                from logger import debug
                debug(f"Error during transcription: {e}")
            except Exception:
                pass
            return f"[ERRO NA TRANSCRIÇÃO: {str(e)}]"
        finally:
            # Delete the temp file after transcription
            if os.path.exists(audio_file_path):
                os.remove(audio_file_path)

# Manual test usage:
if __name__ == "__main__":
    transcriber = GroqTranscriber()
    # test_path = "path/to/test_audio.wav"
    # print(transcriber.transcribe(test_path))
