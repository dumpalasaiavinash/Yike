import pyaudio
import numpy as np

CHUNK = 2**11
RATE = 44100

p=pyaudio.PyAudio()

stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK)

a= float(1000)
b= 30

for i in range(int(10000)): #go for a few seconds
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    peak=np.average(np.abs(data))*2
    bars="#"*int(50*peak/2**16)

    print("%04d %05d %s"%(i,peak,bars))
    if ( i > b) :
        if peak < a:
            stream.stop_stream()
            stream.close()
            p.terminate()


print(type(peak))
stream.stop_stream()
stream.close()
p.terminate()
