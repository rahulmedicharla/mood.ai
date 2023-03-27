import openai, keys
import audio_analysis, visual_analysis, ast

class Generation:
    def __init__(self, video, audio):
        self.openaikey = keys.openaikey
        self.chat_prompt = str("I will give you a bunch of lists. I want you to choose a random item from each of the lists and generate 5 unique prompts that can be used to create AI art. I want each prompt you give to follow a unique art style different from the others. The first list is a list of objects. The second list if a list of emotions. the third list is a list of colors given in RGB. ONLY for this list you should convert the RGB values to their closest color name and select three colors to use. The fourth list is a connotation. ONLY GIVE ME THE PROMPTS IN THE FORMAT ['prompt 1', 'prompt 2', 'prompt3']. Here is an example to follow. Lists: [[\"person\", \"remote\"], [\"neutral\", \"sad\", \"fear\", \"joy\"], [(20, 28, 27), (18, 26, 25), (24, 32, 31), (23, 31, 30), (22, 30, 29), (19, 27, 26), (27, 35, 34), (25, 33, 32), (26, 34, 33)], [\"POSITIVE\"] your response: [\"Create a digital portrait of a person who is feeling joyful, using a color palette inspired by the RGB values (24, 32, 31). Use bold brushstrokes and a vibrant color scheme to capture the exuberance of the subject \", \"Generate an abstract depiction of a remote object, imbued with a sense of neutral detachment. Incorporate the RGB values (22, 30, 29) into the composition to create a subtle, calming atmosphere. \", \" Produce a surrealist landscape that explores the emotion of fear, incorporating the RGB values (27, 35, 34) into the scene. Use contrasting colors and surreal imagery to evoke a sense of unease and disorientation in the viewer. \", \"Design a digital collage that expresses the emotion of sadness, using the RGB values (19, 27, 26) as a starting point. Employ mixed media techniques such as layering and texture to create a complex and nuanced work of art. \",\" Create a minimalist digital sculpture of a person using the RGB values (25, 33, 32) and a sense of positivity as inspiration. Use clean lines and simple forms to create a sense of purity and serenity in the artwork.\"]]")
        self.chat_response = ""
        self.video_analysis = video
        self.audio_analysis = audio

    def generate_chat_prompts(self):
        emotion_list = list(set(self.video_analysis.video_detected_emotions + self.audio_analysis.emotion_detection))

        openai.api_key = self.openaikey

        message = str([self.video_analysis.video_detected_objects, emotion_list, self.video_analysis.video_top_colors, self.audio_analysis.sentiment_analysis])

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
