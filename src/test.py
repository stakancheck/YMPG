import logging
import sys
from pprint import pprint

from client import PlayerClient


logger = logging.getLogger('test_control')
logger.setLevel('DEBUG')
handler = logging.StreamHandler(sys.stdout)
log_format = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s')
handler.setFormatter(log_format)
logger.addHandler(handler)


def control_loop():
    client = PlayerClient(debug=True)
    logger.info('Start')
    while True:
        main_loop(client)


def main_loop(client: PlayerClient):
    listen_music(client)
    # if client.authorization.is_auth:
    #     listen_music(client)
    # else:
    #     input('Auth? Any key...')
    #     auth(client)


def auth(client: PlayerClient):
    client.authorization.request_code()
    code = input('Code: ')
    result = client.authorization.get_token(personal_code=code)
    if result.success:
        logger.info(f'Success auth {result.callback.access_token}')
    else:
        logger.error('Auth failed')


def listen_music(client):
    # logger.info(f'TOKEN: {client.authorization.data}')
    client.get_music_client()
    print(client.music_client.users_likes_tracks())


if __name__ == '__main__':
    control_loop()
