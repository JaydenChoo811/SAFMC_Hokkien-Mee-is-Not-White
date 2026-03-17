import sounddevice as sd
from scipy.io.wavfile import write
import config

def record_audio(filename, duration):
    fs = 16000  # Whisper prefers 16kHz

    print("[INFO] Listening...")

    recording = sd.rec(int(duration * fs),
                       samplerate=fs,
                       channels=1,
                       dtype='int16')

    sd.wait()

    write(filename, fs, recording)