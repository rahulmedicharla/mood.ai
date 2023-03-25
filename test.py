from visual_analysis import Detector
import os

def main():
    video_path = "video_file.mp4"
    config_path = os.path.join("model_data", "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
    model_path = os.path.join("model_data", "frozen_inference_graph.pb")
    classes_path = os.path.join("model_data", "coco.names")

    detector = Detector(video_path, config_path, model_path, classes_path)
    detector.onVideo()


main()