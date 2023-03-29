import threading, pyaudio, wave

class AudioInput:
    def __init__(self):
        self.open = True
        self.rate = 44100
        self.frames_per_buffer = 1024
        self.channels = 2
        self.format = pyaudio.paInt16
        self.audio_filename = "audio_file.wav"
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format,channels=self.channels,rate=self.rate,input=True, frames_per_buffer = self.frames_per_buffer)
        self.audio_frames = []

    def collect_audio(self):
        self.stream.start_stream()
        while(self.open == True):
            data = self.stream.read(self.frames_per_buffer) 
            self.audio_frames.append(data)
            if self.open==False:
                break

    def stop_audio(self):
        if self.open==True:
            self.open = False
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
               
            waveFile = wave.open(self.audio_filename, 'wb')
            waveFile.setnchannels(self.channels)
            waveFile.setsampwidth(self.audio.get_sample_size(self.format))
            waveFile.setframerate(self.rate)
            waveFile.writeframes(b''.join(self.audio_frames))
            waveFile.close()

    def start_audio(self):
        audio_thread = threading.Thread(target=self.collect_audio)
        audio_thread.start()