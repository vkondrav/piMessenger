import os
import threading
import time
import requests
from datetime import datetime
from pytz import timezone
from speech import SpeechThread
from sound import SoundThread

class TransitThread(threading.Thread):

	def __init__(self, config, soundFile):
		self.timezone = timezone(config["timezone"])
		self.pollRate = config["poll_rate"]
		self.route = config["route"]
		self.stop = config["stop"]
		self.minTime = config["minTime"]
		self.maxTime = config["maxTime"]
		self.limit = config["limit"]
		self.weekdays = config["weekdays"]
		self.soundFile = soundFile
		threading.Thread.__init__(self)

	def clock(self):
		return datetime.now(self.timezone).strftime("%I:%M%p")

	def predict(self, url):
		print (url)

		r = requests.get(url)

		if(r.status_code != 200):
			return None
			
		json = r.json()
		if "predictions" not in json:
			return None

		p = json["predictions"]
		title = p["routeTitle"]
		if "direction" not in p:
			return None

		direction = p["direction"]

		if "prediction" not in direction:
			return None
		
		prediction = direction["prediction"]

		current = {}

		if isinstance(prediction, list) and len(prediction) > 0:
			current = prediction[0]
		else:
			current = prediction

		if "minutes" not in current:
			return None
		
		minutes = current["minutes"]

		if(int(minutes) > self.limit):
			return None

		message = self.clock() + " " + title + " arriving in " + minutes + " minutes"

		return message

	def inTimeSlot(self):
		now = datetime.now(self.timezone)
		hour = now.hour
		minute = now.minute
		weekday = now.weekday()

		current = hour * 100 + minute

		return weekday in self.weekdays and current >= self.minTime and current <= self.maxTime

	def run(self):
		url = "http://webservices.nextbus.com/service/publicJSONFeed?command=predictions&a=ttc&r=" + str(self.route) + "&s=" + str(self.stop)
		while True:

			if(self.inTimeSlot()):
				message = self.predict(url)
				if(message is None):
					message = self.clock()
				print(message)
				SoundThread(self.soundFile).start()
				SpeechThread(message).start()

			time.sleep(self.pollRate)