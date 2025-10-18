import pyaudio
import subprocess
import os
import json
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
# Initialize the Groq client
client = Groq()


def speech2text(audio_filename:str)->str:

    with open("./modules/hello.mp3", "rb") as file:
        # Create a transcription of the audio file
        transcription = client.audio.transcriptions.create(
        file=file, # Required audio file
        model="whisper-large-v3-turbo", # Required model to use for transcription
        prompt="Specify context or spelling",  # Optional
        response_format="verbose_json",  # Optional
        timestamp_granularities = ["word", "segment"], # Optional (must set response_format to "json" to use and can specify "word", "segment" (default), or both)
        language="en",  # Optional
        temperature=0.0  # Optional
        )
        # To print only the transcription text, you'd use print(transcription.text) (here we're printing the entire transcription object to access timestamps)
        text = transcription.to_dict()['text']
        # print(text)
        return text
    
# text = speech2text('./modules/hello.mp3')
# print(text)

def record_answer():

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 10

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open stream
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    # Start the MP3 encoder (lame) with stdin connected to the pipe
    lame_process = subprocess.Popen(['lame', '-', '-r', '-m', 'm', 'output.mp3'], stdin=subprocess.PIPE)

    # Record and pipe data
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        lame_process.stdin.write(data)

    # Close the pipe and wait for encoding to finish
    lame_process.stdin.close()
    lame_process.wait()

    # Clean up
    stream.stop_stream()
    stream.close()
    audio.terminate()
record_answer()