import logging
import numpy as np
import sounddevice as sd

logger = logging.getLogger(__name__)

SAMPLE_RATE = 44100
VOLUME = 0.16


def _tone(freq, duration, sample_rate=SAMPLE_RATE):
    n = int(sample_rate * duration)
    t = np.linspace(0, duration, n, endpoint=False)
    wave = np.sin(2 * np.pi * freq * t)
    overtone = 0.18 * np.sin(2 * np.pi * freq * 2 * t)
    fade = min(int(sample_rate * 0.012), n // 4)
    env = np.ones(n)
    if fade > 0:
        env[:fade] = np.linspace(0, 1, fade)
        env[-fade:] = np.linspace(1, 0, fade)
    return ((wave + overtone) * env * VOLUME).astype(np.float32)


def _play(samples):
    try:
        sd.play(samples, SAMPLE_RATE, blocking=True)
    except Exception as e:
        logger.error(f"Falha ao tocar som: {e}")


def play_start():
    _play(_tone(392.0, 0.12))


def play_stop():
    _play(_tone(415.3, 0.09))
