import os
import threading
import time

class SpeechThread(threading.Thread):
	
	basedir = os.path.abspath(os.path.dirname(__file__))
	
	def __init__(self, text, command_path= basedir + "/speech"):
		self.text = text
		self.command_path = command_path
		threading.Thread.__init__(self)
	
	def run(self):
		os.system(self.command_path + " \"" + self.text + "\"")
		
class ShutterThread(threading.Thread):
	
	basedir = os.path.abspath(os.path.dirname(__file__))
	
	def __init__(self, shutterFilePath= basedir + "/camera-shutter.wav"):
		self.shutterFilePath = shutterFilePath
		threading.Thread.__init__(self)
	
	def run(self):
		os.system("omxplayer " + self.shutterFilePath)

class DelugeThread(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		os.system("sudo pkill deluged")
		time.sleep(5)
		os.system("deluged")

