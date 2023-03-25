import openai
import threading
import keys

class Audio_Analysis:

    def __init__(self, audio_path):
        self.transcription = ""
        self.audio_path = audio_path
    
    def transcribe_audio(self):
        openai.api_key = keys.openaikey
        audio_file = open(self.audio_path, "rb")
        self.transcription = openai.Audio.transcribe("whisper-1", audio_file)

    def print_transcription(self):
        print(self.transcription)

    def start_analysis(self):
        audio_transcription_thread = threading.Thread(target=self.transcribe_audio)
        audio_transcription_thread.start()
        audio_transcription_thread.join()
