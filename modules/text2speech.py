from gtts import gTTS
import vlc
import time
import uuid

def convert_to_speech(text:str,filename)->None:
    tts = gTTS(text)
    tts.save(f'{filename}.mp3')

def play_audio(file:str)->None:
    p = vlc.MediaPlayer(file)
    p.play()
    # p.stop()
    duration = p.get_length() / 1000  # milliseconds → seconds
    if duration <= 0:
        duration = 10  # fallback if duration unknown
    time.sleep(duration)


def ask_question(response):
    question_uuid = uuid.uuid4()
    convert_to_speech(response,question_uuid)
    p = vlc.MediaPlayer(f"{question_uuid}.mp3")
    p.play()
    # p.stop()
    duration = p.get_length()  # in milliseconds
    while duration <= 0:
        duration = p.get_length()  # in milliseconds
        time.sleep(0.1)
        
    time.sleep(duration)

ask_question("Can you describe your experience with designing and deploying Agentic AI systems? Please provide specific examples of projects where you built intelligent agents that performed goal-directed tasks autonomously.")