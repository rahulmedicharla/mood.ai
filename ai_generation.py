import openai, keys, ast, threading
from queue import Queue

class Generation:
    def __init__(self, video, audio):
        self.openaikey = keys.openaikey
        self.chat_prompt = """I will give you a bunch of lists. I want you to choose a random item from each of the lists and generate 5 unique prompts that can be used to create AI art. I want each prompt you give to follow a unique and fancy art style different from the others. The first list is a list of captions describing the video. Only use this value in TWO of the prompts generated. The second list is a list of objects. The third list if a list of emotions. the fourth list is a list of colors given in RGB. ONLY for this list you should convert the RGB values to their closest color name and select three colors to use. The fourth list is energy levels, and the fifth list is a list of keywords. I would like at least one prompt to emphasize emotions through color, and at least one prompt be a fully abstracted version of the first list, and use warm colors for a high energy level and cool colors for a low energy level. Use random weights to determine how important a piece of information is for the prompt. Generate titles for each image as well. For some of the prompts follow art styles from famous artists. ONLY GIVE ME THE YOUR RESPONSE IN THE FORMAT ["title 1", "prompt 1", "title 2", "prompt 2", "titile 3", "prompt3"]. 

                            Follow these examples below:
                            [['a man laying on a couch looking at his phone'], ['chair', 'couch', 'person', 'cellphone', 'bottle', 'tv'], ['happy', 'admiration', 'gratitude', 'neutral'], [(167, 184, 182), (145, 172, 173), (147, 173, 171), (142, 168, 166), (136, 162, 165), (141, 161, 158), (147, 159, 158), (145, 160, 158), (138, 150, 149)], ['High'], (basketball)]
                            your response: ["Serenity in Pixels", "Create an abstract representation of a man laying on a couch looking at his phone using a color palette of muted greens and blues. The artwork should convey a sense of calm and tranquility. Use the chair and cellphone objects as additional elements within the piece to add depth and interest. Follow a Baroque art style", "Bottled Admiration", Using a high-energy color scheme of bright oranges and reds, create a digital painting of a bottle filled with gratitude. The bottle should be the focal point of the piece, with a person in the background expressing their admiration. Incorporate the TV object in the background to add a sense of motion and energy. Follow a pop art style", "Neutral Affections", "Create an impressionist painting using a high energy color palate  from  RGB (142, 168, 166). The scene should evoke a sense of gratitude and happiness. Use the couch and bottle objects as the main elements of the artwork, with a person off to the side expressing their contentment." , "Phone in Motion" , "Create a classical illustration of a person on a cellphone in a dynamic pose, using a color palette of blues and purples to convey a sense of energy and movement. Incorporate the chair object in the background to ground the composition. ", "Basketball Gratitude", "Using a warm color scheme of oranges and yellows, create an digital illustration of a basketball expressing gratitude. The artwork should convey a sense of high energy and enthusiasm. Use the bottle and cellphone objects in the background to add additional interest to the piece."]
                        
                            [['a room with a television, a desk, and a chair '], ['person', 'dog', 'tv', 'book', 'chair', 'remote', 'couch', 'bed'], ['neutral', 'excited' 'angry', 'admiration'], [(229, 232, 230), (240, 198, 165), (239, 197, 164), (231, 233, 226), (231, 178, 146), (226, 231, 231), (228, 231, 229), (236, 238, 231)], ['Low'], (today)]
                            ["Reflections of a Home", "Create an classical painting of a room with a television, a desk, and a chair using a monochromatic color scheme of RGB (231, 233, 226). The artwork should evoke a sense of neutral emotion and contemplation. Incorporate the chair and book objects into the piece as the main elements to add depth and interest.", "Companionship Dreams", "Using a color palette of soft pinks and blues, create a digital painting of a person and their dog sitting on a couch together. The artwork should evoke a sense of excitement and admiration. Incorporate the remote and TV objects in the background to ground the composition and add context.", "Fury in the Dark", "Create an abstract representation of anger and frustration using a color palette of dark grays and muted blues from the RGB (229, 232, 230). Use the bed object as the main element of the piece to convey a sense of restlessness and unease.", "The Power of Knowledge", "Using a warm color scheme of oranges and yellows, create a baroqeue painting of a person reading a book at a desk. The artwork should evoke a sense of admiration and inspiration. Incorporate the chair and remote objects in the background to add additional interest to the piece.", "Sleepy Hues", "Create an expressionist painting of sleepiness and relaxation using a color palette of muted pinks and grays from the RGB (231, 178, 146) and (229, 232, 230). Use the couch object as the main element of the piece to convey a sense of comfort and tranquility. Incorporate the person object in the background to add depth and interest to the composition."]
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

        message = str([self.video_analysis.video_classification,self.video_analysis.video_detected_objects, emotion_list, self.video_analysis.video_top_colors, self.audio_analysis.energy_level, self.audio_analysis.keywords])

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

        

            
