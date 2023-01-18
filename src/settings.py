import logging
import os
import dotenv

logger = logging.getLogger('Settings')

env_names = {
    'access_token': 'ACCESS_TOKEN',
    'client_id': 'CLIENT_ID',
    'client_secret': 'CLIENT_SECRET',
    'refresh_token': 'REFRESH_TOKEN',
    'expires_in': 'EXPIRES_IN',
    'token_type': 'TOKEN_TYPE'
}

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

CLIENT_ID = os.environ.get(env_names['client_id'])
CLIENT_SECRET = os.environ.get(env_names['client_secret'])
