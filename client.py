import logging

from yandex_music import Client
from authorize import Authorize
from settings import CLIENT_SECRET, CLIENT_ID

logging.basicConfig(filename='logs.log', filemode='w')


class PlayerClient:
    def __init__(self):
        self.music_client = None
        self.token = ''
        self.authorization = Authorize(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

    def get_music_client(self):
        if self.authorization.is_auth:
            client = Client(token=self.authorization.data.access_token)
            self.music_client = client
        else:
            logging.debug('Try get client without authorization')

