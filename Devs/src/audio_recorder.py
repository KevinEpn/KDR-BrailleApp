import threading
import pyaudio
import wave
import tempfile
import os
import atexit

class AudioRecorder:
    def __init__(self):
        self.stop_event = threading.Event()
        self.temp_dir = tempfile.gettempdir()
        self.filename = os.path.join(self.temp_dir, "temp_audio.wav")
        self.frames = []
        self.p = pyaudio.PyAudio()
        self.stream = None
        atexit.register(self.cleanup)

    def record_audio(self):
        
        chunk = 1024
        sample_format = pyaudio.paInt16
        channels = 1
        fs = 16000
        
        
        self.stream = self.p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True,
                        stream_callback = self.callback)
        
        self.frames = []
        print("Recording...")
        
    def stop_recording(self):
        # self.stop_event.set()
        self.stream.stop_stream()
        self.stream.close()

        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        print("Recording complete")

    def callback(self, in_data, frame_count, time_info, status):
        if status:
            print(status)
        self.frames.append(in_data)
        return in_data, pyaudio.paContinue

    def get_filename(self):
        return self.filename
    
    def cleanup(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)