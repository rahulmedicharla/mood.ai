import openai, keys
import audio_analysis, visual_analysis, ast

class Generation:
    def __init__(self, video, audio):
        self.openaikey = keys.openaikey
        self.chat_prompt = str("I will give you a bunch of lists. I want you to choose a random item from each of the lists and generate 5 unique prompts that can be used to create AI art. I want each prompt you give to follow a unique art style different from the others. The first list is a list of captions describing the video. You can choose not to use a value from the first list for a couple of the images. The second list is a list of objects. The third list if a list of emotions. the fourth list is a list of colors given in RGB. ONLY for this list you should convert the RGB values to their closest color name and select three colors to use. The fourth list is a connotation. I would like atleast one prompt to emphaize emotions through color, and at least one be abstract. ONLY GIVE ME THE PROMPTS IN THE FORMAT ['prompt 1', 'prompt 2', 'prompt3']. Follow this example: Lists: [[\"a man holding a cell phone in his hand \"], [\"person\", \"remote\"], [\"neutral\", \"sad\", \"fear\", \"joy\"], [(20, 28, 27), (18, 26, 25), (24, 32, 31), (23, 31, 30), (22, 30, 29), (19, 27, 26), (27, 35, 34), (25, 33, 32), (26, 34, 33)], [\"POSITIVE\"]  Your response : \"[\"A solitary person holding a remote control with a neutral expression in a dimly lit room. Create an art piece that embodies the feeling of emptiness and monotony, using shades of grey and a pop of color in RGB values (19, 27, 26). Using a pointillism art style, create a portrait of a person holding a remote control that captures the emotion of neutrality and detachment.\" , \"A man holding a cell phone with a look of fear on his face as he stands in front of a bright red background. \"Create a digital painting using RGB values (255, 0, 0) that conveys the intense emotion of fear and panic. Using a surrealist art style, create a portrait of a person with a cell phone that portrays the feeling of being trapped and helpless \", \"A person holding a remote control with a joyful expression, standing in a field of vibrant flowers. Create an art piece that showcases the emotion of happiness using bright and bold colors like RGB values (255, 215, 0) and (144, 238, 144). Using a cubism art style, create a portrait of a person holding a remote control that captures the emotion of joy and playfulness. \", \"A person holding a remote control with a sad expression in front of a moody sky with RGB values (23, 31, 30). Create a digital painting using a muted color palette that conveys the emotion of sadness and melancholy. Using a realism art style, create a portrait of a person holding a remote control that evokes feelings of loneliness and isolation. \" , \"A person holding a remote control with a positive connotation standing in front of a warm, orange backdrop with RGB values (255, 165, 0). Create an art piece that exudes positivity and optimism, using shades of orange and yellow. Using a pop art style, create a portrait of a person holding a remote control that portrays a sense of energy and excitement.\"]")
        self.chat_response = ""
        self.video_analysis = video
        self.audio_analysis = audio

    def generate_chat_prompts(self):
        emotion_list = list(set(self.video_analysis.video_detected_emotions + self.audio_analysis.emotion_detection))

        openai.api_key = self.openaikey

        message = str([self.video_analysis.video_classification,self.video_analysis.video_detected_objects, emotion_list, self.video_analysis.video_top_colors, self.audio_analysis.sentiment_analysis])

        completion = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [
                {"role" : "system", "content": self.chat_prompt},
                {"role" : "user", "content": message}
            ]
        )

        self.chat_response = completion.choices[0].message.content
    
    def generate_images(self):
        prompts = ast.literal_eval(self.chat_response)
        print(prompts)

        openai.api_key = self.openaikey

        f = open("output.txt", 'a')
        for prompt in prompts:
            image = openai.Image.create(
                prompt = prompt,
                n=1,
                size = "256x256"
            )
            f.write(image["data"][0]["url"] + "\n")

        f.close()
