import os
import threading
import time
import requests
from datetime import datetime
from pytz import timezone
import logging
from googleTTS import GoogleTSSThread
import random

class PredictThread(threading.Thread):

	def __init__(self, config):
		self.config = config

		threading.Thread.__init__(self)

	def clock(self):
		tz = timezone(self.config["timezone"])
		return datetime.now(tz).strftime("%I:%M%p")

	def predictDrive(self):
		apiKey = self.config["drive"]["api_key"]
		origin = self.config["drive"]["origin"]
		destination = self.config["drive"]["destination"]
		departureTime = self.config["drive"]["departure_time"]
		units = self.config["drive"]["units"]

		url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=" + units +"&departure_time=" + departureTime + "&origins=" + origin + "&destinations=" + destination + "&key=" + apiKey

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

		return "Your drive to work is estimated to be " + str(minutes) + " minutes."

	def predictTransit(self):
		system = self.config["transit"]["system"]
		route = self.config["transit"]["route"]
		stop = self.config["transit"]["stop"]

		url = "http://webservices.nextbus.com/service/publicJSONFeed?command=predictions&a=" + system + "&r=" + route + "&s=" + stop

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

		if(int(minutes) > self.config["limit"]):
			return None

		return title + " arriving in " + minutes + " minutes."

	def predictNews(self):
		apiKey = self.config["news"]["api_key"]
		region = self.config["news"]["region"]

		url = "https://api.currentsapi.services/v1/latest-news?region=" + region + "&apiKey=" + apiKey

		logging.info(url)
		r = requests.get(url)

		if(r.status_code != 200):
			return None

		json = r.json()
		news = json["news"]

		if not isinstance(news, list) or len(news) <= 0:
			return None
		
		story = news[random.randint(0, len(news) - 1)]

		return "In the news. " + story["title"] + "."

	def predict(self):
		transit = self.predictTransit() or ""
		drive = self.predictDrive() or ""
		news = self.predictNews() or ""

		return self.clock() + ". " + transit + " " + drive + " " + news

	def inTimeSlot(self):
		tz = timezone(self.config["timezone"])
		minTime = self.config["min_time"]
		maxTime = self.config["max_time"]
		weekdays = self.config["weekdays"]

		now = datetime.now(tz)
		hour = now.hour
		minute = now.minute
		weekday = now.weekday()

		current = hour * 100 + minute

		return weekday in weekdays and current >= minTime and current <= maxTime

	def run(self):
		while True:

			if(self.inTimeSlot()):
				message = self.predict()
				logging.info(message)
				GoogleTSSThread(message, self.config["sound_file"]).start()
			else:
				logging.info("not in time slot")

			time.sleep(self.config["poll_rate"])