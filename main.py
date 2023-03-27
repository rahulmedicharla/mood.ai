from visual_input import VideoInput
from audio_input import AudioInput
from visual_analysis import Visual_Analysis
from audio_analysis import Audio_Analysis
from ai_generation import Generation
import keyboard, os, threading

VIDEO_PATH = "video_file.mp4"
AUDIO_PATH = "audio_file.wav"
CONFIG_PATH = os.path.join("model_data", "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
MODEL_PATH = os.path.join("model_data", "frozen_inference_graph.pb")
CLASSES_PATH = os.path.join("model_data", "coco.names")
    

def collect_input(video, audio):
    audio.start_audio()
    video.start_video()

def terminate_input(video, audio):
    video.stop_video()
    audio.stop_audio()

def main():
    #init all objects
    print('Initializing objects, getting ready to run...')
    video_obj = VideoInput()
    audio_obj = AudioInput()
    visual_analysis_obj = Visual_Analysis(VIDEO_PATH, CONFIG_PATH, MODEL_PATH, CLASSES_PATH)
    audio_analysis_obj = Audio_Analysis(AUDIO_PATH)
    ai_generation = Generation(visual_analysis_obj, audio_analysis_obj)
    
    #collecting inupt
    collect_input(video_obj, audio_obj)

    while True:
        if keyboard.is_pressed('q'):
            terminate_input(video_obj, audio_obj)
            break;
    
    print('Analyzing data...')
    
    #running analysis
    audio_analysis_thread = threading.Thread(target = audio_analysis_obj.start_analysis())
    video_analysis_thread = threading.Thread(target = visual_analysis_obj.start_analysis())
    
    video_analysis_thread.start()
    audio_analysis_thread.start()

    audio_analysis_thread.join()
    video_analysis_thread.join()

    visual_analysis_obj.print_video_results()
    audio_analysis_obj.print_audio_results()

    #generate output
    print('Creating output...')
    ai_generation.generate_chat_prompts()
    ai_generation.generate_images()



main()