import os
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import time
import webbrowser
import pyautogui
import difflib
listener = sr.Recognizer()

def talk(text):
    print("Siri:", text)
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[1].id)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print("Speech error:", e)

def take_command():
    command = ""
    try:
        with sr.Microphone() as source:
            print("Listening...")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if "siri" in command:
                command = command.replace("siri", "").strip()
                print("User:", command)
    except:
        pass
    return command

def open_whatsapp_app():
    whatsapp_path = r"C:\Users\Hp\OneDrive\Desktop\WhatsApp.lnk"
    if os.path.exists(whatsapp_path):
        os.startfile(whatsapp_path)
    else:
        print("WhatsApp app not found at the specified path.")

def run_siri():
    command = take_command()
    if not command:
        return

    if "play" in command:
        song = command.replace("play", "")
        talk("Playing " + song)
        pywhatkit.playonyt(song)

    elif "time" in command:
        time_now = datetime.datetime.now().strftime("%I:%M %p")
        talk("The current time is " + time_now)

    elif any(q in command for q in ["search", "who is", "what is"]):
        if "search" in command:
            query = command.replace("search", "")
        elif "who is" in command:
            query = command.replace("who is", "")
        elif "what is" in command:
            query = command.replace("what is", "")
        query = query.strip().replace(".", "")
        print("Searching Wikipedia for:", query)

        try:
            info = wikipedia.summary(query, 2)
            talk(info)
        except wikipedia.exceptions.DisambiguationError:
            talk("That topic is too broad. Please be more specific.")
        except wikipedia.exceptions.PageError:
            talk("Sorry, I couldn't find anything about " + query)
        except Exception as e:
            print("Wikipedia error:", e)
            talk("Something went wrong while searching.")

    elif "date" in command:
        talk("I'm flattered, but I'm just an AI assistant and can't go on dates. But I'm always here to chat!")

    elif "are you single" in command:
        talk("I am in a relationship with WiFi.")

    elif "joke" in command:
        joke = pyjokes.get_joke()
        print("Joke:", joke)
        talk(joke)

    elif "open whatsapp" in command:
        talk("Opening WhatsApp app for you.")
        open_whatsapp_app()


      

    elif "send message" in command:
        try:
            # Step 1: Ask for recipient
            talk("Who do you want to send the message to?")
            recipient = take_command()
            print("Raw recipient input:", repr(recipient))  # DEBUG

            if not recipient:
                talk("I didn't hear the contact name. Please try again.")
                return

            # Step 2: Contact list
            contacts = {
                "sahil singh rajput": "+917301581120"
            }

            # Normalize input
            recipient = recipient.lower().strip()

            # Fuzzy match in case of slight mismatch
            matches = difflib.get_close_matches(recipient, contacts.keys(), n=1, cutoff=0.7)
            print("Closest match:", matches)  # DEBUG

            if not matches:
                talk(f"I don't have {recipient} in your contacts.")
                return

            matched_name = matches[0]
            phone_number = contacts[matched_name]

            # Step 3: Ask for message
            talk(f"What is the message for {matched_name}?")
            message = take_command()
            print("Message captured:", repr(message))  # DEBUG

            if not message:
                talk("I didn't hear the message. Please try again.")
                return

            # Step 4: Send message
            talk(f"Sending message to {matched_name}")
            pywhatkit.sendwhatmsg_instantly(phone_number, message, wait_time=10, tab_close=False)
            time.sleep(20)
            pyautogui.press("enter")
            talk("Message sent!")

        except Exception as e:
            print("Error sending WhatsApp message:", e)
            talk("Sorry, something went wrong while sending the message.")



    elif "open email" in command or "check email" in command:
        talk("Opening your email in browser.")
        webbrowser.open("https://mail.google.com")

    else:
        talk("Sorry, I didn't get that. Please try again.")

while True:
    run_siri()
