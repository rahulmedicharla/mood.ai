from visual_analysis import Visual_Analysis
from audio_analysis import Audio_Analysis
from ai_generation import Generation
import os, threading, tempfile
import moviepy.editor as mp

CONFIG_PATH = os.path.join("model_data", "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
MODEL_PATH = os.path.join("model_data", "frozen_inference_graph.pb")
CLASSES_PATH = os.path.join("model_data", "coco.names")

def main(video_link, openaikey):
    
    #init all objects
    print('Initializing objects, getting ready to run...')
    
    #separate video and audio
    movie = mp.VideoFileClip(video_link)
    audio = movie.audio

    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        # Save the audio to the temporary file
        audio.write_audiofile(temp_file.name, codec ='pcm_s16le')


    visual_analysis_obj = Visual_Analysis(video_link, CONFIG_PATH, MODEL_PATH, CLASSES_PATH)
    audio_analysis_obj = Audio_Analysis(temp_file.name)
    ai_generation = Generation(visual_analysis_obj, audio_analysis_obj)

    print('Analyzing data...')
    
    #running analysis
    audio_analysis_thread = threading.Thread(target = audio_analysis_obj.start_analysis(openaikey))
    video_analysis_thread = threading.Thread(target = visual_analysis_obj.start_analysis())
    
    video_analysis_thread.start()
    audio_analysis_thread.start()

    audio_analysis_thread.join()
    video_analysis_thread.join()

    # visual_analysis_obj.print_video_results()
    # audio_analysis_obj.print_audio_results()

    #generate output
    print('Creating output...')
    ai_generation.generate_chat_prompts(openaikey)
    ai_generation.create_images()


    return ai_generation.image_results
