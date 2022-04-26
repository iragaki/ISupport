import speech_recognition as sr
from gtts import gTTS
import pyttsx3
import time 
import datetime
import webbrowser
import playsound
import os
import requests
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import urllib
import urllib.request as urllib2
import json
import wikipedia
import sys
from time import strftime
import re


wikipedia.set_lang('vi')
language = 'vi'

def speak(text):
    print("IS Support: ", text)
   
    tts = gTTS(text=text, lang="vi", slow=False)
    tts.save("sound.mp3")
    playsound.playsound("sound.mp3", True)
    os.remove("sound.mp3")

def get_audio():
    ear_robot = sr.Recognizer()
    with sr.Microphone() as source:
        print("IS Support: Listening ... \t\t  0.0 ")
        audio = ear_robot.listen(source, phrase_time_limit=5)
        try:
            text = ear_robot.recognize_google(audio, language="vi-VN")
            print("Tôi:  ", text)
            return text
        except:
            print("Erro --__-- ")
            return 0

def get_audio_2():
    ear_robot = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening ===========================")
        audio = ear_robot.listen(source, phrase_time_limit=4)
    try:
        text = ear_robot.recognize_google(audio, language="vi-VN")
    except:
        print("Nhận dạng giọng nói thất bại. Vui lòng nói lại <>")
        text = get_audio_2()
    return text.lower()

def stop():
    speak("Goodbye sir , see you soon")

def get_text():
    for i in range(3):
        text = get_audio()
        if text:
            return text.lower()
        elif i < 2:
            speak(f"Can you say it again sir ? {name}")
    time.sleep(3)
    stop()
    return 0

def hello(name):
    day_time = int(strftime('%H'))

    if 0 <= day_time < 11:
        speak(f'Goodmorning  {name}. Have a good day sir.')
    elif 13 <= day_time < 18:
        speak(f'Goodafternoon {name}. Nice Day sir ')
    elif 18 <= day_time <= 23:
        speak(f'Goodnight {name}. How your day?')

def get_time(text):
    now = datetime.datetime.now()
    if 'giờ' in text:
        speak(f'Time is {now.hour}:{now.minute}:{now.second} ')
    elif "ngày" in text:
        speak(f'Day {now.day} Month {now.month} Year {now.year}')
    else:
        speak(f'I dont understand sir , can you repeat onemor time sir ?')

def open_application(text):
    if "một" in text:
        speak("Spotify opening")
        os.system("C:\\Users\\Asus\\Desktop\\Spotify.lnk")
    elif "2" in text:
        speak("Steam opening")
        os.system("C:\\Users\\Public\\Desktop\\Steam.lnk")
    elif "ba" in text:
        speak("Garena opening")
        os.system("C:\\Users\\Asus\\Desktop\\Garena.lnk")
    elif "5"  in text:
        speak("360 Fusion opening")
        os.system("C:\\Users\\Asus\\Desktop\\Autodesk Fusion 360.lnk")
    else:
        speak("uninstall app sir")

def open_website(text):
    reg_ex = re.search('mở (.+)', text)
    if reg_ex:
        domain = reg_ex.group(1)
        url = "https://www." + domain
        webbrowser.open(url)
        speak("Website opened. ")
        if input("If want me to wait press q: ") == "q":
            pass
        return True
    else:
        return False        

def open_google_and_search(text):
    search_for = str(text).split("kiếm" , 1)[1]
    url = f"https://www.google.com/search?q={search_for}"
    webbrowser.get().open(url)
    speak("There is information you need")

def current_weather():
    speak("Where do you want to see the weather?")    
    ow_url = "http://api.openweathermap.org/data/2.5/weather?"
    city = get_text()
    if not city:
        pass
    api_key = "59bc0e0fd4a7845269e53a8de4e23d3d"  
    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    if data["cod"] != "404":
        city_res = data["main"] 
        current_temperature = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        suntime = data["sys"]
        sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
        sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
        wthr = data["weather"]
        weather_description = wthr[0]["description"]
        now = datetime.datetime.now()
        content = f"""
        Day {now.day} Month {now.month} Year {now.year}
        Sunrise {sunrise.hour} Hour {sunrise.minute} Minute
        Sunset {sunset.hour} Hour {sunset.minute} Minute
        Temperature {current_temperature} Celsius 
        Pressure {current_pressure} Hecta Pascal
        Humidity {current_humidity}%
        """
        speak(content)
    else:
        speak("Location not found sir") 

def play_youtube():
    speak("What content do you want to see sir ?")      
    search = get_text()
    url = f"https://www.youtube.com/search?q={search}"
    webbrowser.get().open(url)
    speak("There you are sir")  
def tell_me_about():
    try:
        speak("What do you want to learn about sir?")
        text = get_text()
        contents = wikipedia.summary(text).split('\n')
        speak(contents[0])
        dem = 0
        for content in contents[1:]:
            if dem < 2:
                speak("Do you want to learn more?")
                ans = get_text()
                if 'có' not in ans:
                    break
            dem += 1
            speak(content)
        speak("I Support cant understand your terms")
    except:
        speak(f"{name} không định nghĩa được thuật ngữ của bạn !!!")

def help_me():
    speak(f"""
    IS Support have functions:
    1. chào hỏi
    2. 
    """)
def main_brain():
    speak("Welcome back my lord, what can i help you sir")
    global robot_name
    robot_name = "IS Support"
    global name
    name = get_text()
    if name:
        speak(f'Hello sir {name}')
        speak(f'What can i help you sir ?')
        while True:
            text = get_text()
            if not text:
                break
            elif ('bye' in text) or ('Goodbye' in text):
                stop()
                break
            elif ('xin chào' in text) or ('Hello IS' in text):
                hello(name)
            elif 'help me' in text:
                help_me()
            elif "hiện tại" in text:
                get_time(text)
            elif "mở" in text:
                if '.' in text:
                    open_website(text)
                else:
                    open_application(text)
            elif "tìm kiếm" in text:
                open_google_and_search(text)            
            elif "thời tiết" in text:
                current_weather()
            elif "youtube" in text:
                play_youtube() 
            elif "thư viện" in text:
                tell_me_about()  
            else:
                speak('Funciton will update soon')


main_brain()