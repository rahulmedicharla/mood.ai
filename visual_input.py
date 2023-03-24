import cv2, threading

class VideoInput:

    def __init__(self):
        self.video_capture_object = cv2.VideoCapture(0);

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_write_object = cv2.VideoWriter('video_file.mp4', fourcc, 10.0, (640, 480))
        
        self.open = True
    
    def collect_video(self):
        while(self.open == True):
            ret, frame = self.video_capture_object.read()
            if ret:
                frame = cv2.flip(frame, 1)
                cv2.imshow('frame', frame)
                self.video_write_object.write(frame)
                cv2.waitKey(1)        

    def stop_video(self):
        if self.open:
            self.open = False
            self.video_capture_object.release()
            self.video_write_object.release()
            cv2.destroyAllWindows();

    def start_video(self):
        video_thread = threading.Thread(target=self.collect_video)
        video_thread.start()