import os

from dotenv import load_dotenv

load_dotenv()

base_url_per_env = {
    'prod_api': 'https://api.streem.eu',
}

ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')


class Env:
    name: str
    base_url: str

    def __init__(self, name):
        self.name = name
        self.base_url = base_url_per_env[name]