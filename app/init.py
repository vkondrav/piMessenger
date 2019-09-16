from flask import Flask
from flask import request
from flask import jsonify
import socket
import os
from db import Database
from speech import SpeechThread
from sound import SoundThread
from transit import TransitThread
import requests
import config

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_url_path="")
database = Database(app)

@app.route("/")
def root():
	return app.send_static_file("index.html")

@app.route("/photos")
def photos():
	return app.send_static_file("photos.html")
	
@app.route("/send")
def send():
	message = request.args.get("message", type = str)
	
	if message is not None:
		database.addMessage(message)
		SpeechThread(message).start()
		return jsonify({"success": message})
	else:
		return jsonify({"error": "no message"})
	
@app.route("/messages")
def messages():
	messages = database.getMessages()
	return jsonify(messages)
	
@app.route("/camport")
def camPort():
	return jsonify({"cam_port" : config.CAMERA_PORT})
	
@app.route("/photos/data")
def images():
	images = os.listdir(basedir + config.RELATIVE_IMG_DIRECTORY)
	images = list(filter(lambda a: a != "lastsnap.jpg", images))
	images = sorted(images, reverse = True, key=imageSort)[:config.MAX_GALLERY_SIZE]
	images = [config.BASE_IMG_DIRECTORY + "/" + item for item in images]
	return jsonify(images)
	
def imageSort(img):
	return img[img.index("-") + 1:] #ignore the motion tag that gets attached
	
@app.route("/capture")
def capture():
	SoundThread(config.CAMERA_WAV).start()
	r = requests.get(config.SNAPSHOT_URL)
	if(r.status_code == 200):
		return jsonify({"success":"image captured"})
	else:
		return jsonify({"failure":"capture fail"})

@app.route("/peers")
def peers():
	return app.send_static_file("peers.html")

@app.route("/peers/data")
def peersData():
	output = os.popen("deluge-console info -v | grep -w 'Peer' | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}'").read()
	peers = output.split('\n')

	result = []
	for peer in peers:

		if(len(peer) == 0):
			continue

		formatted = {}
		url = "http://api.ipapi.com/" + peer + "?access_key=" + config.IPAPI_KEY
		r = requests.get(url)

		if(r.status_code == 200):
			json = r.json()
			formatted["country"] = json["country_name"]
			formatted["region"] = json["region_name"]
			formatted["city"] = json["city"]
			formatted["ip"] = json["ip"]
			lat = json["latitude"]
			lng = json["longitude"]
			formatted["latitude"] = lat
			formatted["longitude"] = lng
			formatted["gmaps"] = "https://www.google.com/maps/search/?api=1&query=" + repr(lat) + "," + repr(lng)
			formatted["flag"] = json["location"]["country_flag"]
			result.append(formatted) 
	
	return jsonify(result)

@app.after_request
def addHeaders(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
		
def getIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

if __name__ == '__main__':
	TransitThread(config.TRANSIT_POLL, config.TRANSIT_ROUTE, config.TRANSIT_STATION, config.BING_WAV).start()
	IP = getIp()
	app.run(host=IP, port=config.APP_PORT)