import os
import threading

class SoundThread(threading.Thread):
	
	basedir = os.path.abspath(os.path.dirname(__file__))
	
	def __init__(self, soundFileName):
		self.soundPath = self.basedir + "/" + soundFileName
		threading.Thread.__init__(self)
	
	def run(self):
		os.system("omxplayer " + self.soundPath)