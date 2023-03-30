import openai, keys, ast, threading
from queue import Queue

class Generation:
    def __init__(self, video, audio):
        self.openaikey = keys.openaikey
        self.chat_prompt = """I will give you a bunch of lists. I want you to choose a random item from each of the lists and generate 5 unique prompts that can be used to create AI art. I want each prompt you give to follow a unique and fancy art style different from the others. The first list is a list of captions describing the video. Only use this value in TWO of the prompts generated. The second list is a list of objects. The third list if a list of emotions. the fourth list is a list of colors given in RGB. ONLY for this list you should convert the RGB values to their closest color name and select three colors to use. The fourth list is a connotation, and the fifth list is a list of keywords. I would like atleast one prompt to emphasize emotions through color, and at least one be abstract. Use random weights to determine how important a piece of information is for the prompt. Generate titles for each image as well. For some of the prompts follow art styles from famous artists. ONLY GIVE ME THE YOUR RESPONSE IN THE FORMAT ["title 1", "prompt 1", "title 2", "prompt 2", "titile 3", "prompt3"]. 

                            Follow these examples below:
                            [['a man laying on a couch looking at his phone'], ['chair', 'couch', 'person', 'cellphone', 'bottle', 'tv'], ['happy', 'admiration', 'gratitude', 'neutral'], [(167, 184, 182), (145, 172, 173), (147, 173, 171), (142, 168, 166), (136, 162, 165), (141, 161, 158), (147, 159, 158), (145, 160, 158), (138, 150, 149)], ['POSITIVE'], (basketball)]
                            your response: ["Connected in Isolation", "Create an realistic Baroque painting using the colors (141, 161, 158) and (145, 172, 173) to convey a feeling of gratitude. The painting should depict a person on a couch, lost in their cellphone, and a TV in the background, with the emphasis on the glowing screen. The style should be inspired by the works of Caraviaggio", "The Blue Serenity", "Create a realistic oil painting of a person sitting on a chair, holding a bottle and looking at their cellphone. Use the colors (145, 160, 158) and (167, 184, 182) to convey a neutral emotion. The background should be blurry, with emphasis on the person and the bottle, and the style should be inspired by the works of Edward Hopper.", "The Joy of Life", "Create a vibrant Bauhaus style painting using the colors (147, 173, 171) and (142, 168, 166) to convey a feeling of happiness. The painting should depict a person sitting on a couch, holding a cellphone, with a TV in the background. The focus should be on the person's expression, conveying a sense of contentment and joy. The style should be inspired by the works of Paul Klee.", "Grateful Reflections", "Create a pop art drawing using the colors (136, 162, 165) and (147, 159, 158) to convey a feeling of gratitude. The painting should depict a person on a couch, holding a bottle, with a TV in the background. The focus should be on the reflection of the person in the bottle, conveying a sense of introspection and appreciation. The style should be inspired by the works of Andy Warhol." , "The Winning Shot", "Create a classical style painting using the colors (138, 150, 149) to convey a positive emotion. The piece should depict a person holding a basketball, sitting on a couch, with a cellphone and a TV in the background. The focus should be on the person's confident expression, conveying a sense of accomplishment and success. The style should be inspired by the works of Keith Haring."]

                            [['a room with a television, a desk, and a chair '], ['person', 'dog', 'tv', 'book', 'chair', 'remote', 'couch', 'bed'], ['neutral', 'excited' 'angry', 'admiration'], [(229, 232, 230), (240, 198, 165), (239, 197, 164), (231, 233, 226), (231, 178, 146), (226, 231, 231), (228, 231, 229), (236, 238, 231)], ['NEGATIVE', 'POSITIVE'], (today)]
                            your response: ["Media Overload", "Create a digital art piece inspired by the works of Salvador Dali, using the color (231, 233, 226) to convey a neutral emotion. The piece should depict a person sitting on a chair, holding a book, with a TV in the background. The TV should display a distorted image of a dog, representing the person's confusion and disconnection from reality.", "A Furry Companion", "Create a futuristic Bauhaus style painting inspired by the works of Walter Gropius, using the colors (229, 232, 230) to convey a feeling of admiration. The painting should depict a person sitting on a couch, with a dog laying on their lap, both looking at a TV. The focus should be on the dog's expression, conveying a sense of love and loyalty.", "The Rage Inside", "Create a black and white drawing inspired by the works of Mark Rothko, using the color (231, 178, 146) to convey an angry emotion. The painting should depict a person standing in front of a desk, with a chair tipped over and a remote in their hand. The focus should be on the person's expression, conveying a sense of frustration and anger.", "A Relaxing Evening", "Create a realistic surrealist style painting inspired by the works of Salvador Dali, using the colors (228, 231, 229) to convey a positive emotion. The piece should depict a person sitting on a bed, holding a remote, with a TV and a book on the nightstand. The focus should be on the person's expression, conveying a sense of relaxation and contentment.", "The World in Our Hands", "Create an classical painting inspired by the works of Vincent Van Gogh, using the colors (240, 198, 165) and (239, 197, 164) to convey an excited emotion. The painting should depict a person holding a remote, with a TV in the background displaying a world map. The focus should be on the person's expression, conveying a sense of wonder and excitement about the world. The style should be with smooth lines and bold colors."]

                        """
        
        self.chat_response = ""
        self.video_analysis = video
        self.audio_analysis = audio
        self.dalle_prompts = []
        self.image_results = []

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
    
    def generate_images(self, results, title, prompt):
        openai.api_key = self.openaikey

        image = openai.Image.create(
                prompt = prompt,
                n=1,
                size = "256x256"
            )
        
        results.put({
                "title": title,
                "link": image["data"][0]["url"],
            })
    
    def create_images(self):
        results = Queue()
        self.dalle_prompts = ast.literal_eval(self.chat_response)
        image_one_thread = threading.Thread(target=self.generate_images, args=(results, self.dalle_prompts[0], self.dalle_prompts[1]))
        image_two_thread = threading.Thread(target=self.generate_images, args=(results, self.dalle_prompts[2], self.dalle_prompts[3]))
        image_three_thread = threading.Thread(target=self.generate_images, args=(results, self.dalle_prompts[4], self.dalle_prompts[5]))
        image_four_thread = threading.Thread(target=self.generate_images, args=(results, self.dalle_prompts[6], self.dalle_prompts[7]))
        image_five_thread = threading.Thread(target=self.generate_images, args=(results, self.dalle_prompts[8], self.dalle_prompts[9]))

        image_one_thread.start()
        image_two_thread.start()
        image_three_thread.start()
        image_four_thread.start()
        image_five_thread.start()

        image_one_thread.join()
        image_two_thread.join()
        image_three_thread.join()
        image_four_thread.join()
        image_five_thread.join()

        while not results.empty():
            image = results.get()
            self.image_results.append(image)

        

            
