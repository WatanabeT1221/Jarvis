import speech_recognition as sr
import pyttsx3

import openai
openai.api_key = "OpenAI API Key"

# Initialize the recognizer
r = sr.Recognizer()

# Function to convert text to speech
def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

# Function to record and recognize speech
def record_text():
    try:
        # use the microphone as source for input.
        with sr.Microphone() as source2:
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.2)

            print("I'm listening")

            # listens for the user's input
            audio2 = r.listen(source2)

            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()

            return MyText

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return None

    except sr.UnknownValueError:
        print("Unknown error occurred")
        return None
    
def send_to_chatGPT(messages, model="gpt-3.5-turbo"):

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_token=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choice[0].message.coontent
    messages.append(response.choice[0].message)
    return message

messages = [{"role":"user","content":"Please act like Jarvis from Iron man."}]
while(1):
    text = record_text()
    messages.append({"role":"user","content":text})
    response = send_to_chatGPT(messages)
    SpeakText(response)

    print(response)