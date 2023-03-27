import openai
import threading, keys
from transformers import pipeline


class Audio_Analysis:

    def __init__(self, audio_path):
        #model inits
        self.sentiment_analysis_pipeline = pipeline('sentiment-analysis', model = 'distilbert-base-uncased-finetuned-sst-2-english')
        self.emotion_detection_pipeline = pipeline('sentiment-analysis', model='arpanghoshal/EmoRoBERTa')

        #whisper inits
        self.openaikey = keys.openaikey

        #data inits
        self.audio_path = audio_path
        self.transcription = []
        self.sentiment_analysis = []
        self.emotion_detection = []
    
    def transcribe_audio(self):
        openai.api_key = self.openaikey
        audio_file = open(self.audio_path, "rb")
        transcription = openai.Audio.transcribe("whisper-1", audio_file)
        self.transcription = transcription["text"].split('.')
    
    def run_sentiment_analysis(self):
        sentiment_analysis_results = self.sentiment_analysis_pipeline(self.transcription)

        self.sentiment_analysis = self.convert_analysis_result_to_array(sentiment_analysis_results)

    def run_emotion_detection(self):
        emotion_detection_results = self.emotion_detection_pipeline(self.transcription)

        self.emotion_detection = self.convert_analysis_result_to_array(emotion_detection_results)
    
    def convert_analysis_result_to_array(self, data):
        formatted_data = []
        for sentence_result in data:
            if sentence_result['label'] not in formatted_data:
                formatted_data.append(sentence_result['label'])
        
        return formatted_data


    def print_audio_results(self):
        print(self.transcription)
        print(self.sentiment_analysis)
        print(self.emotion_detection)

    def start_analysis(self):
        self.transcribe_audio()
        
        sentiment_analysis_thread = threading.Thread(target=self.run_sentiment_analysis)
        emotion_detection_thread = threading.Thread(target=self.run_emotion_detection)

        sentiment_analysis_thread.start()
        emotion_detection_thread.start()

        sentiment_analysis_thread.join()
        emotion_detection_thread.join()
