import speech_recognition as sr
from heart import display_heart_red, display_heart_blue, turn_off, heart
import time

r = sr.Recognizer()

def recognize_speech():
    with sr.Microphone() as source:
        print("Say something...")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print("You said: " + command)
        return command
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return ""
    except sr.RequestError as e:
        print(f"Could not get results; {e}")
        return ""

if __name__ == "__main__":
    print("Starting speech recognition...")
    while True:
        command = recognize_speech()
        if 'red heart' in command:
            print("Command recognized: red heart")
            while True:
                display_heart_red(heart)
        elif 'blue heart' in command:
            print("Command recognized: blue heart")
            display_heart_blue(heart)
        elif 'turn off' in command:
            print("Command recognized: turn off")
            turn_off()
        elif 'exit' in command:
            print("Exiting...")
            break
        #time.sleep(1)  # Sleep for a short duration before the next iteration
    print("Script ended.")
