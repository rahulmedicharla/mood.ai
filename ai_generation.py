import openai, keys
import audio_analysis, visual_analysis, ast

class Generation:
    def __init__(self, video, audio):
        self.openaikey = keys.openaikey
        self.chat_prompt = """I will give you a bunch of lists. I want you to choose a random item from each of the lists and generate 5 unique prompts that can be used to create AI art. I want each prompt you give to follow a unique art style different from the others. The first list is a list of captions describing the video. You can choose not to use a value from the first list for a couple of the images. The second list is a list of objects. The third list if a list of emotions. the fourth list is a list of colors given in RGB. ONLY for this list you should convert the RGB values to their closest color name and select three colors to use. The fourth list is a connotation, and the fifth list is a list of keywords. I would like atleast one prompt to emphasize emotions through color, and at least one be abstract. Use random weights to determine how important a piece of information is for the prompt. For some of the prompts follow art styles from famous artists. ONLY GIVE ME THE YOUR RESPONSE IN THE FORMAT ["prompt 1", "prompt 2", "prompt3"]. 

                            Follow these example below:
                            [['a man laying on a couch looking at his phone'], ['chair', 'couch', 'person', 'cellphone', 'bottle', 'tv'], ['happy', 'admiration', 'gratitude', 'neutral'], [(167, 184, 182), (145, 172, 173), (147, 173, 171), (142, 168, 166), (136, 162, 165), (141, 161, 158), (147, 159, 158), (145, 160, 158), (138, 150, 149)], ['POSITIVE'], (basketball)] 
                            your response: "["Create an abstract digital art piece that incorporates bright, cheerful colors such as (167, 184, 182) and (145, 172, 173) to depict a man lounging on a couch, staring intently at his cellphone screen with a grin on his face. Use geometric shapes and patterns to add depth and complexity to the piece ", "Create a realistic oil painting that features a bottle of an indeterminate liquid resting on the arm of a well-worn couch. The couch is surrounded by muted, earthy tones like (142, 168, 166) and (147, 173, 171), while the bottle is a pop of bright color such as (141, 161, 158). The piece should emphasize the neutral emotion ", "Create a digital art piece that mimics the look of a distorted reflection in a television screen. Use a cool color palette such as (145, 160, 158) and (138, 150, 149) to create a moody, contemplative atmosphere. Incorporate a person sitting in a nearby chair, gazing intently at the TV screen with an expression of admiration on their face ", "Create a playful digital art piece that looks like it was drawn in marker or crayon. Use a bright, energetic color palette such as (147, 159, 158) and (136, 162, 165) to depict a person hunched over their cellphone, absorbed in the digital world. The piece should emphasize the happy emotion ", "Create an abstract mixed media art piece that combines elements of painting, photography, and digital manipulation. The piece should feature a basketball being passed from one person to another, with an emphasis on the emotion of gratitude. Use a warm color palette such as (167, 184, 182) and (141, 161, 158) to create a sense of warmth and connection between the players "]"

                            [['a room with a television, a desk, and a chair '], ['person', 'dog', 'tv', 'book', 'chair', 'remote', 'couch', 'bed'], ['neutral', 'sad', 'angry', 'fear', 'disapproval', 'admiration'], [(229, 232, 230), (240, 198, 165), (239, 197, 164), (231, 233, 226), (231, 178, 146), (226, 231, 231), (228, 231, 229), (236, 238, 231), (229, 237, 236), (185, 169, 154), (234, 237, 235), (34, 37, 27), (38, 41, 31), (236, 237, 232), (210, 139, 99), (35, 31, 27), (31, 26, 27), (30, 25, 26), (29, 25, 28), (33, 27, 30), (31, 26, 32), (35, 26, 30), (232, 238, 233), (17, 25, 24), (182, 129, 143), (181, 129, 140), (181, 128, 137)], ['NEGATIVE', 'POSITIVE'], (today)]
                            your response: "["Create an abstract digital art piece that uses bold, contrasting colors such as RGB (229, 232, 230) and RGB (34, 37, 27) to depict a person sitting in a chair with a remote control in their hand. The piece should convey a sense of disapproval through the use of sharp, angular shapes and lines. ", "Create a mixed media art piece that combines painting and photography to depict a room with a bed and a dog lying on it. Use warm colors such as RGB (239, 197, 164) and RGB (236, 237, 232) to create a cozy, inviting atmosphere. The piece should emphasize the emotion of admiration.", "Create an oil painting that features a desk cluttered with books and papers. Use a monochromatic color scheme such as RGB (30, 25, 26) to create a somber, serious mood. The piece should convey the emotion of sadness.", "Create an classic painting that incorporates earthy tones such as RGB (185, 169, 154) and RGB (182, 129, 143) to depict a room with a couch and a person sitting on it. The piece should convey a sense of anger through the use of bold, expressive brushstrokes.", "Create a pop art piece that features a television with distorted imagery. Use a cool color palette such as (17, 25, 24) to create an eerie, unsettling atmosphere. The piece should emphasize the emotion of fear."]"
                        """
        
        self.chat_response = ""
        self.video_analysis = video
        self.audio_analysis = audio
        self.dalle_prompts = []
        self.image_links = []

    def generate_chat_prompts(self):
        emotion_list = list(set(self.video_analysis.video_detected_emotions + self.audio_analysis.emotion_detection))
        if 'sad' in emotion_list:
            emotion_list.remove('sad')

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
        self.dalle_prompts = ast.literal_eval(self.chat_response)

        openai.api_key = self.openaikey

        for prompt in self.dalle_prompts:
            image = openai.Image.create(
                prompt = prompt,
                n=1,
                size = "256x256"
            )
            self.image_links.append(image["data"][0]["url"])
            
