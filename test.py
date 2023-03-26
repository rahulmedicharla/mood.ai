import cv2
from fer import FER, Video

emotion_detector = FER(mtcnn = True)


cap = cv2.VideoCapture('video_file.mp4')

if cap.isOpened() == False:
    print("error opening file")
    

emotion_list = []


(success, image) = cap.read()

while success:
    dominant_emotion, emotion_score = emotion_detector.top_emotion(image)

    if dominant_emotion not in emotion_list:
        emotion_list.append(dominant_emotion)

    key = cv2.waitKey(1)

    (success, image) = cap.read()
cv2.destroyAllWindows()

print(emotion_list)