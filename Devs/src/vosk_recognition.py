import os
import json
import wave
import pyaudio
from vosk import Model, KaldiRecognizer

class VoskRecognizer:
    def __init__(self, model_path):
        if not os.path.exists(model_path):
            raise FileNotFoundError("Model path does not exist.")
        self.model = Model(model_path)

    def record_audio(self, filename, duration=5):
        chunk = 1024
        sample_format = pyaudio.paInt16
        channels = 1
        fs = 16000
        p = pyaudio.PyAudio()
        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)
        frames = []
        print("Recording...")
        for _ in range(0, int(fs / chunk * duration)):
            data = stream.read(chunk)
            frames.append(data)
        print("Recording complete")
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()

    def transcribe_audio(self, filename):
        wf = wave.open(filename, "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
            raise ValueError("Audio file must be WAV format mono PCM.")
        rec = KaldiRecognizer(self.model, wf.getframerate())
        transcription = ""
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = rec.Result()
                transcription += json.loads(result)["text"] + " "
        result = rec.FinalResult()
        transcription += json.loads(result)["text"]
        return transcription.strip()

