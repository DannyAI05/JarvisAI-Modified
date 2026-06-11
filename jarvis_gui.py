import random
import speech_recognition as sr
from datetime import datetime
from playsound import playsound
import time
import asyncio
import edge_tts
import os
import sys
import math
import webbrowser
import psutil
import platform
import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox
from  PIL import Image , ImageTk
import threading
import requests

def show_about():

    messagebox.showinfo(
        "About JarvisAI",
        "JarvisAI\nVersion 1.0\nCreated by Daniela Wakhu"
    )

print(os.getcwd())


def get_weather(city):

    API_KEY = "9bf9b1d02371cd843effd1405ce6e199"

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}"
        f"&appid={API_KEY}"
        f"&units=metric"
    )

    response = requests.get(url)

    data = response.json()

    return {
        "temp": round(data["main"]["temp"]),
        "description": data["weather"][0]["description"],
        "condition": data["weather"][0]["main"]
    }

def update_clock():

    current_time = datetime.now().strftime(
        "%d %B %Y | %I:%M:%S %p"
    )

    clock_label.config(text=current_time)

    root.after(1000, update_clock)

def send_message():

    message = user_entry.get("1.0", tk.END).strip()

    if not message:
        return
    
    chat_area.insert(
        tk.END,
        f"You: {message}\n"
    )

    response = chatbot_response(
        message,
        "Daniela"
    )

    chat_area.insert(
        tk.END,
        f"JarvisAI: {response}\n\n"
    )

    speak(response)

    user_entry.delete("1.0", tk.END)

def clear_chat():

    chat_area.delete(
        "1.0",
        tk.END
    )

    chat_area.insert(
        tk.END,
        "JarvisAI: Chat cleared.\n\n"
    )
    
def get_greeting():

    current_hour = datetime.now().hour

    if current_hour < 12:
        return "Good morning"

    elif current_hour < 18:
        return "Good afternoon"

    else:
        return "Good evening"

def speak(text):
    print("JarvisAI:", text)

    filename = f"jarvis_{int(time.time() * 1000)}.mp3"

    async def generate_voice():
        communicate = edge_tts.Communicate(
            str(text),
            "en-US-JennyNeural"
        )
        await communicate.save(filename)

    asyncio.run(generate_voice())

    playsound(filename)

    try:
        os.remove(filename)
    except:
        pass

def blink_status():
    current = status_label.cget("fg")
    new_color = "lightgreen" if current == "#00ffcc" else "#00ffcc"
    status_label.config(fg=new_color)
    root.after(800, blink_status)

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("Heard:", text)
        return text

    except sr.UnknownValueError:
        return "Sorry, I didn't catch that"
    except sr.RequestError:
        return "Speech service error"


# MEMORY SYSTEM
memory = {
    "favorite_color": None,
    "favorite_food":None,
    "favorite_movie":None,
    "age":None,
    "school":None,
    "brother":None,
    "mother":None
    
}


# RANDOM RESPONSES
jokes = [
    "Why did the programmer quit his job? Because he didn't get arrays.",
    "Why do Java developers wear glasses? Because they can't C sharp.",
    "Debugging is like being the detective in a crime movie where you are also the murderer.",
    "A SQL query walks into a bar, walks up to two tables and asks: Can I join you?"
]

greetings = [
    "Hey there",
    "Hello",
    "Hi, nice to see you",
    "Yo what's up"
]



def chatbot_response(user_input, user_name):
    user_input = user_input.lower()

    if user_input in ["hello", "hi", "hey"]:
        return f"{random.choice(greetings)} {user_name}!"

    elif "how are you" in user_input:
        return "I'm feeling fantastic and fully charged!"

    elif "your name" in user_input:
        return "I'm JarvisAI, created by Wakhu. Nice to meet you!"

    elif "time" in user_input:
        current_time = datetime.now().strftime("%I:%M:%S %p")
        return f"The current time is {current_time}"

    elif "date" in user_input:
        current_date = datetime.now().strftime("%d %B %Y")
        return f"Today's date is {current_date}"

    elif "joke" in user_input:
        return random.choice(jokes)

    elif "help" in user_input:
        return (
            "I can chat, tell jokes, remember your favorite color, "
            "tell the date and time, and respond to voice commands."
        )
    elif "weather" in user_input:
        weather = get_weather(city)

        return (
                f"The temperature in {city} is "
                f"{weather['temp']} degrees Celsius with "
                f"{weather['description']}."
         )
        
#BATTERY CHARGING
    elif "battery" in user_input:

        battery = psutil.sensors_battery()

        if battery:

            if battery.power_plugged:
                   return f"Battery is at {battery.percent} percent and is currently charging."

            else:
                   return f"Battery is at {battery.percent} percent and is not charging."

        return "I cannot detect a battery on this device."

#SYSTEM INFORMATION
    elif "system information" in user_input:
        return (
            f"Operating System: {platform.system()}"
            f"{platform.release()}"
            )

#MEMORY
    elif user_input.startswith("my favorite color is"):
        color = user_input.replace("my favorite color is", "").strip()
        memory["favorite_color"] = color
        return f"Awesome! I'll remember that your favorite color is {color}."

    elif "what is my favorite color" in user_input:
        if memory["favorite_color"]:
            return f"Your favorite color is {memory['favorite_color']}."
        else:
            return "You haven't told me your favorite color yet."

    elif user_input.startswith("my favorite food is"): #My favorite food is chicken
        food = user_input.replace("my favorite food is", "").strip()
        memory["favorite_food"] = food
        return f"Awesome! I'll remember that your favorite food is {food}."

    elif "what is my favorite food" in user_input:
        if memory["favorite_food"]:
            return f"Your favorite food is {memory['favorite_food']}."
        else:
            return "You haven't told me your favorite food yet."
        
    elif user_input.startswith("my favorite movie is"):#My favorite movie is Mission Impossible
        movie = user_input.replace("my favorite movie is", "").strip()
        memory["favorite_movie"] = movie
        return f"Awesome! I'll remember that your favorite movie is {movie}."

    elif "what is my favorite movie" in user_input:
        if memory["favorite_movie"]:
            return f"Your favorite movie is {memory['favorite_movie']}."
        else:
            return "You haven't told me your favorite movie yet."

#Open apps
    elif "open notepad" in user_input:
        os.system("notepad")
        return "Opening Notepad."
    
    elif "open file_explorer" in user_input:
        os.system("explorer")
        return "Opening File Explorer."
    
    elif "open chrome" in user_input:
        webbrowser.open("https://www.google.com")
        return "Opening Chrome."

    elif "open microsoft_edge" in user_input:
        os.system("start msedge")
        return "Opening Microsoft Edge."

    elif "open whatsapp" in user_input:
        webbrowser.open("https://web.whatsapp.com")
        return "Opening Whatsapp."

#Search web
    elif user_input.startswith("search "):
        query = user_input.replace("search ", "")
        webbrowser.open(
               f"https://www.google.com/search?q={query}"
        )
        return f"Searching for {query}."

#Take note
    elif user_input.startswith("take note"):
        note = user_input.replace("take note", "").strip()

        with open("notes.txt", "a") as file:
             file.write(note + "\n")

        return "Note saved."

#Calculate
    elif user_input.startswith("calculate"):

        expression = user_input.replace(
        "calculate",
        ""
        ).strip()

        try:
            answer = eval(expression)
            return f"The answer is {answer}"
        except:
            return "Invalid calculation."

#Play music
    elif "play music" in user_input:
        webbrowser.open(
            "https://music.youtube.com"
            )
        return "Opening music."

#Show notes    
    elif "show notes" in user_input:
        try:
            with open("notes.txt","r") as file:
                notes = file.read()

            return notes if notes else "No notes found."

        except FileNotFoundError:
            return "No notes found."

#Clear notes
    elif "clear notes" in user_input:
        open("notes.txt","w").close()
        return "All notes have been cleared."
            

    elif "goodbye jarvis" in user_input:
        return f"Goodbye {user_name}, talk to you later!"

    else:
        return "Hmmm...I'm not sure about that. Could you rephrase your question?"


def voice_input():

    message = listen()

    if not message:
        return

    chat_area.insert(
        tk.END,
        f"You: {message}\n"
    )

    response = chatbot_response(
        message,
        "Daniela"
    )

    chat_area.insert(
        tk.END,
        f"JarvisAI: {response}\n\n"
    )

    speak(response)

    chat_area.see(tk.END)

wake_word = "jarvis"

def listen_for_wake_word():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Listening for wake word...")

        while True:
            audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio).lower()
                print("Heard:", text)

                if wake_word in text:
                    print("Wake word detected!")
                    return True

            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("Speech service error")


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def play_startup_sound():
    playsound(
        resource_path("startup.mp3")
     )
threading.Thread(target=play_startup_sound, daemon=True).start()

def start_jarvis():
    # play sound
    threading.Thread(target=play_startup_sound, daemon=True).start()

    # wait for wake word
    listen_for_wake_word()

    # now activate chatbot / voice command system
    print("Jarvis activated!")
          
def create_button(text, command, color):

    return tk.Button(
        button_container,
        text=text,
        command=command,
        bg=color,
        fg="white",
        font=("Arial", 10, "bold"),
        bd=0,
        relief="flat",
        pady=8
    )

boot_messages = [
    "Initializing JARVIS...",
    "Loading voice modules...",
    "Loading AI core...",
    "Loading interface systems...",
    "Establishing secure connection...",
    "System Online."
]

def boot_sequence(index=0):
    if index < len(boot_messages):
        chat_area.insert(
            tk.END,
            boot_messages[index] + "\n"
        )

        chat_area.see(tk.END)

        root.after(
            800,
            lambda: boot_sequence(index + 1)
        )

def animate_processing():
    frames = [
        "Processing.",
        "Processing..",
        "Processing..."
    ]

    for frame in frames:
        status_label.config(text=frame)
        root.update()
        time.sleep(0.3)

    status_label.config(text="🟢 Online")

def set_theme(theme):

    if theme == "dark":

        root.configure(bg="#1e1e1e")

        left_panel.config(bg="#121212")
        right_panel.config(bg="#1e1e1e")

        chat_area.config(
            bg="#0d0d0d",
            fg="#00ffcc",
            insertbackground="#00ffcc"
        )

        user_entry.config(
            bg="#111111",
            fg="#00ffcc",
            insertbackground="#00ffcc"
        )

    elif theme == "light":

        root.configure(bg="white")

        left_panel.config(bg="#dddddd")
        right_panel.config(bg="#f5f5f5")

        chat_area.config(
            bg="white",
            fg="black",
            insertbackground="black"
        )

        user_entry.config(
            bg="white",
            fg="black",
            insertbackground="black"
        )

    elif theme == "cyber":

        root.configure(bg="black")

        left_panel.config(bg="#050505")
        right_panel.config(bg="black")

        chat_area.config(
            bg="black",
            fg="#00ff00",
            insertbackground="#00ff00"
        )

        user_entry.config(
            bg="#101010",
            fg="#00ff00",
            insertbackground="#00ff00"
        )
    
root = tk.Tk()
root.configure(bg="#1e1e1e")

root.title("JarvisAI")
root.geometry("1000x1000")

root.iconbitmap("jarvis_icon.ico")

image = Image.open(
    resource_path("jarvis_logo.png")
)

image = image.resize((100, 100))

logo = ImageTk.PhotoImage(image)


main_frame = tk.Frame(root, bg="#1e1e1e")
main_frame.pack(fill="both", expand=True)

left_panel = tk.Frame(
    main_frame,
    bg="#121212",
    width=200
)

left_panel.pack(
    side=tk.LEFT,
    fill=tk.Y
)

right_panel = tk.Frame(
    main_frame,
    bg="#1e1e1e"
)

right_panel.pack(
    side=tk.RIGHT,
    fill=tk.BOTH,
    expand=True
)

header_frame = tk.Frame(right_panel, bg="#1e1e1e")
header_frame.pack(fill="x")

logo_label = tk.Label(
    right_panel,
    image=logo,
    bg="#1e1e1e"

)

logo_label.pack(pady=5)

status_label = tk.Label(
    right_panel,
    text="🟢 Online",
    font=("Arial", 10),
    bg="#1e1e1e",
    fg="lightgreen"
)

status_label.pack()

clock_label = tk.Label(
    right_panel,
    font=("Arial", 10),
    bg="#1e1e1e",
    fg="white"
)

clock_label.pack(pady=5)

title_label = tk.Label(
    right_panel,
    text="JarvisAI Assistant",
    font=("Arial", 18, "bold"),
    bg="#1e1e1e",
    fg="white"
)
title_label.pack(pady=10)

title_label.config(
    bg="#1e1e1e",
    fg="white"
)

status_label.config(
    bg="#1e1e1e"
)

clock_label.config(
    bg="#1e1e1e",
    fg="white"
)

scrollbar = tk.Scrollbar(right_panel)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

chat_area = tk.Text(
    right_panel,
    height=25,
    width=70,
    bg="#0d0d0d",
    fg="#00ffcc",
    insertbackground="#00ffcc",
    font=("Consolas", 11),
    yscrollcommand=scrollbar.set,
    bd=0
)
scrollbar.config(command=chat_area.yview)

chat_area.config(
    bg="black",
    fg="#00ff00"
)

def update_weather(city):

    data = get_weather(city)

    condition = data["condition"]

    if condition == "Clear":
        weather_icon.config(
            text="☀️",
            fg="yellow"
         )

    elif condition == "Clouds":
         weather_icon.config(
             text="☁️",
             fg="lightgray"
        )

    elif condition == "Rain":
        weather_icon.config(
             text="🌧️",
             fg="cyan"
       )

    elif condition == "Thunderstorm":
         weather_icon.config(
              text="⛈️",
              fg="yellow"
       )

    elif condition == "Snow":
          weather_icon.config(
                text="❄️",
                fg="white"
       )

    if condition == "Rain":

       weather_icon.config(
            text="🌧️",
            fg="cyan"
       )

       setup_rain()

       animate_rain()

    elif condition == "Clear":

        weather_canvas.delete("all")

        weather_icon.config(
              text="☀️",
              fg="yellow"
      )

    weather_temp.config(
        text=f"{data['temp']}°C"
    )

    weather_desc.config(
        text=data['description']
    )

def refresh_weather():

    update_weather("Nairobi")

    root.after(
        600000,
        refresh_weather
    )


#Radar scanner
canvas = tk.Canvas(
    left_panel,
    width=140,
    height=140,
    bg="#121212",
    highlightthickness=0
)

canvas.pack(pady=20)

wave_canvas = tk.Canvas(
    left_panel,
    width=140,
    height=60,
    bg="#121212",
    highlightthickness=0
)

wave_canvas.pack(pady=10)


weather_frame = tk.Frame(
    left_panel,
    bg="#1a1a1a",
    bd=5
)

weather_frame.pack(
    fill="x",
    padx=10,
    pady=10
)

weather_icon = tk.Label(
    weather_frame,
    text="☀️",
    font=("Arial", 20),
    bg="#1a1a1a",
    fg="yellow"
)

weather_icon.pack()

weather_temp = tk.Label(
    weather_frame,
    text="--°C",
    font=("Arial", 16, "bold"),
    bg="#1a1a1a",
    fg="cyan"
)

weather_temp.pack()

weather_desc = tk.Label(
    weather_frame,
    text="Loading...",
    bg="#1a1a1a",
    fg="white"
)

weather_desc.pack()

weather_canvas = tk.Canvas(
    weather_frame,
    width=120,
    height=40,
    bg="#1a1a1a",
    highlightthickness=0
)

weather_canvas.pack()

tk.Label(left_panel, text="JARVIS", fg="cyan", bg="#121212",
         font=("Arial", 14, "bold")).pack(pady=20)


def update_system_monitor():
    cpu_usage = psutil.cpu_percent(interval=None)
    memory = psutil.virtual_memory()

    used_ram = memory.used / (1024 ** 3)
    total_ram = memory.total / (1024 ** 3)

    ram_label.config(
            text=f"RAM: {used_ram:.1f} / {total_ram:.1f} GB"
     )

    cpu_color = "cyan"
    ram_color = "yellow"

    cpu_label.config(
        text=f"CPU: {cpu_usage}%",
        fg=cpu_color
    )

    ram_label.config(
        text=f"RAM: {used_ram:.1f}/{total_ram:.1f}GB",
        fg=ram_color
    )

    root.after(1000, update_system_monitor)

cpu_label = tk.Label(
    left_panel,
    text="CPU: 0%",
    fg="cyan",
    bg="#121212",
    font=("Arial", 10)
)

cpu_label.pack(pady=2)

ram_label = tk.Label(
    left_panel,
    text="RAM: 0%",
    fg="cyan",
    bg="#121212",
    font=("Arial", 10)
)

ram_label.pack(pady=2)

button_container = tk.Frame(
    left_panel,
    bg="#121212"
)

button_container.pack(
    fill="x",
    padx=10,
    pady=10
)

create_button(
    "Speak",
    voice_input,
    "#1f6aa5"
).pack(fill="x", pady=5)


create_button(
    "Send",
    send_message,
    "#333333"
).pack(fill="x", pady=5)


create_button(
    "Clear",
    clear_chat,
    "#888888"
).pack(fill="x", pady=5)


create_button(
    "About",
    show_about,
    "#006600"
).pack(fill="x", pady=5)


angle = 0

def radar():
    global angle

    canvas.delete("sweep")

    x = 90
    y = 90
    r = 80

    x2 = x + r * math.cos(math.radians(angle))
    y2 = y + r * math.sin(math.radians(angle))

    canvas.create_line(
        x, y,
        x2, y2,
        fill="cyan",
        width=2,
        tags="sweep"
    )

    angle += 5

    root.after(50, radar)

canvas.create_oval(
    10, 10, 170, 170,
    outline="cyan"
)

canvas.create_oval(
    40, 40, 140, 140,
    outline="cyan"
)

canvas.create_line(
    90, 10,
    90, 170,
    fill="cyan"
)

canvas.create_line(
    10, 90,
    170, 90,
    fill="cyan"
)

chat_area.insert(
    tk.END,
    "JarvisAI: System online and ready.\n\n"
    )

chat_area.see(tk.END)

chat_area.tag_config("Daniela", foreground="#ffffff")
chat_area.tag_config("jarvis", foreground="#00ffcc")

input_frame = tk.Frame(right_panel, bg="#1e1e1e")
input_frame.pack(side=tk.TOP, fill=tk.X)

user_entry = tk.Text(
    input_frame,
    height = 1,
    bg="#111111",
    fg="#00ffcc",
    insertbackground="#00ffcc",
    font=("Consolas", 12),
    bd=0
)
user_entry.pack(fill=tk.X, padx=10, pady=5)

user_entry.focus_set()

chat_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

def send_on_enter(event):
    send_message()
    return "break"

user_entry.bind("<Return>", send_on_enter)

bars = []

for i in range(20):
    bar = canvas.create_rectangle(
        10 + i*8,
        50,
        15 + i*8,
        100,
        fill="cyan"
    )
    bars.append(bar)

def listen_forever():
    recognizer = sr.Recognizer()

    while True:
        with sr.Microphone() as source:

            recognizer.adjust_for_ambient_noise(source)

            audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio)

                if "jarvis" in text.lower():

                    command = text.lower().replace(
                        "jarvis",
                        ""
                    )

                    response = process_command(command)

                    asyncio.run(
                        speak(response)
                    )

            except:
                pass

threading.Thread(
    target=listen_forever,
    daemon=True
).start()

def exit_fullscreen(event=None):
    global fullscreen

    fullscreen = False

    root.attributes(
        "-fullscreen",
        False
    )

root.bind(
    "<Escape>",
    exit_fullscreen
)

rain_drops = []

def setup_rain():

    global rain_drops

    weather_canvas.delete("all")

    rain_drops = []

    for _ in range(20):

        x = random.randint(0, 160)

        drop = weather_canvas.create_line(
            x,
            0,
            x,
            10,
            fill="cyan"
        )

        rain_drops.append(drop)

def animate_rain():

    for drop in rain_drops:

        weather_canvas.move(drop, 0, 5)

        coords = weather_canvas.coords(drop)

        if coords[1] > 80:

            x = random.randint(0, 160)

            weather_canvas.coords(
                drop,
                x, 0,
                x, 10
            )

    root.after(50, animate_rain)

update_system_monitor()

radar()

animate_processing()

boot_sequence()

refresh_weather()

update_clock()

root.mainloop()
