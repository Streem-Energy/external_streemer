import requests


BASE_URL = 'https://api.streem.eu'


params = {
    'email': '',
    'password': '',
}

r = requests.post(BASE_URL + '/authenticate', params=params)
print(r.json())
token = r.json()['auth_token']


headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': token,
}

r = requests.get(BASE_URL + '/v2/installations', headers=headers)
print(r.json())