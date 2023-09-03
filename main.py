import pyttsx3
import speech_recognition as sr
from PyCharacterAI import Client
import asyncio


# Creating the speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) #0 - male, 1 - female

keyword = 'character'

# Set up the voice engine
def voice(text, rate=130):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

def parse():
    listener = sr.Recognizer()
    print('Waiting for response...')

    with sr.Microphone() as mic:
        listener.pause_threshold = 2
        inp = listener.listen(mic)

    try:
        print('Registering speech...')
        query = listener.recognize_google(inp, language='en_gb')
        print(f'Interpreted as: {query}')
    except Exception as exception:
        print("I did not quite catch that")

        voice("I did not quite catch that")
        print(exception)
        return 'None'
    return query

char_id = '' # character id
access_token = '' # access token

async def main():

    ############### Main Setup ##################
    client = Client()
    await client.authenticate_with_token(access_token)

    # get the username
    username = (await client.fetch_user())['user']['username']
    print(f"Logged in as: {username}")

    chat = await client.create_or_continue_chat(char_id)
    char_info = await client.fetch_character_info(char_id)

    char_name = char_info['name']

    ###############################################
    voice("Welcome")

    while True:
        message = parse()

        if message.split(' ')[0] == keyword:
            new_msg = message.split(' ')
            new_msg.pop(0)
            resp = await chat.send_message(" ".join(new_msg))

            voice(f'{char_name} says: {resp}')
            print('')
            print(resp)


asyncio.run(main())

