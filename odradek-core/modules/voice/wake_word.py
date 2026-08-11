import config
import os
import json

class WakeWordListener:
    def __init__(self):
        self.recognizer = None
        self.audio_stream = None
        self.model = None
        self.keyword = "computer"

        if os.path.exists(config.VOSK_MODEL_PATH):
            try:
                from vosk import Model, KaldiRecognizer
                import pyaudio

                self.model = Model(config.VOSK_MODEL_PATH)
                self.recognizer = KaldiRecognizer(self.model, 16000)

                pa = pyaudio.PyAudio()
                self.audio_stream = pa.open(
                    rate=16000, channels=1,
                    format=pyaudio.paInt16, input=True,
                    frames_per_buffer=4000
                )
                print("Vosk wake word listener active.")
            except Exception as e:
                print(f"Vosk wake word failed ({e})")
        else:
            print(f"Vosk model not found at {config.VOSK_MODEL_PATH}")
            print("Wake word disabled — run 'python test_detector.py' for vision-only testing.")

    def detect(self):
        if self.recognizer and self.audio_stream:
            try:
                data = self.audio_stream.read(4000, exception_on_overflow=False)
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "").lower()
                    if self.keyword in text:
                        print(f"Wake word detected!")
                        return True
            except:
                pass
        return False
