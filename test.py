import logging
from pprint import pprint

from client import PlayerClient


logger = logging.getLogger('test_control')


def control_loop():
    client = PlayerClient()
    while True:
        main_loop(client)


def main_loop(client: PlayerClient):
    if client.authorization.is_auth:
        listen_music(client)
    else:
        input('Auth? Any key...')
        auth(client)


def auth(client: PlayerClient):
    client.music_client.request_code()
    code = input('Code: ')
    result = client.authorization.get_token(personal_code=code)
    if result.success:
        logger.info('Success auth')
    else:
        logger.error('Auth failed')


def listen_music(client):
    client.get_music_client()
    pprint(client.users_likes_tracks())


if __name__ == '__main__':
    control_loop()