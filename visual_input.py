import cv2

class VideoInput:

    def __init__(self):
        self.video_capture_object = cv2.VideoCapture(0);

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_write_object = cv2.VideoWriter('video_file.mp4', fourcc, 10.0, (640, 480))

        self.FRAME_WIDTH = self.video_capture_object.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.FRAME_HEIGHT = self.video_capture_object.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    def collect_frame(self):
        ret, frame = self.video_capture_object.read()
        frame = cv2.flip(frame, 1)
        return ret,frame
    
    def write_frame(self, frame):
        return self.video_write_object.write(frame)
    
    def stop_video(self):
        self.video_capture_object.release()
        self.video_write_object.release()
        cv2.destroyAllWindows();