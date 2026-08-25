import io
import logging
import wave
import winsound

import numpy as np

logger = logging.getLogger(__name__)

SAMPLE_RATE = 44100
VOLUME = 0.16


def _tone(freq, duration, sample_rate=SAMPLE_RATE):
    n = int(sample_rate * duration)
    t = np.linspace(0, duration, n, endpoint=False)
    wave_data = np.sin(2 * np.pi * freq * t)
    overtone = 0.18 * np.sin(2 * np.pi * freq * 2 * t)
    fade = min(int(sample_rate * 0.012), n // 4)
    env = np.ones(n)
    if fade > 0:
        env[:fade] = np.linspace(0, 1, fade)
        env[-fade:] = np.linspace(1, 0, fade)
    return ((wave_data + overtone) * env * VOLUME).astype(np.float32)


def _to_wav_bytes(samples):
    pcm = (np.clip(samples, -1.0, 1.0) * 32767).astype(np.int16)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(pcm.tobytes())
    return buf.getvalue()


def _play(samples):
    try:
        winsound.PlaySound(_to_wav_bytes(samples), winsound.SND_MEMORY | winsound.SND_NODEFAULT)
    except Exception as e:
        logger.error(f"Falha ao tocar som: {e}")


def play_start():
    _play(_tone(392.0, 0.12))


def play_stop():
    _play(_tone(415.3, 0.09))
