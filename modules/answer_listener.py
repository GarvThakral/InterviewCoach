import webrtcvad
from scipy.io import wavfile
   
samplerate, data = wavfile.read('./modules/hello.mp3')

vad = webrtcvad.Vad(2)
print('Contains speech: %s' % (vad.is_speech(data, samplerate)))