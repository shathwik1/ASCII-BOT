import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import datetime
import os
import time

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("voice", pyttsx3.init().getProperty("voices")[28].id)
engine.setProperty("rate", 150)
engine.setProperty("volume", 1)

# Speak function


def speak(text):
    engine.say(text)
    engine.runAndWait()

# Greeting function


def wish_me():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am ASCII. How may I assist you?")

# Recognize speech input


def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}\n")
            return text.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError:
            print("Could not request results; check your connection.")
        except sr.WaitTimeoutError:
            print("No speech detected.")
        return ""

# Wikipedia summary function


def wikipedia_summary(query):
    speak("Searching Wikipedia...")
    try:
        summary = wikipedia.summary(query.replace(
            "wikipedia", "").strip(), sentences=2)
        print(summary)
        speak(f"According to Wikipedia, {summary}")
    except wikipedia.exceptions.DisambiguationError as e:
        speak("The query is too ambiguous. Please specify further.")
        print(f"Disambiguation Error: {e.options}")
    except wikipedia.exceptions.PageError:
        speak("Sorry, no matching page was found.")
        print("The page does not exist.")

# Power calculation function


def power(base, exponent):
    return base ** exponent if exponent >= 0 else 1 / (base ** abs(exponent))

# Calculator function


def calculator():
    try:
        speak("Enter the first number")
        num1 = float(input("Enter the first number: "))
        speak("Enter the second number")
        num2 = float(input("Enter the second number: "))
        speak("Enter the operation you want to perform (+, -, *, /, **)")
        operation = input("Enter the operation: ")
        operations = {
            '+': num1 + num2,
            '-': num1 - num2,
            '*': num1 * num2,
            '/': num1 / num2 if num2 != 0 else "undefined (division by zero)",
            '**': power(num1, num2)
        }
        if operation in operations:
            result = operations[operation]
            speak(f"The result is {result}")
            print(f"The result of {num1} {operation} {num2} = {result}")
        else:
            speak("Invalid operation. Supported operations are +, -, *, /, **")
    except ValueError:
        speak("Invalid input. Please enter numeric values.")

# Main function


def main():
    while True:
        query = recognize_speech()
        if not query:
            continue
        if "exit" in query:
            speak("Goodbye!")
            break
        elif "time" in query:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {current_time}")
            print(f"The time is {current_time}")
        elif "open file" in query:
            speak("What is the file path?")
            file_path = input("Enter the file path: ")
            if os.path.exists(file_path):
                os.startfile(file_path)
            else:
                speak("File not found.")
                print("File not found.")
        elif "open" in query:
            website = query.replace("open ", "").strip()
            speak(f"Opening {website}")
            time.sleep(0.9)
            webbrowser.open(f"https://{website}.com")
        elif "google" in query:
            search_term = query.replace("google ", "").strip()
            speak(f"Searching {search_term} on Google")

            webbrowser.open(f"https://www.google.com/search?q={search_term}")
        elif "wikipedia" in query:
            wikipedia_summary(query)
        elif "calculate" in query:
            calculator()


# Main program
if __name__ == "__main__":
    wish_me()
    time.sleep(3.2)
    main()
