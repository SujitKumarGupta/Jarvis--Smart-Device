import speech_recognition as sr
import webbrowser
import pyttsx3
import music_library
import requests
import os
import platform
import google.genai as genai
from dotenv import load_dotenv
load_dotenv()
recognizer = sr.Recognizer()

newsapi = "75d93cb14126445aa1de177e8f4fa916"



def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY environment variable")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=command
    )
    return response.text


def processCommand(c):
    print(c)
    if "open google" in c.lower():
        webbrowser.open("http://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("http://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("http://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("http://linked.com")
    elif(c.lower().startswith("play")):
        song = c.lower().split(" ")[1]
        link = music_library.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")

        # Check if request was successful
        if r.status_code == 200:
            # Convert response to JSON
            data = r.json()
            # Extract the articles
            articles = data.get('articles', [])

            for article in articles:
                speak(article['title'])
    elif "shutdown" in c:
        speak("Shutting down the system.")
        if platform.system() == "Windows":
            os.system("shutdown /s /t 5")
        elif platform.system() == "Linux":
            os.system("shutdown now")
        return

    elif "restart" in c:
        speak("Restarting the system.")
        if platform.system() == "Windows":
            os.system("shutdown /r /t 5")
        elif platform.system() == "Linux":
            os.system("reboot")
        return
    else:
        output = aiProcess(c)
        speak(output)
               

if __name__ == "__main__":
    speak("Hey I am Jarvis How can I help you")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Yes")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))

