from visual_input import VideoInput
from audio_input import AudioInput
import keyboard

def collect_input(video, audio):
    audio.start_audio()
    video.start_video()

def terminate_input(video, audio):
    video.stop_video()
    audio.stop_audio()

def main():
    video_obj = VideoInput()
    audio_obj = AudioInput()

    collect_input(video_obj, audio_obj)

    while True:
        if keyboard.is_pressed('q'):
            terminate_input(video_obj, audio_obj)
            break;


main()