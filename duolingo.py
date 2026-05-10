
import sounddevice as sd
import random
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from translate import Translator
import time
import tkinter as tk

# Инициализация переменных
score = 0
data = ""
lvl = 1
location = 1 
scoreWrite = False
duration = 5 
sample_rate = 44100

# Переменные для хранения данных текущего юзера, чтобы не зависеть от полей ввода
current_user = ""
current_pass = ""

e1 = None
e2 = None

root = tk.Tk()
root.title("Duolingo on python")
root.geometry("450x630")

def Clear():
    for widget in root.winfo_children():
        widget.destroy()

def readDb():
    global data
    try:
        with open("db.txt", "r", encoding="utf-8") as file:
            data = file.read()
    except FileNotFoundError:
        data = ""

def start_screen():
    Clear()
    lbl = tk.Label(root, text="Пожалуйста авторизуйтесь\nили зарегистрируйтесь", font=("Arial", 20))
    lbl.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
    
    tk.Button(root, text="Авторизация", font=("Arial", 18), 
              command=autorization_screen, width=15).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    tk.Button(root, text="Регистрация", font=("Arial", 18), 
              command=registration_screen, width=15).place(relx=0.5, rely=0.6, anchor=tk.CENTER)

def registration_screen():
    global e1, e2
    Clear()
    tk.Label(root, text="Регистрация", font=("Arial", 24)).place(relx=0.5, rely=0.3, anchor=tk.CENTER)
    
    e1 = tk.Entry(root, font=("Arial", 18))
    e1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    e2 = tk.Entry(root, font=("Arial", 18), show="*")
    e2.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
    
    # При регистрации вызываем спец. функцию, которая заберет данные из полей ПЕРЕД их удалением
    tk.Button(root, text="Зарегистрироваться", font=("Arial", 18), 
              command=process_registration).place(relx=0.5, rely=0.7, anchor=tk.CENTER)
    
def process_registration():
    global current_user, current_pass
    current_user = e1.get()
    current_pass = e2.get()
    write_db_data()
    autorization_screen()

def write_db_data():
    global score, current_user, current_pass
    # Проверяем, что у нас есть данные для записи
    if current_user and current_pass:
        # Мы не просто дописываем, а создаем новую строку с результатом
        with open("db.txt", "a", encoding="utf-8") as file:
            file.write(f"USER:{current_user}|PASS:{current_pass}|SCORE:{score}\n")

def autorization_screen():
    global e1, e2
    Clear()
    tk.Label(root, text="Авторизация", font=("Arial", 24)).place(relx=0.5, rely=0.3, anchor=tk.CENTER)
    
    e1 = tk.Entry(root, font=("Arial", 18))
    e1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    e2 = tk.Entry(root, font=("Arial", 18), show="*")
    e2.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
    
    tk.Button(root, text="Войти", font=("Arial", 18), 
              command=test_auth).place(relx=0.5, rely=0.7, anchor=tk.CENTER)

def test_auth():
    global score, current_user, current_pass
    readDb()
    
    login = e1.get()
    password = e2.get()
    
    search_pattern = f"USER:{login}|PASS:{password}"
    found = False
    max_score = 0
    
    lines = data.split('\n')
    for line in lines:
        if search_pattern in line:
            try:
                parts = line.split('|')
                # Ищем кусок со SCORE
                for p in parts:
                    if "SCORE:" in p:
                        s_val = int(p.split(':')[1])
                        if s_val >= max_score:
                            max_score = s_val
                found = True
            except:
                continue

    if found:
        current_user = login
        current_pass = password
        score = max_score
        Clear()
        tk.Label(root, text=f"Успех!\nТвои очки: {score}\nЗагрузка...", font=("Arial", 20)).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        root.after(2000, gameMainLoop)
    else:
        tk.Label(root, text="Неверный логин или пароль", fg="red").place(relx=0.5, rely=0.8, anchor=tk.CENTER)


def gameMainLoop():
    Clear()
    
    tk.Label(root, text=f"Уровень: {lvl}  Локация: {location}", font=("Arial", 18)).place(relx=0.5, rely=0.1, anchor=tk.CENTER)
    tk.Label(root, text=f"Очки: {score}", font=("Arial", 18)).place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    proverka()

def proverka():
    global lvl, location
    if lvl == 1 and location == 1:
        tk.Label(root, text="как будет слово <<привет>>\n на английском?", font=("Arial", 18)).place(relx=0.5, rely=0.1, anchor=tk.CENTER) 
        ot1l1l1 = tk.Button(root, text="Hello", font=("Arial", 18), command=cal1l1, width=15) 
        ot1l1l1.place(relx=0.3, rely=0.3, anchor=tk.CENTER)

        ot2l1l1 = tk.Button(root, text="Hi", font=("Arial", 18), command=dcal1l1, width=15)
        ot2l1l1.place(relx=0.7, rely=0.3, anchor=tk.CENTER)

    if lvl == 2 and location == 1:
        tk.Label(root, text="как будет слово <<солнце>>\n на английском?", font=("Arial", 18)).place(relx=0.5, rely=0.1, anchor=tk.CENTER) 
        ot1l1l1 = tk.Button(root, text="sun", font=("Arial", 18), command=cal1l1, width=15) 
        ot1l1l1.place(relx=0.3, rely=0.3, anchor=tk.CENTER)

        ot2l1l1 = tk.Button(root, text="summ", font=("Arial", 18), command=dcal1l1, width=15)
        ot2l1l1.place(relx=0.7, rely=0.3, anchor=tk.CENTER)

    if lvl == 3 and location == 1:
        tk.Label(root, text="как будет слово <<вода>>\n на английском?", font=("Arial", 18)).place(relx=0.5, rely=0.1, anchor=tk.CENTER) 
        ot1l1l1 = tk.Button(root, text="water", font=("Arial", 18), command=cal1l1, width=15) 
        ot1l1l1.place(relx=0.3, rely=0.3, anchor=tk.CENTER)

        ot2l1l1 = tk.Button(root, text="wutter", font=("Arial", 18), command=dcal1l1, width=15)
        ot2l1l1.place(relx=0.7, rely=0.3, anchor=tk.CENTER)

    #заглушка для проверки перехода на следующую локацию
    if lvl == 4 and location == 1:
        tk.Label(root, text="как будет слово <<автомобиль>>\n на английском?\nговори... у тебя 5 секунд", font=("Arial", 18)).place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        
        root.update()  # Обновляем интерфейс, чтобы надпись появилась до начала записи

        recording = sd.rec(
            int(duration * sample_rate), # длительность записи в сэмплах
            samplerate=sample_rate,      # частота дискретизации
            channels=1,                  # 1 — это моно
            dtype="int16")               # формат аудиоданных
        sd.wait() 

        wav.write("output.wav", sample_rate, recording)

        recognizer = sr.Recognizer()
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        try:
            text = ""
            text = recognizer.recognize_google(audio, language="en-US")  # распознаём с помощью Google API
        except sr.UnknownValueError:
            text = ""

        if text.lower() == "car":
            label = tk.Label(root, text="Ты сказал: " + text, font=("Arial", 18))
            label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
            root.after(2000,cal1l1)
        else:
            label = tk.Label(root, text="Ты сказал: " + text, font=("Arial", 18))
            label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
            root.after(2000,dcal1l1)
        
    
    if lvl == 5 and location == 1:
        tk.Label(root, text="как будет слово <<пока>>\n на английском?\nговори... у тебя 5 секунд", font=("Arial", 18)).place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        
        root.update()  # Обновляем интерфейс, чтобы надпись появилась до начала записи

        recording = sd.rec(
            int(duration * sample_rate), # длительность записи в сэмплах
            samplerate=sample_rate,      # частота дискретизации
            channels=1,                  # 1 — это моно
            dtype="int16")               # формат аудиоданных
        sd.wait()

        wav.write("output.wav", sample_rate, recording)

        recognizer = sr.Recognizer()
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        try:
            text = ""
            text = recognizer.recognize_google(audio, language="en-US")  # распознаём с помощью Google API
        except sr.UnknownValueError:
            text = ""

        if text.lower() == "bye":
            label = tk.Label(root, text="Ты сказал: " + text, font=("Arial", 18))
            label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
            root.after(2000,cal1l1)
        else:
            label = tk.Label(root, text="Ты сказал: " + text, font=("Arial", 18))
            label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
            root.after(2000,dcal1l1)

    if lvl == 1 and location == 2:
        tk.Label(root, text="как будет слово <<собирать>>\n на английском?", font=("Arial", 18)).place(relx=0.5, rely=0.1, anchor=tk.CENTER) 
        ot1l1l1 = tk.Button(root, text="assembly", font=("Arial", 18), command=cal1l1, width=15) 
        ot1l1l1.place(relx=0.3, rely=0.3, anchor=tk.CENTER)

        ot2l1l1 = tk.Button(root, text="assembler", font=("Arial", 18), command=dcal1l1, width=15)
        ot2l1l1.place(relx=0.7, rely=0.3, anchor=tk.CENTER)

    if lvl == 2 and location == 2:
        tk.Label(root, text="как будет слово <<плюс>>\n на английском?", font=("Arial", 18)).place(relx=0.5, rely=0.1, anchor=tk.CENTER) 
        ot1l1l1 = tk.Button(root, text="plus", font=("Arial", 18), command=cal1l1, width=15) 
        ot1l1l1.place(relx=0.3, rely=0.3, anchor=tk.CENTER)

        ot2l1l1 = tk.Button(root, text="plis", font=("Arial", 18), command=dcal1l1, width=15)
        ot2l1l1.place(relx=0.7, rely=0.3, anchor=tk.CENTER)

    if lvl == 3 and location == 2:
        tk.Label(root, text="как будет слово <<минус>>\n на английском?", font=("Arial", 18)).place(relx=0.5, rely=0.1, anchor=tk.CENTER) 
        ot1l1l1 = tk.Button(root, text="muns", font=("Arial", 18), command=dcal1l1, width=15) 
        ot1l1l1.place(relx=0.3, rely=0.3, anchor=tk.CENTER)

        ot2l1l1 = tk.Button(root, text="minus", font=("Arial", 18), command=cal1l1, width=15)
        ot2l1l1.place(relx=0.7, rely=0.3, anchor=tk.CENTER)

    #заглушка для проверки перехода на следующую локацию
    if lvl == 4 and location == 2:
        tk.Label(root, text="как будет слово <<регистр>>\n на английском?\nговори... у тебя 5 секунд", font=("Arial", 18)).place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        
        root.update()  # Обновляем интерфейс, чтобы надпись появилась до начала записи

        recording = sd.rec(
            int(duration * sample_rate), # длительность записи в сэмплах
            samplerate=sample_rate,      # частота дискретизации
            channels=1,                  # 1 — это моно
            dtype="int16")               # формат аудиоданных
        sd.wait()

        wav.write("output.wav", sample_rate, recording)

        recognizer = sr.Recognizer()
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        try:
            text = ""
            text = recognizer.recognize_google(audio, language="en-US")  # распознаём с помощью Google API
        except sr.UnknownValueError:
            text = ""

        if text.lower() == "register" or text.lower() == "reg":
            label = tk.Label(root, text="Ты сказал: " + text, font=("Arial", 18))
            label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
            root.after(2000,cal1l1)
        else:
            label = tk.Label(root, text="Ты сказал: " + text, font=("Arial", 18))
            label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
            root.after(2000,dcal1l1)
    
    if lvl == 5 and location == 2:
        tk.Label(root, text="как будет слово <<нога>>\n на английском?\nговори... у тебя 5 секунд", font=("Arial", 18)).place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        
        root.update()  # Обновляем интерфейс, чтобы надпись появилась до начала записи

        recording = sd.rec(
            int(duration * sample_rate), # длительность записи в сэмплах
            samplerate=sample_rate,      # частота дискретизации
            channels=1,                  # 1 — это моно
            dtype="int16")               # формат аудиоданных
        sd.wait()

        wav.write("output.wav", sample_rate, recording)

        recognizer = sr.Recognizer()
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        try:
            text = ""
            text = recognizer.recognize_google(audio, language="en-US")  # распознаём с помощью Google API
        except sr.UnknownValueError:
            text = ""

        if text.lower() == "foot":
            label = tk.Label(root, text="Ты сказал: " + text, font=("Arial", 18))
            label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
            root.after(2000,cal1l1)
        else:
            label = tk.Label(root, text="Ты сказал: " + text, font=("Arial", 18))
            label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
            root.after(2000,dcal1l1)

    
    if lvl == 1 and location == 3:
        tk.Label(root, text="как будет слово <<луна>>\n на английском?", font=("Arial", 18)).place(relx=0.5, rely=0.1, anchor=tk.CENTER) 
        ot1l1l1 = tk.Button(root, text="moon", font=("Arial", 18), command=cal1l1, width=15) 
        ot1l1l1.place(relx=0.3, rely=0.3, anchor=tk.CENTER)

        ot2l1l1 = tk.Button(root, text="mun", font=("Arial", 18), command=dcal1l1, width=15)
        ot2l1l1.place(relx=0.7, rely=0.3, anchor=tk.CENTER)

    if lvl == 2 and location == 3:
        tk.Label(root, text="как будет слово <<земля>>\n на английском?", font=("Arial", 18)).place(relx=0.5, rely=0.1, anchor=tk.CENTER) 
        ot1l1l1 = tk.Button(root, text="erth", font=("Arial", 18), command=dcal1l1, width=15) 
        ot1l1l1.place(relx=0.3, rely=0.3, anchor=tk.CENTER)

        ot2l1l1 = tk.Button(root, text="earth", font=("Arial", 18), command=cal1l1, width=15)
        ot2l1l1.place(relx=0.7, rely=0.3, anchor=tk.CENTER)

    if lvl == 3 and location == 3:
        tk.Label(root, text="как будет слово <<меркурий>>\n на английском?", font=("Arial", 18)).place(relx=0.5, rely=0.1, anchor=tk.CENTER) 
        ot1l1l1 = tk.Button(root, text="mercuriy", font=("Arial", 18), command=dcal1l1, width=15) 
        ot1l1l1.place(relx=0.3, rely=0.3, anchor=tk.CENTER)

        ot2l1l1 = tk.Button(root, text="mercury", font=("Arial", 18), command=cal1l1, width=15)
        ot2l1l1.place(relx=0.7, rely=0.3, anchor=tk.CENTER)

    #заглушка для проверки перехода на следующую локацию
    if lvl == 4 and location == 3:
        tk.Label(root, text="как будет слово <<еда>>\n на английском?\nговори... у тебя 5 секунд", font=("Arial", 18)).place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        
        root.update()  # Обновляем интерфейс, чтобы надпись появилась до начала записи

        recording = sd.rec(
            int(duration * sample_rate), # длительность записи в сэмплах
            samplerate=sample_rate,      # частота дискретизации
            channels=1,                  # 1 — это моно
            dtype="int16")               # формат аудиоданных
        sd.wait()

        wav.write("output.wav", sample_rate, recording)

        recognizer = sr.Recognizer()
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        try:
            text = ""
            text = recognizer.recognize_google(audio, language="en-US")  # распознаём с помощью Google API
        except sr.UnknownValueError:
            text = ""

        if text.lower() == "food":
            label = tk.Label(root, text="Ты сказал: " + text, font=("Arial", 18))
            label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
            root.after(2000,cal1l1)
        else:
            label = tk.Label(root, text="Ты сказал: " + text, font=("Arial", 18))
            label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
            root.after(2000,dcal1l1)
    
    if lvl == 5 and location == 3:
        tk.Label(root, text="как будет слово <<есть (еду)>>\n на английском?\nговори... у тебя 5 секунд", font=("Arial", 18)).place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        
        root.update()  # Обновляем интерфейс, чтобы надпись появилась до начала записи

        recording = sd.rec(
            int(duration * sample_rate), # длительность записи в сэмплах
            samplerate=sample_rate,      # частота дискретизации
            channels=1,                  # 1 — это моно
            dtype="int16")               # формат аудиоданных
        sd.wait()

        wav.write("output.wav", sample_rate, recording)

        recognizer = sr.Recognizer()
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        try:
            text = ""
            text = recognizer.recognize_google(audio, language="en-US")  # распознаём с помощью Google API
        except sr.UnknownValueError:
            text = ""

        if text.lower() == "eat":
            label = tk.Label(root, text="Ты сказал: " + text, font=("Arial", 18))
            label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
            root.after(2000,cal1l1)
        else:
            label = tk.Label(root, text="Ты сказал: " + text, font=("Arial", 18))
            label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
            root.after(2000,dcal1l1)


    if lvl == 1 and location == 4:
        tk.Label(root, text="как будет слово <<потомучто>>\n на английском?", font=("Arial", 18)).place(relx=0.5, rely=0.1, anchor=tk.CENTER) 
        ot1l1l1 = tk.Button(root, text="becase", font=("Arial", 18), command=dcal1l1, width=15) 
        ot1l1l1.place(relx=0.3, rely=0.3, anchor=tk.CENTER)

        ot2l1l1 = tk.Button(root, text="because", font=("Arial", 18), command=cal1l1, width=15)
        ot2l1l1.place(relx=0.7, rely=0.3, anchor=tk.CENTER)

    if lvl == 2 and location == 4:
        tk.Label(root, text="как будет слово <<если>>\n на английском?", font=("Arial", 18)).place(relx=0.5, rely=0.1, anchor=tk.CENTER) 
        ot1l1l1 = tk.Button(root, text="if", font=("Arial", 18), command=cal1l1, width=15) 
        ot1l1l1.place(relx=0.3, rely=0.3, anchor=tk.CENTER)

        ot2l1l1 = tk.Button(root, text="fi", font=("Arial", 18), command=dcal1l1, width=15)
        ot2l1l1.place(relx=0.7, rely=0.3, anchor=tk.CENTER)

    if lvl == 3 and location == 4:
        tk.Label(root, text="как будет слово <<иначе>>\n на английском?", font=("Arial", 18)).place(relx=0.5, rely=0.1, anchor=tk.CENTER) 
        ot1l1l1 = tk.Button(root, text="esle", font=("Arial", 18), command=dcal1l1, width=15) 
        ot1l1l1.place(relx=0.3, rely=0.3, anchor=tk.CENTER)

        ot2l1l1 = tk.Button(root, text="else", font=("Arial", 18), command=cal1l1, width=15)
        ot2l1l1.place(relx=0.7, rely=0.3, anchor=tk.CENTER)

    #заглушка для проверки перехода на следующую локацию
    if lvl == 4 and location == 4:
        tk.Label(root, text="как будет слово <<нос>>\n на английском?\nговори... у тебя 5 секунд", font=("Arial", 18)).place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        
        root.update()  # Обновляем интерфейс, чтобы надпись появилась до начала записи

        recording = sd.rec(
            int(duration * sample_rate), # длительность записи в сэмплах
            samplerate=sample_rate,      # частота дискретизации
            channels=1,                  # 1 — это моно
            dtype="int16")               # формат аудиоданных
        sd.wait()

        wav.write("output.wav", sample_rate, recording)

        recognizer = sr.Recognizer()
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        try:
            text = ""
            text = recognizer.recognize_google(audio, language="en-US")  # распознаём с помощью Google API
        except sr.UnknownValueError:
            text = ""

        if text.lower() == "nose":
            label = tk.Label(root, text="Ты сказал: " + text, font=("Arial", 18))
            label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
            root.after(2000,cal1l1)
        else:
            label = tk.Label(root, text="Ты сказал: " + text, font=("Arial", 18))
            label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
            root.after(2000,dcal1l1)
    
    if lvl == 5 and location == 4:
        tk.Label(root, text="как будет слово <<стек>>\n на английском?\nговори... у тебя 5 секунд", font=("Arial", 18)).place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        
        root.update()  # Обновляем интерфейс, чтобы надпись появилась до начала записи

        recording = sd.rec(
            int(duration * sample_rate), # длительность записи в сэмплах
            samplerate=sample_rate,      # частота дискретизации
            channels=1,                  # 1 — это моно
            dtype="int16")               # формат аудиоданных
        sd.wait()

        wav.write("output.wav", sample_rate, recording)

        recognizer = sr.Recognizer()
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        try:
            text = ""
            text = recognizer.recognize_google(audio, language="en-US")  # распознаём с помощью Google API
        except sr.UnknownValueError:
            text = ""

        if text.lower() == "stack":
            label = tk.Label(root, text="Ты сказал: " + text, font=("Arial", 18))
            label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
            root.after(2000,cal1l1)
        else:
            label = tk.Label(root, text="Ты сказал: " + text, font=("Arial", 18))
            label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
            root.after(2000,dcal1l1)


    if lvl == 1 and location == 5:
        tk.Label(root, text="как будет слово <<пока чтото>>\n на английском?", font=("Arial", 18)).place(relx=0.5, rely=0.1, anchor=tk.CENTER) 
        ot1l1l1 = tk.Button(root, text="goodbuye", font=("Arial", 18), command=dcal1l1, width=15) 
        ot1l1l1.place(relx=0.3, rely=0.3, anchor=tk.CENTER)

        ot2l1l1 = tk.Button(root, text="while", font=("Arial", 18), command=cal1l1, width=15)
        ot2l1l1.place(relx=0.7, rely=0.3, anchor=tk.CENTER)

    if lvl == 2 and location == 5:
        tk.Label(root, text="как будет слово <<но>>\n на английском?", font=("Arial", 18)).place(relx=0.5, rely=0.1, anchor=tk.CENTER) 
        ot1l1l1 = tk.Button(root, text="btuton", font=("Arial", 18), command=dcal1l1, width=15) 
        ot1l1l1.place(relx=0.3, rely=0.3, anchor=tk.CENTER)

        ot2l1l1 = tk.Button(root, text="but", font=("Arial", 18), command=cal1l1, width=15)
        ot2l1l1.place(relx=0.7, rely=0.3, anchor=tk.CENTER)

    if lvl == 3 and location == 5:
        tk.Label(root, text="как будет слово <<плоский>>\n на английском?", font=("Arial", 18)).place(relx=0.5, rely=0.1, anchor=tk.CENTER) 
        ot1l1l1 = tk.Button(root, text="flat", font=("Arial", 18), command=cal1l1, width=15) 
        ot1l1l1.place(relx=0.3, rely=0.3, anchor=tk.CENTER)

        ot2l1l1 = tk.Button(root, text="flut", font=("Arial", 18), command=dcal1l1, width=15)
        ot2l1l1.place(relx=0.7, rely=0.3, anchor=tk.CENTER)

    #заглушка для проверки перехода на следующую локацию
    if lvl == 4 and location == 5:
        tk.Label(root, text="как будет слово <<отладка>>\n на английском?\nговори... у тебя 5 секунд", font=("Arial", 18)).place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        
        root.update()  # Обновляем интерфейс, чтобы надпись появилась до начала записи

        recording = sd.rec(
            int(duration * sample_rate), # длительность записи в сэмплах
            samplerate=sample_rate,      # частота дискретизации
            channels=1,                  # 1 — это моно
            dtype="int16")               # формат аудиоданных
        sd.wait()

        wav.write("output.wav", sample_rate, recording)

        recognizer = sr.Recognizer()
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        try:
            text = ""
            text = recognizer.recognize_google(audio, language="en-US")  # распознаём с помощью Google API
        except sr.UnknownValueError:
            text = ""

        if text.lower() == "debugging":
            label = tk.Label(root, text="Ты сказал: " + text, font=("Arial", 18))
            label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
            root.after(2000,cal1l1)
        else:
            label = tk.Label(root, text="Ты сказал: " + text, font=("Arial", 18))
            label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
            root.after(2000,dcal1l1)
    
    if lvl == 5 and location == 5:
        tk.Label(root, text="как будет слово <<куча>>\n на английском?\nговори... у тебя 5 секунд", font=("Arial", 18)).place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        
        root.update()  # Обновляем интерфейс, чтобы надпись появилась до начала записи

        recording = sd.rec(
            int(duration * sample_rate), # длительность записи в сэмплах
            samplerate=sample_rate,      # частота дискретизации
            channels=1,                  # 1 — это моно
            dtype="int16")               # формат аудиоданных
        sd.wait()

        wav.write("output.wav", sample_rate, recording)

        recognizer = sr.Recognizer()
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        try:
            text = ""
            text = recognizer.recognize_google(audio, language="en-US")  # распознаём с помощью Google API
        except sr.UnknownValueError:
            text = ""

        if text.lower() == "heap":
            label = tk.Label(root, text="Ты сказал: " + text, font=("Arial", 18))
            label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
            root.after(2000,cal1l1)
        else:
            label = tk.Label(root, text="Ты сказал: " + text, font=("Arial", 18))
            label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
            root.after(2000,dcal1l1)




def cal1l1():
    global  score, lvl, location
    score += 10

    write_db_data()

    lvl += 1

    if lvl > 5:
        location += 1
        lvl = 1

    Clear()
    tk.Label(root, text="Правильно!", font=("Arial", 18)).place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    root.after(2000,gameMainLoop)

def dcal1l1():
    Clear()
    tk.Label(root, text="Неправильно!", font=("Arial", 18)).place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    root.after(2000,gameMainLoop)
    

start_screen()
root.mainloop()