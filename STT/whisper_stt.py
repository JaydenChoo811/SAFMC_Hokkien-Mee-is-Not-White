import sounddevice as sd
import numpy as np
import whisper
import queue
import threading
import time

class StreamingWhisper:
    def __init__(self, model_size="base", samplerate=16000):
        print("[INFO] Loading Whisper model...")
        self.model = whisper.load_model(model_size)

        self.samplerate = samplerate
        self.q = queue.Queue()

        self.buffer = np.zeros((0,), dtype=np.float32)
        self.buffer_duration = 3  # seconds

        self.running = True

    def audio_callback(self, indata, frames, time_info, status):
        if status:
            print(status)
        self.q.put(indata.copy())

    def start_stream(self):
        self.stream = sd.InputStream(
            samplerate=self.samplerate,
            channels=1,
            callback=self.audio_callback
        )
        self.stream.start()

        threading.Thread(target=self.process_audio, daemon=True).start()

    def process_audio(self):
        while self.running:
            while not self.q.empty():
                data = self.q.get()
                data = data.flatten().astype(np.float32) / 32768.0

                self.buffer = np.concatenate((self.buffer, data))

                # keep last N seconds
                max_samples = int(self.buffer_duration * self.samplerate)
                if len(self.buffer) > max_samples:
                    self.buffer = self.buffer[-max_samples:]

            time.sleep(0.1)

    def listen(self):
        # run transcription on current buffer
        if len(self.buffer) < self.samplerate:
            return ""

        result = self.model.transcribe(self.buffer, fp16=False)
        text = result['text'].lower().strip()

        return text

    def stop(self):
        self.running = False
        self.stream.stop()
        self.stream.close()