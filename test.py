import cv2
from PIL import Image
from transformers import pipeline

image_classification = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")

cap = cv2.VideoCapture("video_file.mp4")

if cap.isOpened() == False:
    print('error opening file image classification')


list = []
for i in range(0,5):
    print('running')
    cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_FRAME_COUNT) - 1)
    success, image = cap.read()

    pil_image = Image.fromarray(image)

    classification = image_classification(pil_image)
    if classification[0]['generated_text'] not in list:
            list.append(classification[0]['generated_text'])

    key = cv2.waitKey(1)

print(list)
cv2.destroyAllWindows()
