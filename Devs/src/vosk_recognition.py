import os
import json
import wave
import pyaudio
from vosk import Model, KaldiRecognizer
from src.audio_recorder import AudioRecorder

class VoskRecognizer:
    def __init__(self, model_path):
        if not os.path.exists(model_path):
            raise FileNotFoundError("Model path does not exist.")
        self.model = Model(model_path)


    def get_raw_audio(self):
        return AudioRecorder().get_filename()


    def transcribe_audio(self):
        filename = self.get_raw_audio()
        wf = wave.open(filename, "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
            raise ValueError("Audio file must be WAV format mono PCM.")
        rec = KaldiRecognizer(self.model, wf.getframerate())
        self.transcription = ""
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = rec.Result()
                self.transcription += json.loads(result)["text"] + " "
        result = rec.FinalResult()
        self.transcription += json.loads(result)["text"]
        return self.transcription.strip()

