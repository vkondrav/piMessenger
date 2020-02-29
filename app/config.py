APP_PORT = "8080"
CAMERA_PORT = "8082"
BASE_IMG_DIRECTORY = "/img"
RELATIVE_IMG_DIRECTORY = "/static" + BASE_IMG_DIRECTORY
SNAPSHOT_URL = "http://localhost:8081/0/action/snapshot"
MAX_GALLERY_SIZE = 20
IPAPI_KEY = "3da6b6ce3ea6a1a8199540a2b2726154"
CAMERA_WAV = "camera-shutter.wav"
PREDICT = {
    "timezone": "US/Eastern",
    "weekdays": [0,1,2,3,4],
    "min_time": 715,
    "max_time": 900,
    "limit": 15,
    "poll_rate": 180,
    "sound_file": "bingbong.wav",
    "transit": {
        "system": "ttc",
        "route": "508",
        "stop": "5692"
    },
    "drive": {
        "api_key": "AIzaSyAytb3l7eA-3-w3JgIKYBntZQW6FtfQIM8",
        "origin": "49+Yachters+Lane+Etobicoke+Ontario+Canada",
        "destination": "64+St+Claire+Avenue+East+Toronto+Ontario",
        "units": "metric",
        "departure_time": "now",
    },
    "news": {
        "api_key": "HHFZ--1qSgGhsLuGvi5smgNy60Hv8jwIREC3HCBPEZREuHSm",
        "region": "CA"
    }
}