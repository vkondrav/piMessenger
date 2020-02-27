APP_PORT = "8080"
CAMERA_PORT = "8082"
BASE_IMG_DIRECTORY = "/img"
RELATIVE_IMG_DIRECTORY = "/static" + BASE_IMG_DIRECTORY
SNAPSHOT_URL = "http://localhost:8081/0/action/snapshot"
MAX_GALLERY_SIZE = 20
IPAPI_KEY = "3da6b6ce3ea6a1a8199540a2b2726154"
GOOGLE_API_KEY = "AIzaSyAytb3l7eA-3-w3JgIKYBntZQW6FtfQIM8"
CAMERA_WAV = "camera-shutter.wav"
BING_WAV = "bingbong.wav"
TRANSIT = {
    "timezone": "US/Eastern",
    "weekdays": [0,1,2,3,4],
    "minTime": 715,
    "maxTime": 900,
    "limit": 15,
    "poll_rate": 180,
    "route": 508,
    "stop": 5692
}
LOG_FILE_LOCATION= "/home/pi/piMessenger/app/tmp/app.log"