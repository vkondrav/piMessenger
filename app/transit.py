import os
import threading
import time
import requests
from datetime import datetime
from pytz import timezone
import logging
from googleTTS import GoogleTSSThread

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

		self.apiKey = config["api_key"]
		self.driveOrigin = config["drive"]["origin"]
		self.driveDestination = config["drive"]["destination"]
		threading.Thread.__init__(self)

	def clock(self):
		return datetime.now(self.timezone).strftime("%I:%M%p")

	def predictDrive(self):
		url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&departure_time=now&origins=" + self.driveOrigin + "&destinations=" + self.driveDestination + "&key=" + self.apiKey

		logging.info(url)
		r = requests.get(url)

		if(r.status_code != 200):
			return None

		json = r.json()
		if "rows" not in json:
			return None

		rows = json["rows"]
		if not isinstance(rows, list) or len(rows) <= 0:
			return None

		row = rows[0]

		if "elements" not in row:
			return None
		
		elements = row["elements"]
		if not isinstance(elements, list) or len(elements) <= 0:
			return None

		element = elements[0]

		if "duration_in_traffic" not in element:
			return None

		duration = element["duration_in_traffic"]

		minutes = int(duration["value"]) // 60

		return "Your drive to work is estimated to be " + str(minutes) + " minutes"

	def predictTransit(self):
		url = "http://webservices.nextbus.com/service/publicJSONFeed?command=predictions&a=ttc&r=" + str(self.route) + "&s=" + str(self.stop)

		logging.info(url)
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

		return title + " arriving in " + minutes + " minutes."

	def predict(self):
		transit = self.predictTransit() or ""
		drive = self.predictDrive() or ""

		return self.clock() + ". " + transit + " " + drive

	def inTimeSlot(self):
		now = datetime.now(self.timezone)
		hour = now.hour
		minute = now.minute
		weekday = now.weekday()

		current = hour * 100 + minute

		return weekday in self.weekdays and current >= self.minTime and current <= self.maxTime

	def run(self):
		while True:

			if(self.inTimeSlot()):
				message = self.predict()
				logging.info(message)
				GoogleTSSThread(message, self.soundFile).start()
			else:
				logging.info("not in time slot")

			time.sleep(self.pollRate)