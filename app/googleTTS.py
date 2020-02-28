import os
import threading
import logging
from google.cloud import texttospeech
from google.cloud.texttospeech import enums
from sound import SoundThread
import time

class GoogleTSSThread(threading.Thread):
    
    def __init__(self, message, soundFile):
        self.soundFile = soundFile
        self.message = message
        threading.Thread.__init__(self)
    
    def run(self):
        client = texttospeech.TextToSpeechClient()

        synthesisInput = texttospeech.types.SynthesisInput(text=self.message)

        voice = texttospeech.types.VoiceSelectionParams(language_code="en-us", name="en-GB-Wavenet-A")

        audioConfig = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3,
            speaking_rate=0.85)

        response = client.synthesize_speech(synthesisInput, voice, audioConfig)

        basedir = os.path.abspath(os.path.dirname(__file__))

        fileName = basedir + "/tmp/google_tts.mp3"
        with open(fileName, 'wb') as out:
            out.write(response.audio_content)
            logging.info("audio content written to file " + fileName)

            SoundThread(self.soundFile).start()
            time.sleep(0.5)
            os.system("omxplayer " + fileName)