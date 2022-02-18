import sys
import requests
from spin import log


def get_iam_api_key(config):
    url = '{}'.format(config['auth']['tokenUrl'])
    data = {
             'client_id': config['auth']['clientId'],
             'grant_type': 'password',
             'client_secret': config['auth']['clientSecret'],
             'scope': 'openid',
             'username': config['auth']['username'],
             'password': config['auth']['password']
           }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=data, headers=headers, verify=False)
    if response.status_code != 200:
        log.error(f'Error getting IAM Tokens from server {url}')
        sys.exit(1)
    response_json = response.json()
    if 'access_token' in response_json and 'refresh_token' in response_json:
        log.info('Found API Token {}'.format(response_json['access_token']))
        return response_json['access_token'], response_json['refresh_token']
    else:
        log.error('Error getting IAM Tokens from server response {url} {response.text}')
        sys.exit(1)
