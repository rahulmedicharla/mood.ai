import streamlit as st
import moviepy.editor as mp
import main
import requests
from io import BytesIO
from PIL import Image

st.title("Welcome to mood.ai")
st.header("Store memories as AI generated art")
st.subheader("Simply upload a short clip, enter your openai API key, and watch as AI turns that moment into art")

st.markdown("")
openaikey = st.text_input("Please enter your open ai key")

st.text("Use a short, max 10s mp4 video clip for best performance")
file = st.file_uploader("Upload File", type = 'mp4')
st.markdown("")

if file and openaikey:
    st.text("Analyzing text....")
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

    st.text("Generating Art....")
    image_links = main.main(openaikey)

    for image in image_links:
        with st.container():
            st.image(image['link'])
            st.text(image['title'])
            img = BytesIO(requests.get(image['link']).content)
            file_name = str(image['title']) + ".png"
            st.download_button(
                label="Download Image",
                data=img,
                file_name=file_name,
                mime='image/png',
            )


    

