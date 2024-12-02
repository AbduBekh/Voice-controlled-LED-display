import spidev
import warnings
import speech_recognition as sr
from speech_recognition.recognizers import google

from datetime import date
from time import sleep

import threading
from globals import stop_flag, running  # Import the stop_flag
from heart import cyan
from goodbye import clear_matrix
from goodbye import exit_program
from heartRainbow import heartColors
from rainbow import rainbow
from smile import smile
from square import square
from digitDisplay import timeDisplay
from digitDisplay import dateDisplay
from digitDisplay import countdown
from digitDisplay import parse_timer
from TemperatureDisplay import tempDisplay
from weatherDisplay import displayForcast

warnings.filterwarnings("ignore")
# Initialize speech recognition
r = sr.Recognizer()
mic = sr.Microphone()

def choose_language():
    with mic as source:
        print("Please say 'English' or 'Hungarian' to choose your language:")
        audio = r.listen(source)
    try:
        language_choice = r.recognize_google(audio, language="en-US").lower()
        if "hungarian" in language_choice or "magyar" in language_choice:
            print("Hungarian selected.")
            print()
            return "hu-HU"
        elif "english" in language_choice:
            print("English selected.")
            print()
            return "en-US"
        else:
            print("Language not recognized, defaulting to English.")
            return "en-US"
    except sr.UnknownValueError:
        print("Could not understand the language choice, defaulting to English.")
        return "en-US"
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return "en-US"



def execute_command(command):
	if command in COMMAND_MAP:
		COMMAND_MAP[command]()
	else:
		print("Command not recognized, please try again.")
        
# Define a command map
COMMAND_MAP = {
	"countdown": countdown,
	"visszaszámlálás": countdown,
	"time": timeDisplay,
	"idő": timeDisplay,
	"date": dateDisplay,
	"dátum": dateDisplay,
	"temperature": tempDisplay,
	"hőmérséklet": tempDisplay,
	"weather": displayForcast,
	"előrejelzés": displayForcast,
    "blue heart": cyan,  
    "kék szív": cyan,
    "colourful heart": heartColors,
    "színes szív": heartColors,
    "rainbow": rainbow,
    "szivárvány": rainbow,
    "smile": smile,
    "mosoly": smile,
    "square": square,
    "négyzet": square,
    "clear": exit_program,
    "törlés": exit_program
}

chosen_language = choose_language()
active_thread = None
        
while running:
	with mic as source:
		print(f"Running flag status: {running}")
		print("Say something:")
		print()
		audio = r.listen(source, timeout=20)
	try:
		words = r.recognize_google(audio, language=chosen_language).lower()
		print()
		print(f"You said: {words}")
		print()
		
		if "exit" in words or "kijárat" in words:
			exit_program()
			break 
			
		if "countdown" in words or "timer" in words:
			minutes, seconds = parse_timer(words)
			if active_thread and active_thread.is_alive():
				stop_flag.set()
				active_thread.join()
				stop_flag.clear()
			clear_matrix()
			active_thread = threading.Thread(target=countdown, args=(minutes, seconds))
			active_thread.start()
			continue

		for command in COMMAND_MAP:
			if command in words:
				print(f"Command detected: {command}")
				if active_thread and active_thread.is_alive():
					stop_flag.set()
					active_thread.join()
					stop_flag.clear()
				clear_matrix()
				active_thread = threading.Thread(target= execute_command, args=(command,))
				active_thread.start()
				#execute_command(command)
				break
		
		
		
		
	except sr.UnknownValueError:
		print("Sorry, I could not understand the audio.")
	except sr.RequestError as e:
		print(f"Could not request results from Google Speech Recognition service; {e}")
