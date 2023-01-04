import uuid
import socket
import logging
import requests
import webbrowser

from pprint import pprint
from settings import CLIENT_SECRET, CLIENT_ID
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
        self.data = None
        self.client_id = client_id
        self.client_secret = client_secret
        self.device = socket.gethostname()
        self.uuid = uuid.uuid4()
        self.is_auth = False

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

    def get_token(self, personal_code) -> ResponseAuth:
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
                self.data = data
                return ResponseAuth(callback=data,
                                    success=True)

            else:
                return ResponseAuth(success=False)

        except requests.exceptions.ConnectionError:
            return ResponseAuth(success=False)


if __name__ == "__main__":
    auth = Authorize(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    auth.request_code()
    code = input('Code: ')
    result = auth.get_token(personal_code=code)

    if result.success:
        print('УСПЕШНО ПОЛУЧЕН ТОКЕН: ')
        pprint(result.callback)
