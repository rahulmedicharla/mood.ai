import streamlit as st
import moviepy.editor as mp
import main
import requests
from io import BytesIO

ref = main.init()

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

        image_links = main.main(openaikey, ref[0], ref[1], ref[2])
        st.text("Generating art....")
        
        for image in image_links:
            with st.container():
                st.image(image['link'])
                st.text(image['title'])
                img = BytesIO(requests.get(image['link']).content)

        generate_art = None
        


    

