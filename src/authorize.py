import os
import uuid
import socket
import dotenv
import logging
import requests
import webbrowser

from pprint import pprint
from settings import CLIENT_SECRET, CLIENT_ID, env_names
from dataclasses import dataclass

logger = logging.getLogger('authorize_client')


@dataclass
class AuthData:
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str


@dataclass
class ResponseAuth:
    callback: AuthData = None
    success: bool = True


class Authorize:
    """
    Класс авторизации пользователя, получение специального токена

    """
    URL = 'https://oauth.yandex.ru/'

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.device = socket.gethostname()
        self.uuid = uuid.uuid4()
        self.is_auth = False

    def start_auth(self):
        if self.check_has_token():
            pass
            # self.check_token_active()
        else:
            self.request_code()

    @staticmethod
    def check_has_token() -> bool:
        token = os.environ.get('ACCESS_TOKEN')
        return bool(token)

    # @staticmethod
    # def check_token_active() -> bool:
    #     time = os.environ.get(env_names['exprice'])

    @staticmethod
    def change_key(key_name: str, value: str):
        try:
            dotenv_file = dotenv.find_dotenv()
            dotenv.set_key(dotenv_file, key_name, value)
        except Exception as e:
            logger.error(f'While set env key: {e}')

    def request_code(self) -> bool:
        """
        Запрос на регистрацию (вызов браузера)

        :return: self
        """
        parameters = f'response_type=code&' \
                     f'client_id={self.client_id}&' \
                     f'device_id={self.uuid}&' \
                     f'device_name={self.device}'
        result_link = self.URL + 'authorize?' + parameters

        try:
            webbrowser.open(result_link, new=2)
            return True
        except Exception as e:
            logger.error(f'Request code failed with {e}')
            return False

    def get_response(self, personal_code) -> ResponseAuth:
        """
        Получение токена

        :param personal_code: Персональный код для получения токена
        :return: ResponseAuth
        """
        try:
            result_link = self.URL + 'token'
            parameters = f'grant_type=authorization_code&' \
                         f'code={personal_code}&' \
                         f'client_id={self.client_id}&' \
                         f'client_secret={self.client_secret}&' \
                         f'device_id={self.uuid}&' \
                         f'device_name={self.device}'

            request_auth = requests.post(result_link, data=parameters, timeout=10)

            if request_auth.status_code == 200:
                data = request_auth.json()
                self.is_auth = True
                data = AuthData(
                    access_token=data['access_token'],
                    expires_in=data['expires_in'],
                    refresh_token=data['refresh_token'],
                    token_type=data['token_type']
                )
                return ResponseAuth(callback=data,
                                    success=True)

            else:
                return ResponseAuth(success=False)

        except requests.exceptions.ConnectionError:
            return ResponseAuth(success=False)

    def refresh_token(self) -> ResponseAuth:
        pass

    def update_env_conf(self, token: str):
        self.change_key(key_name='DEBUG_TOKEN', value=token)


if __name__ == "__main__":
    auth = Authorize(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    auth.request_code()
    code = input('Code: ')
    result = auth.get_response(personal_code=code)

    if result.success:
        print('УСПЕШНО ПОЛУЧЕН ТОКЕН: ')
        auth.update_env_conf(result.callback.access_token)
        pprint(result.callback)
