import requests


def get_auth_token():
    token_request = requests.post('https://regions-test.2gis.com/v1/auth/tokens')
    assert token_request.status_code == 200, print('ошибка запроса, статус-код:', token_request.status_code)

    response_headers = token_request.headers
    session_token = dict([response_headers.get('Set-Cookie')[:38].split('=')])
    return session_token

