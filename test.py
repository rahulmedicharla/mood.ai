import tkinter as tk
import cv2
from PIL import Image, ImageTk

class CameraApp:
    def __init__(self, video_source=0):

        self.cap = cv2.VideoCapture(video_source)
        if not self.cap.isOpened():
            raise ValueError("Unable to open camera")

        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.is_recording = False
        self.start_time = 0

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_write_object = cv2.VideoWriter('video_file.mp4', fourcc, 10.0, (640, 480))

        self.root = tk.Tk()
        self.root.title("mood.ai")

        self.info_frame = tk.Frame(self.root, width=self.width)
        self.title_text = tk.Label(self.info_frame, text="Welcome to mood.ai!", font=('Helvetica', 14), pady=5)

        self.info_text = tk.Label(self.info_frame, text = "Simply click the button below to begin recording for 5 seconds!", font=('Helvetica', 10), pady=5)

        self.record_button = tk.Button(self.info_frame, text="Start Recording!", command=self.toggle_recording, font=('Helvetica', 10), pady = 5)
        
        self.title_text.pack()
        self.info_text.pack()
        self.record_button.pack()
        self.info_frame.pack()

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()

        self.update()

        self.root.mainloop()

    def toggle_recording(self):
        self.is_recording = True
        self.start_time = cv2.getTickCount()

    def stop_recording(self):
        self.is_recording = False;
        if self.cap.isOpened():
            self.cap.release()
        self.video_write_object.release()
        cv2.destroyAllWindows()
        self.root.quit()


    def update(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
           
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image=Image.fromarray(image))
            self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)

            if self.is_recording: 
                self.video_write_object.write(frame)

                if (cv2.getTickCount() - self.start_time)/cv2.getTickFrequency() > 5:
                    self.stop_recording()

        self.root.update()
        self.root.after(0, self.update)


app = CameraApp()
