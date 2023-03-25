from visual_input import VideoInput
from audio_input import AudioInput
from visual_analysis import Detector
import keyboard, os

def collect_input(video, audio):
    audio.start_audio()
    video.start_video()

def terminate_input(video, audio):
    video.stop_video()
    audio.stop_audio()

def main():
    #init all objects
    video_obj = VideoInput()
    audio_obj = AudioInput()

    video_path = "video_file.mp4"
    config_path = os.path.join("model_data", "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
    model_path = os.path.join("model_data", "frozen_inference_graph.pb")
    classes_path = os.path.join("model_data", "coco.names")
    detector = Detector(video_path, config_path, model_path, classes_path)
    

    #collecting inupt
    collect_input(video_obj, audio_obj)

    while True:
        if keyboard.is_pressed('q'):
            terminate_input(video_obj, audio_obj)
            break;
    
    #running analysis
    detector.start_analysis()
    detector.printthing()


main()