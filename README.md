# mood.ai
This is a program that captures moments into AI generated art!

# How it works!
1. Record the moment you would like to capture!
2. Program runs video and audio through numerous ML models running in parallel such as
    -> video: multi object detection
    -> video: facial emotion detection
    -> video: image classification
    -> video: primary color detection
    -> audio: transcription
    -> audio: sentiment analysis
    -> audio: emotion detection from text
    -> audio: identifying key words from text
3. With all the data received from these ML models, Chat GPT generates prompt ideas that encorporates the essence of the moment
4. DALLE-2 then generates images from those prompts and gives them to you in the "output.html" file for you to enjoy

# How to use!
There are some preliminary steps that first must be completed in order for you to be able to run this program

1. First clone the repo to you local computer, and make sure you have the latest python installed, www.python.org
2. Generate a virtual environment for this program running this in your terminal,
```python -m venv myenv```
3. Activate virtual environment by running
```source myenv/bin/activate``` on MacOs or Linux, or 
```source myenv/Scripts/activate``` on Windows
4. Everytime you want to run the program, make sure to activate the virtual environment as this is where all the dependencies for the project will live
5. Install all dependecies for the project in your virtual environment by running 
```pip install -r requirements.txt``` on Windows, and
```pip3 install requirements.txt``` on Mac
6. Install one more dependency by running
```python -m spacy download en_core_web_sm``` 
7. Download the ffmpeg executable from this link and place the exectuable in your root directory of this project
 -> https://ffmpeg.org/download.html
8. Create a openai api key on the openai website, create a 'keys.py' file in the root directory of this project, and put this as the first line in that file
```openaikey = "your api key"```
9. There! you should now be ready to run the program.

# Run the program
To run the program simply type
```python main.py``` into your terminal
The program will take a second to boot up. Once the camera is up on your screen, it will start recording automatically and click the 'q' button whenever you are finished. 

The output may take a second to generate the images but enjoy!
