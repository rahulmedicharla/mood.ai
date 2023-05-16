from visual_analysis import Visual_Analysis
from audio_analysis import Audio_Analysis
from ai_generation import Generation
import os, threading

VIDEO_PATH = "video_file.mp4"
AUDIO_PATH = "audio_file.wav"
CONFIG_PATH = os.path.join("model_data", "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
MODEL_PATH = os.path.join("model_data", "frozen_inference_graph.pb")
CLASSES_PATH = os.path.join("model_data", "coco.names")

def clean_up():
    os.remove('video_file.mp4')
    os.remove('audio_file.wav')
    os.remove('movie.mp4')

def init():
    visual_analysis_obj = Visual_Analysis(VIDEO_PATH, CONFIG_PATH, MODEL_PATH, CLASSES_PATH)
    audio_analysis_obj = Audio_Analysis(AUDIO_PATH)
    ai_generation = Generation(visual_analysis_obj, audio_analysis_obj)

    return [visual_analysis_obj, audio_analysis_obj, ai_generation]

def main(openaikey):
    #init all objects
    print('Initializing objects, getting ready to run...')
    visual_analysis_obj = Visual_Analysis(VIDEO_PATH, CONFIG_PATH, MODEL_PATH, CLASSES_PATH)
    audio_analysis_obj = Audio_Analysis(AUDIO_PATH)
    ai_generation = Generation(visual_analysis_obj, audio_analysis_obj)

    print('Analyzing data...')
    
    #running analysis
    audio_analysis_thread = threading.Thread(target = audio_analysis_obj.start_analysis(openaikey))
    video_analysis_thread = threading.Thread(target = visual_analysis_obj.start_analysis())
    
    video_analysis_thread.start()
    audio_analysis_thread.start()

    audio_analysis_thread.join()
    video_analysis_thread.join()

    visual_analysis_obj.print_video_results()
    audio_analysis_obj.print_audio_results()

    #generate output
    print('Creating output...')
    ai_generation.generate_chat_prompts(openaikey)
    ai_generation.create_images()

    clean_up()

    return ai_generation.image_results
