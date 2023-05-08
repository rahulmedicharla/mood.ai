from input_parent import InputParent
from visual_analysis import Visual_Analysis
from audio_analysis import Audio_Analysis
from ai_generation import Generation
from generate_webpage import WebBrowser
import os, threading

VIDEO_PATH = "video_file.mp4"
AUDIO_PATH = "audio_file.wav"
CONFIG_PATH = os.path.join("model_data", "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
MODEL_PATH = os.path.join("model_data", "frozen_inference_graph.pb")
CLASSES_PATH = os.path.join("model_data", "coco.names")

def clean_up():
    os.remove('video_file.mp4')
    os.remove('audio_file.wav')

def main():
    #init all objects
    print('Initializing objects, getting ready to run...')
    visual_analysis_obj = Visual_Analysis(VIDEO_PATH, CONFIG_PATH, MODEL_PATH, CLASSES_PATH)
    audio_analysis_obj = Audio_Analysis(AUDIO_PATH)
    ai_generation = Generation(visual_analysis_obj, audio_analysis_obj)
    
    #collecting inupt
    input_parent = InputParent()

    print('Analyzing data...')
    
    #running analysis
    audio_analysis_thread = threading.Thread(target = audio_analysis_obj.start_analysis(input_parent.openai_api_key))
    video_analysis_thread = threading.Thread(target = visual_analysis_obj.start_analysis())
    
    video_analysis_thread.start()
    audio_analysis_thread.start()

    audio_analysis_thread.join()
    video_analysis_thread.join()

    visual_analysis_obj.print_video_results()
    audio_analysis_obj.print_audio_results()

    #generate output
    print('Creating output...')
    ai_generation.generate_chat_prompts(input_parent.openai_api_key)
    ai_generation.create_images()

    #create webpage
    web_browser = WebBrowser(ai_generation)
    web_browser.create_webpage()

    clean_up()


main()