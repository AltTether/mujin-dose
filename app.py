import json
import requests


PROTOCOL_BASE = "http://"

FACE_HOSTNAME = "face"
FACE_PORT = "5000"

ARUCO_HOSTNAME = "aruco"
ARUCO_PORT = "5000"

MAGNET_PORT = "5000"
MAGNET_HOSTNAME = "magnet"


def main():
    face_url = build_url(FACE_HOSTNAME, FACE_PORT)
    aruco_url = build_url(ARUCO_HOSTNAME, ARUCO_PORT)
    magnet_url = build_url(MAGNET_HOSTNAME, MAGNET_PORT)

    while(True):
        response = requests.get(magnet_url, stream=True)
        for line in response.iter_lines():
            if line:
                response_json = json.loads(line) 
                if response_json["state"] == 1:
                    print("open")

def build_url(host, port):
    return PROTOCOL_BASE + host + ":" + port


if __name__ == '__main__':
    main()
