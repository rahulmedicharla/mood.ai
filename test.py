from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification, pipeline

tokenizer = RobertaTokenizerFast.from_pretrained("arpanghoshal/EmoRoBERTa")
model = TFRobertaForSequenceClassification.from_pretrained("arpanghoshal/EmoRoBERTa")

emotion = pipeline('sentiment-analysis', 
                    model='arpanghoshal/EmoRoBERTa')

emotion_labels = emotion(["Thanks for giving me the time to explain why I am a good fit for this opportunity"," I feel you will be pleased with the results", "Thanks for giving me the time to explain why I am a good fit for this opportunity"])

results = []
for sentence in emotion_labels:
    if sentence['label'] not in results:
        results.append(sentence['label'])

print(results)