from calendar import month
from email.mime import audio
from tkinter import BROWSE
import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser 
import wikipedia
import smtplib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import pyjokes
import pyowm
import pywhatkit


engine = pyttsx3.init()


voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)
newVoiceRate = 150
engine.setProperty('rate', newVoiceRate)

def speak (audio):
    engine.say(audio)
    engine.runAndWait()


def time():
    Time = datetime.datetime.now().strftime("%I:%M:%S") #Conseguir la hora, con este formato
    speak(Time)

def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    speak("La fecha Actual es")
    speak(date)
    speak("Del mes numero")
    speak(month)
    speak("del año")
    speak(year)

def wishme():
    #speak("La hora actual es:")
    
    #time()
    #date()

    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        speak("Buenos Dias")
    elif hour >= 12 and hour <= 18:
        speak("Buenas Tardes")
    elif hour >= 18 and hour <= 24:
        speak("Buenas noches")
    else:
        speak("Buenas noches")
        
    speak("Friday a su servicio!, como puedo ayudarle")
    
    
def jokes():
    speak(pyjokes.get_joke(language='es', category= 'all'))


def getClimate():
    apikey = "abcdefghijklimnopqrstuvxyz"
    #Se crea la instancia OWM pasando la llave para el uso del API.
    owm = pyowm.owm(apikey)
    #Se obtiene la llave de uso del API
    print(owm.get_API_key())
    #Se define la ciudad por nombre o se pasa la coordenada.
    speak("Dime que ciudad Deseas conocer el clima ")
    obs = takeCommand()
    #Se Instancia los datos de la estacion meterologica.
    w = obs.get_weather()
    speak("El Clima en"+ obs + "es " + w.get_temperature())
#Obtener un comando por el usuario
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Escuchando...")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Reconociendo...")
        query = r.recognize_google(audio, language='es-SP') #in language, the value en-US, used to put the interpreter in English / Spanish = usamos es-SP, y por las pruebas funciona
        print(query)
    except Exception as e:
        print(e)
        speak("Disculpa no he entendido...")
        return "None"
    with open("recorded.wav", "wb") as f:
        f.write(audio.get_wav_data())
    return query
#takeCommand()

#Buscar en google
def search(something):
    browser = webdriver.Chrome(executable_path= 'C:\\ChromeDriver\\chromedriver.exe')
    browser.maximize_window()
    browser.get('https://www.google.com/')
    #En la linea siguiente accedemos a la barra de busqueda de google 
    findElem = browser.find_element_by_name('q')
    #Enviamos el parametro que recibe la funcion a la barra de busqueda del navegador
    findElem.send_keys(something)
    findElem.send_keys(Keys.RETURN) #Darle al ENTER

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Hola soy tu asistente por voz: ")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print('Has dicho: {}'.format(text))
            print(text)
            if "Amazon" in text:
                webbrowser.open('http://amazon.es')
            elif "noticias" in text:
                webbrowser.open("https://www.lavoz.com.ar/")
        except:
            print("No he entendido")

def sendMail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    #Verificar la conexion al servidor
    server.ehlo()
    server.starttls()
    #Nos logeamos nosotros,
    server.login("mateo.j.ramallo@gmail.com", "password")
    server.sendmail("mateo.j.ramallo@gmail.com", to, content)
    server.close()




if __name__ == "__main__":
    wishme()
    
    while True:
        query = takeCommand().lower()
        print(query)
        
        if "hora" in query:
            time()
        elif "fecha" in query:
            date()
        elif "offline" in query:
            speak("Saludos, señor")
            quit()
        elif "buscar" in query:
            search = query.replace('busca', '')
            wikipedia.set_lang("es")
            wiki = wikipedia.summary(search, 1)
            print(search + " : "+ wiki)
            speak(wiki)
        elif "hazme acordar de algo" in query:
            speak("Okey, dime que ")
            data = takeCommand()
            speak("Dijiste: " + data)
            remember = open("data.txt", "w")
            remember.write(data)
            remember.close()
        elif "que te había dicho" in query:
            remember = open("data.txt", "r")
            speak("Habias dicho: " + remember.read())
        elif "chiste" in query:
            jokes()
        elif "clima" in query:
            getClimate()
        elif "reproducir" in query:
            music = query.replace('reproducir', '')
            speak("Reproduciendo" + music)
            pywhatkit.playonyt(music)
        elif "noticias" in query:
            webbrowser.open("https://www.lavoz.com.ar/")
        elif "Amazon" in query:
            webbrowser.open('https://www.amazon.com/')
        elif "enviar correo" in query:
            try:
                speak("Que Deberia Decir?")
                content = takeCommand()
                to = "mateo.j.ramallo@gmail.com"
                sendMail(to, content)
                speak(content)
            except Exception as e:
                print(e)
                speak("Error Al Enviar El Mensaje")
        elif "búscame" in query:
            speak("Buscando...")
            something = query.replace('buscame', '').strip()
            speak("Buscando..." + something)
            search(something)
        elif "cerrar sesión" in query:
            os.system("shutdown -1")
        elif "apagar" in query:
            os.system("shutdown /s /t 1")
        elif "reiniciar" in query:
            os.system("shutdown /r /t 1")