from flask import Flask
from flask import request
from flask import jsonify
import socket
from db import Database
from speech import SpeechThread

app = Flask(__name__, static_url_path="")
database = Database(app)

@app.route("/")
def root():
	return app.send_static_file("index.html")
	
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
	IP = getIp()
	app.run(host=IP, port='8080')
