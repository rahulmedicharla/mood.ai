import tkinter as tk
from PIL import Image, ImageTk
from visual_input import VideoInput
from audio_input import AudioInput
import cv2


class InputParent:
    def __init__(self):

        #visual and audio recording inits
        self.video_input = VideoInput()
        self.audio_input = AudioInput()

        self.RECORDING_LENGTH = 7
        self.is_recording = False
        self.is_open = True
        self.start_time = 0

        #tkinter inits
        self.width = int(self.video_input.FRAME_WIDTH)
        self.height = int(self.video_input.FRAME_HEIGHT)

        self.root = tk.Tk()
        self.root.title("mood.ai")

        self.info_frame = tk.Frame(self.root, width=self.width)
        self.title_text = tk.Label(self.info_frame, text="Welcome to mood.ai!", font=('Helvetica', 14), pady=5)

        self.info_text = tk.Label(self.info_frame, text = "Simply click the button below to begin recording for " + str(self.RECORDING_LENGTH) + " seconds!", font=('Helvetica', 10), pady=5)

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
        self.record_button.pack_forget()
        self.start_time = cv2.getTickCount()
        self.audio_input.start_audio()

    def stop_recording(self):
        try:
            self.video_input.stop_video()
            self.audio_input.stop_audio()
            self.root.destroy()
            self.is_open = False
        except Exception as e:
            print(e)

    def update(self):
        ret, frame = self.video_input.collect_frame()
        if ret:
           
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image=Image.fromarray(image))
            self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)

            #record items being recorded
            if self.is_recording:
                #write video frame
                self.video_input.write_frame(frame)

                #collect and write audio frame

                if (cv2.getTickCount() - self.start_time)/cv2.getTickFrequency() > self.RECORDING_LENGTH:
                    self.stop_recording()

        self.root.update()
        self.root.after(0, self.update)