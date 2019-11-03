import speech_recognition as sr
r= sr.Recognizer()

with sr.Microphone() as source:
    print('say something')
    audio = r.listen(source)
res = r.recognize_google(audio)
print('u said "' + res + '"')
