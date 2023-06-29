import speech_recognition as sr
from gtts import gTTS
import os
import datetime
import numpy as np
import transformers
class chatBot():
    def action_time(self):
        return  datetime.datetime.now().time().strftime('%H:%M')
    
    def __init__(self,name) -> None:
        print("-----Starting up", name, "------")
        self.name=name

    def wake_up(self,text):
        return True if self.name.lower() in text.lower() else False
    
    def speech_to_text(self):
        recognizer=sr.Recognizer()
        with sr.Microphone() as mic:
            print("listening...")
            audio=recognizer.listen(mic)
        try:
            self.text = recognizer.recognize_google(audio)
            print("me -->", self.text)
        except Exception as e:
            self.text="Error"
            print("me --> Error:", str(e))

    def text_to_speech(self,text):
        print("AI ----> ",text)
        speaker=gTTS(text=text,lang="en",slow=False)
        speaker.save("res.mp3")
        os.system("afplay res.mp3")
        os.remove("res.mp3")

if __name__=="__main__":
    ai=chatBot(name="Dev")
    nlp=transformers.pipeline("conversational",model="microsoft/DialoGPT-medium")
    os.environ["TOKENIZERS_PARALLELISM"]= "true"
    ex=True
    while ex :
        ai.speech_to_text()
        if(ai.wake_up(ai.text) is True):
            res="Hello I am Dev the AI, what can i do for you ?"
        elif any(i in ai.text for i in ["exit","quit","close","shutdown"]):
            res = np.random.choice(["Have a Good Day","Bye Bye","GoodBye!"])
            ex=False
        elif "time" in ai.text:
            res=ai.action_time()
        elif any(i in ai.text for i in ["thank","thanks","thank you"]):
            res=np.random.choice(["Your welcome!","anytme!","no problem!","cool!","i am here if you need me!","Peace Out!"])
        else:
            if ai.text=="Error":
                res = "Sorry, come again?"
            else:
                chat=nlp(transformers.Conversation(ai.text),pad_token_id=50256)
                res =str(chat)
                res= res[res.find("bot >> ")+6:].strip()
        ai.text_to_speech(res)
    print("------------ Closing down Dev -----------")
