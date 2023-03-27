from transformers import pipeline
import cv2
from PIL import Image 
from sentence_transformers import SentenceTransformer, util

image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")

