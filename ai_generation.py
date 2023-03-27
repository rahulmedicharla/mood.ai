import openai, keys
import audio_analysis, visual_analysis, ast

class Generation:
    def __init__(self, video, audio):
        self.openaikey = keys.openaikey
        self.chat_prompt = str("I will give you a bunch of lists. I want you to choose a random item from each of the lists and generate 5 unique prompts that can be used to create AI art. I want each prompt you give to follow a unique art style different from the others. The first list is a list of captions describing the video. You can choose not to use a value from the first list for a couple of the images. The second list is a list of objects. The third list if a list of emotions. the fourth list is a list of colors given in RGB. ONLY for this list you should convert the RGB values to their closest color name and select three colors to use. The fourth list is a connotation, and the fith list is a list of keywords. I would like atleast one prompt to emphaize emotions through color, and at least one be abstract. ONLY GIVE ME THE PROMPTS IN THE FORMAT ['prompt 1', 'prompt 2', 'prompt3']. Follow this example below: [['a man laying on a couch with a cat on his lap '], ['chair', 'couch', 'person', 'remote', 'bottle', 'tv', 'refrigerator', 'bed'], ['sad', 'admiration', 'anger', 'neutral'], [(167, 184, 182), (145, 172, 173), (147, 173, 171), (142, 168, 166), (136, 162, 165), (141, 161, 158), (147, 159, 158), (145, 160, 158), (138, 150, 149)], ['POSITIVE'], (today, Brad)] your response: \"[\"Create an abstract art piece with a color palette of (128, 138, 137), (156, 161, 161), and (161, 166, 166). Use fluid shapes and lines to represent the man and the couch, and let the colors bleed into each other.\", \"Create a digital art piece using pixel art with a color palette of (187, 199, 204), (190, 201, 202), and (189, 200, 201). Use the pixel art to depict the person sleeping, and incorporate the remote control into the piece in a way that feels organic and natural.\", \"Create an impressionist painting with a color palette of (143, 160, 158), (145, 160, 158), and (141, 161, 158). Use loose brushstrokes to create the man and the cat, and focus on capturing the emotion in their faces and body language.\", \"Create a vector art piece with a color palette of (147, 159, 158), (138, 164, 162), and (142, 150, 149). Use the vector art to depict the person sitting in the chair, and incorporate the refrigerator in the background in a way that feels geometric and precise.\", \"Create a digital art piece using glitch art with a color palette of (106, 118, 130), (143, 155, 154), and (154, 165, 173). Use the glitch art to create an abstract representation of the person on the couch, and incorporate the bottle in a way that feels fragmented and disjointed. Emphasize the emotion of admiration through the use of color.\"]\"")
        self.chat_response = ""
        self.video_analysis = video
        self.audio_analysis = audio

    def generate_chat_prompts(self):
        emotion_list = list(set(self.video_analysis.video_detected_emotions + self.audio_analysis.emotion_detection))

        openai.api_key = self.openaikey

        message = str([self.video_analysis.video_classification,self.video_analysis.video_detected_objects, emotion_list, self.video_analysis.video_top_colors, self.audio_analysis.sentiment_analysis, self.audio_analysis.keywords])

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
