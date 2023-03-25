import cv2
import numpy as np 
import threading

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

        #custom inits
        self.video_detected_objects = []
        self.read_classes()

    def detect_objects(self):
        cap = cv2.VideoCapture(self.video_path)

        if cap.isOpened() == False:
            print("error opening file")
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

                    cv2.rectangle(image, (x,y), (x+w, y+h), color=class_color, thickness = 1)
                    cv2.putText(image, display_text, (x,y-10), cv2.FONT_HERSHEY_PLAIN, 1, class_color, 2)

            
            for x in frame_object_list:
                if x not in self.video_detected_objects:
                    self.video_detected_objects.append(x)
            
            cv2.imshow("Result", image)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

            (success, image) = cap.read()
        cv2.destroyAllWindows()


    def read_classes(self):
        with open(self.classes_path, 'r') as f:
            self.classes_list = f.read().splitlines()
        
        self.classes_list.insert(0, "__Background__")

        self.color_list = np.random.uniform(low = 0, high = 255, size = (len(self.classes_list), 3))
    
    def print_detected_objects(self):
        print(self.video_detected_objects)

    def start_analysis(self):
        obj_detection_thread = threading.Thread(target=self.detect_objects)
        obj_detection_thread.start()
        obj_detection_thread.join()
