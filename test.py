from transformers import pipeline
import cv2
from PIL import Image 
from sentence_transformers import SentenceTransformer, util
import torch

model = SentenceTransformer('distilbert-base-nli-mean-tokens')

image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")

cap = cv2.VideoCapture("video_file.mp4")

if cap.isOpened() == False:
    print('error opening file emotion')

(success, image) = cap.read()

res = []
similar = []
while success:
    pil_image = Image.fromarray(image)

    temp = image_to_text(pil_image)
    if temp[0]['generated_text'] not in res:
            res.append(temp[0]['generated_text'])

    key = cv2.waitKey(1)

    (success, image) = cap.read()

cv2.destroyAllWindows()

print(res)
