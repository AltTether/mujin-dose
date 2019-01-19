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
        # 扉が開くまでループさせる
        door_closed = True
        while(door_closed):
            magnet_response = requests.get(magnet)
            magnet_response_json = magnet_response.json()
            if magnet_response_json["state"] == 1:
                door_closed = False

def build_url(host, port):
    return PROTOCL_BASE + host + ":" + port


if __name__ == '__main__':
    main()
