import requests

from flask import Flask

PROTOCOL_BASE = "http://"

FACE_HOSTNAME = "face"
FACE_PORT = "5000"

ARUCO_HOSTNAME = "aruco"
ARUCO_PORT = "5000"

MAGNET_PORT = "5000"
MAGNET_HOSTNAME = "magnet"


app = Flask(__name__)
@app.route('/')
def main():
    face_url = build_url(FACE_HOSTNAME, FACE_PORT)
    aruco_url = build_url(ARUCO_HOSTNAME, ARUCO_PORT)
    magnet_url = build_url(MAGNET_HOSTNAME, MAGNET_PORT)

    return 'hello'

def build_url(host, port):
    return PROTOCL_BASE + host + ":" + port


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
