# mood.ai
Application that captures moments into AI generated art!

# How it works!
1. Record the moment you would like to capture!
2. Program runs video and audio through numerous ML models running in parallel such as\n
    <ol><li>video: multi object detection</li>
    <li>video: facial emotion detection</li>
    <li>video: image classification</li>
    <li>video: primary color detection</li>
    <li>audio: transcription</li>
    <li>audio: sentiment analysis</li>
    <li>audio: energy level detection</li></ol>
3. With all the data received from these ML models, Chat GPT generates prompt ideas that encorporates the essence of the moment
4. DALLE-2 then generates images from those prompts and gives them to you to enjoy

# How to use!
If you would like to test the application for yourself, check out the link below
https://rahulmedicharla-mood-ai-app-y2im29.streamlit.app/

If you would like to fork and change the program, there are some preliminary steps that first must be completed in order for you to be able to run this program locally

1. First clone the repo to you local computer, and make sure you have the latest python installed, www.python.org
2. Generate a virtual environment for this program running this in your terminal,
```python -m venv myenv```
3. Activate virtual environment by running
```source myenv/bin/activate``` on MacOs or Linux, or 
```source myenv/Scripts/activate``` on Windows
4. Everytime you want to run the program, make sure to activate and virtual environment as this is where all the dependencies for the project will live
5. Install all dependecies for the project in your virtual environment by running 
```pip install -r requirements.txt``` on Windows, and
```pip3 install requirements.txt``` on Mac
6. Create a openai api key on the openai website, and have it on hand. You'll need it when running the program
9. There! you should now be ready to run the program.

# Run the program
To run the program simply type
```streamlit run app.py``` into your terminal
The program will take a second to boot up. Once the camera is up on your screen, it will start recording automatically and click the 'q' button whenever you are finished. 

The output may take a second to generate the images but enjoy!
