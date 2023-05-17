import requests
from keys import openaikey
import urllib.parse

BASE = "http://127.0.0.1:5000/"

url = "https%3A%2F%2Ffirebasestorage.googleapis.com%2Fv0%2Fb%2Fmood-ai-34418.appspot.com%2Fo%2Frecordings%252FZ94e4nOz89NXtVAL8YwaWTK2Edl1.mp4%3Falt%3Dmedia%26token%3D0dbd2a89-552e-48c4-bd34-dc0d9c4136be"

final = BASE + 'moodai/' + url +  '/' + openaikey
response = requests.get(final)

print(response.json())