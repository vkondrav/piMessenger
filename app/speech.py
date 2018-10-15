import os
import threading

class SpeechThread(threading.Thread):
	def __init__(self, text, command_path="speech"):
		self.text = text
		self.command_path = command_path
		threading.Thread.__init__(self)
	
	def run(self):
		os.system("./" + self.command_path + " \"" + self.text + "\"")
