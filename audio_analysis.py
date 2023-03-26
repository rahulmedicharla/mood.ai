import openai
import threading, keys
from transformers import pipeline


class Audio_Analysis:

    def __init__(self, audio_path):
        #model inits
        self.sentiment_analysis_pipeline = pipeline('sentiment-analysis', model = 'distilbert-base-uncased-finetuned-sst-2-english')
        #data inits
        self.audio_path = audio_path
        self.transcription = ""
        self.sentiment_analysis = ""
    
    def transcribe_audio(self):
        openai.api_key = keys.openaikey
        audio_file = open(self.audio_path, "rb")
        transcription = openai.Audio.transcribe("whisper-1", audio_file)
        self.transcription = transcription["text"]
    
    def run_sentiment_analysis(self):
        formated_audio_transcription = [self.transcription]
        sentiment_analysis_results = self.sentiment_analysis_pipeline(formated_audio_transcription)

        self.sentiment_analysis = sentiment_analysis_results[0]['label']

    def print_audio_results(self):
        print(self.transcription)
        print(self.sentiment_analysis)

    def start_analysis(self):
        self.transcribe_audio()
        
        sentiment_analysis_thread = threading.Thread(target=self.run_sentiment_analysis)
        sentiment_analysis_thread.start()
        sentiment_analysis_thread.join()
