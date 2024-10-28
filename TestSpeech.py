from speech_recognition.recognizers import google
import speech_recognition as sr
from heart import display_heart_red, display_heart_blue, turn_off, heart

r = sr.Recognizer()
with sr.Microphone() as source:
	print("Say something")
	audio = r.listen(source)
	
try:
	words = r.recognize_google(audio).lower()
	print("you said: " + words)
	if "red" in words:
		while True:
			display_heart_red(heart)
			
	
except sr.UnkownValueError:
	print("nope")
except sr.RequestError as e:
	print("could not get results {0}".format(e))
