import cv2
import numpy as np 
import threading
from fer import FER
from transformers import pipeline
from PIL import Image


np.random.seed(20)
class Visual_Analysis:
    def __init__(self, video_path, config_path, model_path, classes_path):
        #object detection inits
        self.video_path = video_path
        self.config_path = config_path
        self.model_path = model_path
        self.classes_path = classes_path

        self.net = cv2.dnn_DetectionModel(self.model_path, self.config_path)
        self.net.setInputSize(320,320)
        self.net.setInputScale(1.0/127.5)
        self.net.setInputMean((127.5,127.5,127.5))
        self.net.setInputSwapRB(True)

        #emotion detection inits
        self.emotion_detector = FER(mtcnn = True)

        #image classification inits
        self.image_classification = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")

        #data inits
        self.video_detected_objects = []
        self.video_detected_emotions = []
        self.video_classification = []
        self.video_top_colors = []

        self.read_classes()

    def detect_objects(self):
        #uncomment to see analysis
        cap = cv2.VideoCapture(self.video_path)

        if cap.isOpened() == False:
            print("error opening file object detection")
            return
        
        (success, image) = cap.read()

        while success:
            class_label_ids, confidence, bboxs = self.net.detect(image, confThreshold = 0.5)

            bboxs = list(bboxs)
            confidence = list(np.array(confidence).reshape(1,-1)[0])
            confidence = list(map(float, confidence))

            bbox_idx = cv2.dnn.NMSBoxes(bboxs, confidence, score_threshold = 0.5, nms_threshold = 0.2)

            frame_object_list = []

            if len(bbox_idx) != 0:
                for i in range(0, len(bbox_idx)):

                    bbox = bboxs[np.squeeze(bbox_idx[i])]
                    class_confidence = confidence[np.squeeze(bbox_idx[i])]
                    class_label_id = np.squeeze(class_label_ids[np.squeeze(bbox_idx[i])])
                    class_label = self.classes_list[class_label_id]
                    class_color = [int(c) for c in self.color_list[class_label_id]]

                    display_text = "{}:{:.2f}".format(class_label, class_confidence)

                    if (class_label not in frame_object_list):
                        frame_object_list.append(class_label)

                    x,y,w,h = bbox

                    #cv2.rectangle(image, (x,y), (x+w, y+h), color=class_color, thickness = 1)
                    #cv2.putText(image, display_text, (x,y-10), cv2.FONT_HERSHEY_PLAIN, 1, class_color, 2)

            
            for x in frame_object_list:
                if x not in self.video_detected_objects:
                    self.video_detected_objects.append(x)
            
            #cv2.imshow("Result", image)
            
            key = cv2.waitKey(1)

            (success, image) = cap.read()
        cv2.destroyAllWindows()
    
    def detect_emotions(self):
        cap = cv2.VideoCapture(self.video_path)

        if cap.isOpened() == False:
            print('error opening file emotion')
        
        (success, image) = cap.read()

        while success:
            dominant_emotion, emotion_score = self.emotion_detector.top_emotion(image)

            if dominant_emotion not in self.video_detected_emotions and dominant_emotion != None:
                self.video_detected_emotions.append(dominant_emotion)

            key = cv2.waitKey(1)

            (success, image) = cap.read()
        cv2.destroyAllWindows()

    def classify_video(self):
        cap = cv2.VideoCapture(self.video_path)

        if cap.isOpened() == False:
            print('error opening file image classification')

        
        for i in range(0,5):
            cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_FRAME_COUNT) - 1)
            success, image = cap.read()
        
            pil_image = Image.fromarray(image)

            classification = self.image_classification(pil_image)
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

            top_colors = sorted_colors[:3]

            rgb_colors = [c[1] for c in top_colors]

            if rgb_colors[0] not in self.video_top_colors:
                self.video_top_colors.append(rgb_colors[0])
            if rgb_colors[1] not in self.video_top_colors:
                self.video_top_colors.append(rgb_colors[1])
            if rgb_colors[2] not in self.video_top_colors:
                self.video_top_colors.append(rgb_colors[2])

            key = cv2.waitKey(1)

            (success, image) = cap.read()
        cv2.destroyAllWindows()


    
    def read_classes(self):
        with open(self.classes_path, 'r') as f:
            self.classes_list = f.read().splitlines()
        
        self.classes_list.insert(0, "__Background__")

        self.color_list = np.random.uniform(low = 0, high = 255, size = (len(self.classes_list), 3))
    
    def print_video_results(self):
        print("Objects Detected: " + str(self.video_detected_objects))
        print("Emotions detected:" + str(self.video_detected_emotions))
        print("Classification: " + str(self.video_classification))
        print("Top Colors: " + str(self.video_top_colors))

    def start_analysis(self):
        try:
            obj_detection_thread = threading.Thread(target=self.detect_objects)
            emotion_detection_thread = threading.Thread(target=self.detect_emotions)
            image_classification_thread = threading.Thread(target=self.classify_video)
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
            print("Exception: " + e)

