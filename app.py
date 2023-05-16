import streamlit as st
import moviepy.editor as mp
import main
import requests
from io import BytesIO
import os
from visual_analysis import Visual_Analysis
from audio_analysis import Audio_Analysis
from ai_generation import Generation

VIDEO_PATH = "video_file.mp4"
AUDIO_PATH = "audio_file.wav"
CONFIG_PATH = os.path.join("model_data", "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
MODEL_PATH = os.path.join("model_data", "frozen_inference_graph.pb")
CLASSES_PATH = os.path.join("model_data", "coco.names")

visual_analysis_obj = Visual_Analysis(VIDEO_PATH, CONFIG_PATH, MODEL_PATH, CLASSES_PATH)
audio_analysis_obj = Audio_Analysis(AUDIO_PATH)
ai_generation = Generation(visual_analysis_obj, audio_analysis_obj)

st.title("Welcome to mood.ai")
st.header("Store memories as AI generated art")
st.subheader("Simply upload a short clip, enter your openai API key, and watch as AI turns that moment into art")

st.markdown("")
openaikey = st.text_input("Please enter your open ai key")

st.text("Use a short, max 10s mp4 video clip for best performance")
file = st.file_uploader("Upload File", type = 'mp4')
st.markdown("")

generate_art = st.button("Generate Art!")
st_image_container = st.empty()

if file and openaikey:
    if generate_art:
        st.text("Analyzing video....")
        with open("movie.mp4", "wb") as f:
            f.write(file.getvalue())

        # Load the MP4 file
        video = mp.VideoFileClip("movie.mp4")

        # Separate audio and video streams
        audio = video.audio
        video = video.without_audio()

        # Save audio and video files
        audio_filename = "audio_file.wav"
        video_filename = "video_file.mp4"

        audio.write_audiofile(audio_filename)
        video.write_videofile(video_filename)

        image_links = main.main(openaikey, visual_analysis_obj, audio_analysis_obj, ai_generation)
        st.text("Generating art....")
        
        for image in image_links:
            with st.container():
                st.image(image['link'])
                st.text(image['title'])
                img = BytesIO(requests.get(image['link']).content)

        generate_art = None
        


    

