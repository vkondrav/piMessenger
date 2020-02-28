import os
import threading
from google.cloud import texttospeech
from google.cloud.texttospeech import enums
import logging

class SoundThread(threading.Thread):
	
	basedir = os.path.abspath(os.path.dirname(__file__))
	
	def __init__(self, soundFileName):
		self.soundPath = self.basedir + "/" + soundFileName
		threading.Thread.__init__(self)
	
	def run(self):
		logging.info("playing sound file " + self.soundPath)
		os.system("omxplayer " + self.soundPath)