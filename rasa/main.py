import speech_recognition as sr
import asyncio
import pprint as pretty_print
import typing
from typing import Any, Dict, Text, Optional
from rasa.cli.utils import print_success, print_error
from rasa.core.interpreter import NaturalLanguageInterpreter, RasaNLUInterpreter
import rasa.model as model
from rasa.run import create_agent


model_path = 'model'
agent = create_agent(model_path)

loop = asyncio.get_event_loop()

while True:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('say something')
        audio = r.listen(source)
    res = r.recognize_google(audio)
    print(res)

    message = res

    if message == "/stop":
        break

    responses = loop.run_until_complete(agent.handle_text(message))
    for response in responses:
        print(str(response) + '\n')
