import os
import threading
import time
import requests
from speech import SpeechThread
from sound import SoundThread

class TransitThread(threading.Thread):
	def __init__(self, delay, route, stop, soundFile):
		self.delay = delay
		self.route = route
		self.stop = stop
		self.soundFile = soundFile
		threading.Thread.__init__(self)

	def predict(self, url):
		formatted = {}
		r = requests.get(url)

		if(r.status_code != 200):
			return
			
		json = r.json()
		if "predictions" not in json:
			return
		p = json["predictions"]

		title = p["routeTitle"]
		if "direction" not in p:
			return

		direction = p["direction"]

		if "prediction" not in direction:
			return
		
		prediction = direction["prediction"]

		if len(prediction) <= 0:
			return
		
		current = prediction[0]

		if "minutes" not in current:
			return
		
		minutes = current["minutes"]

		message = title + " arriving in " + minutes + " minutes"

		print (message)

		if(int(minutes) > 15):
			return

		SoundThread(self.soundFile).start()
		SpeechThread(message).start()

	def run(self):
		starttime = time.time()
		url = "http://webservices.nextbus.com/service/publicJSONFeed?command=predictions&a=ttc&r=" + str(self.route) + "&s=" + str(self.stop)
		while True:
			self.predict(url)
			time.sleep(self.delay - ((time.time() - starttime) % self.delay))