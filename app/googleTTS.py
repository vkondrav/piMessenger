import os
import threading
import logging
from google.cloud import texttospeech
from google.cloud.texttospeech import enums

class GoogleTSSThread(threading.Thread):
    
    def __init__(self, message):
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
            logging.info("Audio content written to file " + fileName)
            os.system("omxplayer " + fileName)