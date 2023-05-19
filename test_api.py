import requests

BASE = "http://127.0.0.1:5000/"

openaikey = "ENTER_OPENAI_KEY"
url = "ENTER_VIDEO_URL"

final = BASE + 'moodai/' + url +  '/' + openaikey
response = requests.get(final)

print(response.json())
