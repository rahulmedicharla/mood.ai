import cv2
import numpy as np 
import threading
from fer import FER
from transformers import pipeline
from PIL import Image
from collections import Counter
import streamlit as st
import copy
import tokenizers


class Visual_Analysis:

    def get_object_detection_model(self, model_path, config_path):
        net = cv2.dnn_DetectionModel(model_path, config_path)
        net.setInputSize(320,320)
        net.setInputScale(1.0/127.5)
        net.setInputMean((127.5,127.5,127.5))
        net.setInputSwapRB(True)
        return net
    
    @st.cache_resource
    def get_emotion_detection_model(_self):
        return FER(mtcnn=True)
    
    @st.cache_resource
    def get_image_classification_model(_self):
        return pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
    

    def __init__(self, video_path, config_path, model_path, classes_path):
        #object detection inits
        self.video_path = video_path
        self.config_path = config_path
        self.model_path = model_path
        self.classes_path = classes_path

        #data inits
        self.video_detected_objects = []
        self.video_detected_emotions = []
        self.video_classification = []
        self.video_top_colors = []

        self.read_classes()

    
    def detect_objects(self):
        model = self.get_object_detection_model(self.model_path, self.config_path)

        #uncomment to see analysis
        cap = cv2.VideoCapture(self.video_path)

        if cap.isOpened() == False:
            print("error opening file object detection")
            return
        
        (success, image) = cap.read()

        detected_objects = []

        while success:
            class_label_ids, confidence, bboxs = model.detect(image, confThreshold = 0.5)

            bboxs = list(bboxs)
            confidence = list(np.array(confidence).reshape(1,-1)[0])
            confidence = list(map(float, confidence))

            bbox_idx = cv2.dnn.NMSBoxes(bboxs, confidence, score_threshold = 0.5, nms_threshold = 0.2)

            frame_object_list = []

            if len(bbox_idx) != 0:
                for i in range(0, len(bbox_idx)):

                    bbox = bboxs[np.squeeze(bbox_idx[i])]
                    class_label_id = np.squeeze(class_label_ids[np.squeeze(bbox_idx[i])])
                    class_label = self.classes_list[class_label_id]
                    
                    if (class_label not in frame_object_list):
                        frame_object_list.append(class_label)

                    x,y,w,h = bbox
            
            for x in frame_object_list:
                detected_objects.append(x)
            
            
            key = cv2.waitKey(1)

            (success, image) = cap.read()
        cv2.destroyAllWindows()

        most_common_objects = Counter(detected_objects).most_common(3)
        for object in most_common_objects:
            self.video_detected_objects.append(object[0])
    
    def detect_emotions(self, model):
        cap = cv2.VideoCapture(self.video_path)

        if cap.isOpened() == False:
            print('error opening file emotion')
        
        (success, image) = cap.read()

        emotions_detected = []

        while success:
            dominant_emotion, emotion_score = model.top_emotion(image)

            emotions_detected.append(dominant_emotion)

            key = cv2.waitKey(1)

            (success, image) = cap.read()
        cv2.destroyAllWindows()

        most_common_emotions = Counter(emotions_detected).most_common(2)
        for emotion in most_common_emotions:
            self.video_detected_emotions.append(emotion[0])
        
    def classify_video(self, model):
        cap = cv2.VideoCapture(self.video_path)

        if cap.isOpened() == False:
            print('error opening file image classification')
        
        for i in range(0,5):
            cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_FRAME_COUNT) - 1)
            success, image = cap.read()
        
            pil_image = Image.fromarray(image)

            classification = model(pil_image)
            if classification[0]['generated_text'] not in self.video_classification:
                    self.video_classification.append(classification[0]['generated_text'])

            key = cv2.waitKey(1)

        cv2.destroyAllWindows()
    
    def detect_colors(self):
        cap = cv2.VideoCapture(self.video_path)

        if cap.isOpened() == False:
            print('error opening file color detection')

        (success, image) = cap.read()

        while success:
            pil_image = Image.fromarray(image)

            res = pil_image.getcolors(pil_image.size[0] * pil_image.size[1])

            sorted_colors = sorted(res, key = lambda x:x[0], reverse=True)

            top_colors = sorted_colors[:2]

            rgb_colors = [c[1] for c in top_colors]

            if rgb_colors[0] not in self.video_top_colors:
                self.video_top_colors.append(rgb_colors[0])
            if rgb_colors[1] not in self.video_top_colors:
                self.video_top_colors.append(rgb_colors[1])

            key = cv2.waitKey(1)

            (success, image) = cap.read()
        cv2.destroyAllWindows()


    
    def read_classes(self):
        with open(self.classes_path, 'r') as f:
            self.classes_list = f.read().splitlines()
        
        self.classes_list.insert(0, "__Background__")

        self.color_list = np.random.uniform(low = 0, high = 255, size = (len(self.classes_list), 3))
    
    def print_video_results(self):
        f = open('detection_results.txt', 'a')

        f.write("\nObjects Detected: " + str(self.video_detected_objects))
        f.write("\nEmotions detected:" + str(self.video_detected_emotions))
        f.write("\nClassification: " + str(self.video_classification))
        f.write("\nTop Colors: " + str(self.video_top_colors))

        f.close()

    def start_analysis(self):
        try:
            print("analysis is being run")
            obj_detection_thread = threading.Thread(target=self.detect_objects)
            emotion_detection_thread = threading.Thread(target=self.detect_emotions, args=(copy.deepcopy(self.get_emotion_detection_model()),))
            image_classification_thread = threading.Thread(target=self.classify_video, args=(copy.deepcopy(self.get_image_classification_model()),))
            color_detection_thread = threading.Thread(target=self.detect_colors)
            
            obj_detection_thread.start()
            emotion_detection_thread.start()
            image_classification_thread.start()
            color_detection_thread.start()

            obj_detection_thread.join()
            emotion_detection_thread.join()
            image_classification_thread.join()
            color_detection_thread.join()
        except Exception as e:
            print("Video Exception: " + e)

