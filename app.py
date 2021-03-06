import os
import json
import requests

from src import Logger


HOST_KEYS = ['FACE_HOST', 'ARUCO_HOST', 'MAGNET_HOST', "POOL_HOST", "WEB_HOST"]
PORT_KEYS = ['FACE_PORT', 'ARUCO_PORT', 'MAGNET_PORT', "POOL_PORT", "WEB_PORT"]

CONFIG = {'PROTOCOL_BASE': 'http://',
          'FACE_HOST': 'face', 'FACE_PORT': '5001',
          'ARUCO_HOST': 'aruco', 'ARUCO_PORT': '5002',
          'MAGNET_HOST': 'magnet', 'MAGNET_PORT': '5003',
          'POOL_HOST': 'localhost', 'POOL_PORT': '5004',
          'WEB_HOST': 'localhost', 'WEB_PORT': None}

logger = Logger()

def main():
    set_config()

    face_url = build_url(CONFIG['FACE_HOST'], CONFIG['FACE_PORT'])
    aruco_url = build_url(CONFIG['ARUCO_HOST'], CONFIG['ARUCO_PORT'])
    magnet_url = build_url(CONFIG['MAGNET_HOST'], CONFIG['MAGNET_PORT'])
    pool_url = build_url(CONFIG['POOL_HOST'], CONFIG['POOL_PORT'])
    web_url = build_url(CONFIG['WEB_HOST'], CONFIG['WEB_PORT'])

    logger.info('mujin service is starting')
    while(True):
        logger.info('mujin service start to check the door')

        # 扉開閉検知をする
        response = requests.get(magnet_url, stream=True)
        for line in response.iter_lines():
            if line:
                response_json = json.loads(line.decode('utf-8'))
                if response_json['state'] == 0:
                    break
        logger.info('mujin item case\'s door is opened')

        # 商品検出する
        response = requests.get(aruco_url+'/item')
        before_ids_json = response.json()['ids']
        logger.info('get ids in item case: {}'.format(json.dumps(before_ids_json)))

        # 顔検出する
        logger.info('mujin service detecting face')
        response = requests.get(face_url, stream=True)
        response_json = response.json()

        detected_external_image_id = response_json["FaceMatches"][0]["Face"]["ExternalImageId"]
        user_id, image_file_name = detected_external_image_id.split('_')
        user_name = image_file_name.split('.')[0]

        logger.info('mujin face detected user: {}'.format(user_name))

        # 扉開閉検知をする
        response = requests.get(magnet_url, stream=True)
        for line in response.iter_lines():
            if line:
                response_json = json.loads(line.decode('utf-8'))
                if response_json["state"] == 1:
                    break

        logger.info('mujin item case\'s door is closed')

        response = requests.get(aruco_url+'/item')
        after_ids_json = response.json()['ids']
        logger.info('get ids in item case: {}'.format(json.dumps(after_ids_json)))

        # 購入、追加した商品のidsを取得する
        added_item_ids = list(set(after_ids_json) - set(before_ids_json))
        bought_item_ids = list(set(before_ids_json) - set(after_ids_json))

        logger.info('added item ids: {}'.format(added_item_ids))
        logger.info('bought_item_ids: {}'.format(bought_item_ids))


        # リクエストプールに購入商品をなげる
        post_request_json = {"user_id": int(user_id), "user_name": user_name, "items": []}
        for item_id in bought_item_ids:
            # 各アイテムに対して情報を取得する
            item_response = requests.get(web_url+'/item', params={"id": item_id})
            logger.info(item_response)
            item_response_json = item_response.json()["item"]
            item_json = {"item_id": item_id,
                         "item_name": item_response_json["name"],
                         "value": item_response_json["value"],
                         "volume": 1}
            post_request_json["items"].append(item_json)

        logger.info('posting request to pool')
        response = requests.post(pool_url,
                                 json.dumps(post_request_json),
                                 headers={'Content-Type': 'application/json'})
        logger.info('complete posting')

def build_url(host, port=None):
    if port is None:
        return CONFIG['PROTOCOL_BASE'] + host
    else:
        return CONFIG['PROTOCOL_BASE'] + host + ':' + port

def set_config():
    for host in HOST_KEYS:
        if os.getenv(host):
            CONFIG[host] = os.environ[host]

    for port in PORT_KEYS:
        if os.getenv(port):
            CONFIG[port] = os.environ[port]

def build_url(host, port=None):
    if port is not None:
        return CONFIG['PROTOCOL_BASE'] + host + ":" + port
    else:
        return CONFIG['PROTOCOL_BASE'] + host


if __name__ == '__main__':
    main()
