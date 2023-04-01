import openai
import threading, keys
from transformers import pipeline
import spacy
import numpy as np
from scipy.io.wavfile import read

class Audio_Analysis:

    def __init__(self, audio_path):
        #model inits
        self.sentiment_analysis_pipeline = pipeline('sentiment-analysis', model = 'distilbert-base-uncased-finetuned-sst-2-english')
        self.emotion_detection_pipeline = pipeline('sentiment-analysis', model='arpanghoshal/EmoRoBERTa')
        self.keyword_detection_pipeline = spacy.load('en_core_web_sm')

        #whisper inits
        self.openaikey = keys.openaikey

        #data inits
        self.audio_path = audio_path
        self.transcription_array = []
        self.transcription = ""
        self.sentiment_analysis = []
        self.emotion_detection = []
        self.keywords = ()
        self.energy_level = "Low"
    
    def transcribe_audio(self):
        openai.api_key = self.openaikey
        audio_file = open(self.audio_path, "rb")
        transcription = openai.Audio.transcribe("whisper-1", audio_file)
        self.transcription = transcription["text"]
        self.transcription_array = transcription["text"].split('.')

    def run_energy_detection(self):
        fs, amplitude = read('audio_file.wav')

        avg_amplitude = np.mean(np.abs(amplitude))
        if avg_amplitude > 500:
            self.energy_level = "High"
    
    def run_sentiment_analysis(self):
        sentiment_analysis_results = self.sentiment_analysis_pipeline(self.transcription_array)

        self.sentiment_analysis = self.convert_analysis_result_to_array(sentiment_analysis_results)

    def run_emotion_detection(self):
        emotion_detection_results = self.emotion_detection_pipeline(self.transcription_array)

        self.emotion_detection = self.convert_analysis_result_to_array(emotion_detection_results)

    def run_keyword_detection(self):
        keyword_detection = self.keyword_detection_pipeline(self.transcription)

        self.keywords = keyword_detection.ents

    def convert_analysis_result_to_array(self, data):
        formatted_data = []
        for sentence_result in data:
            if sentence_result['label'] not in formatted_data:
                formatted_data.append(sentence_result['label'])
        
        return formatted_data


    def print_audio_results(self):
        print(self.transcription_array)
        print(self.sentiment_analysis)
        print(self.emotion_detection)
        print(self.keywords)

    def start_analysis(self):
        self.transcribe_audio()
        
        #sentiment_analysis_thread = threading.Thread(target=self.run_sentiment_analysis)
        emotion_detection_thread = threading.Thread(target=self.run_emotion_detection)
        keyword_detection_thread = threading.Thread(target=self.run_keyword_detection)
        energy_detection_thread = threading.Thread(target=self.run_energy_detection)

        #sentiment_analysis_thread.start()
        emotion_detection_thread.start()
        keyword_detection_thread.start()
        energy_detection_thread.start()

        #sentiment_analysis_thread.join()
        emotion_detection_thread.join()
        keyword_detection_thread.join()
        energy_detection_thread.join()
