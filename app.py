import os
import json
import requests

from logging import getLogger


HOST_KEYS = ['FACE_HOST', 'ARUCO_HOST', 'MAGNET_HOST']
PORT_KEYS = ['FACE_PORT', 'ARUCO_PORT', 'MAGNET_PORT']

CONFIG = {'PROTOCOL_BASE': 'http://',
          'FACE_HOST': 'face', 'FACE_PORT': '5000',
          'ARUCO_HOST': 'aruco', 'ARUCO_PORT': '5000',
          'MAGNET_HOST': 'magnet', 'MAGNET_PORT': '5000'}

def main():
    set_CONFIG()

    face_url = build_url(CONFIG['FACE_HOST'], CONFIG['FACE_PORT'])
    aruco_url = build_url(CONFIG['ARUCO_HOST'], CONFIG['ARUCO_PORT'])
    magnet_url = build_url(CONFIG['MAGNET_HOST'], CONFIG['MAGNET_PORT'])

    while(True):
        response = requests.get(magnet_url, stream=True)
        for line in response.iter_lines():
            if line:
                response_json = json.loads(line.decode('utf-8'))
                if response_json['state'] == 1:
                    print('open')

def build_url(host, port):
    return CONFIG['PROTOCOL_BASE'] + host + ':' + port

def set_CONFIG():
    for host in HOST_KEYS:
        if os.getenv(host):
            CONFIG[host] = os.environ[host]

    for port in PORT_KEYS:
        if os.getenv(port):
            CONFIG[port] = os.environ[port]



if __name__ == '__main__':
    main()
