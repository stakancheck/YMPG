import logging

from yandex_music import Client
from authorize import Authorize
from settings import CLIENT_SECRET, CLIENT_ID

logger = logging.getLogger('main_client')


class PlayerClient:
    def __init__(self):
        self.music_client: Client = None
        self.token = ''
        self.authorization = Authorize(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

    def get_music_client(self):
        if self.authorization.is_auth:
            client = Client(token=self.authorization.data.access_token)
            self.music_client = client
        else:
            logging.debug('Try get client without authorization')

    def request_code(self):
        return self.authorization.request_code()

    def request_auth(self, user_code: str):
        return self.authorization.get_token(personal_code=user_code)

