from getting_an_authorization_token import getting_an_authorization_token
from current_datetime import current_datetime
from big_title import BIG_TITLE, BIG_NEGATIVE_TITLE
import requests
import pytest


URL = 'https://regions-test.2gis.com/v1/favorites'


class TestPositiveScripts:
    @pytest.mark.parametrize(
        "data, status_code",
        [
            pytest.param(
                {
                    'title': 'Latin characters',
                    'lat': 55.028254,
                    'lon': 82.918501,
                    'color': 'BLUE'
                }, 200, marks=pytest.mark.set1),
            pytest.param(
                {
                    'title': BIG_TITLE,
                    'lat': 89.999999,
                    'lon': 179.999999,
                    'color': 'GREEN'
                }, 200, marks=pytest.mark.set2),
            pytest.param(
                {
                    'title': 'Кириллические символы',
                    'lat': 90,
                    'lon': -180,
                    'color': 'RED'
                }, 200, marks=pytest.mark.set3),
            pytest.param(
                {
                    'title': ',.:""!?...',
                    'lat': 1,
                    'lon': 1,
                    'color': 'YELLOW'
                }, 200, marks=pytest.mark.set4)
        ])
    def test_smoke_creating_a_favorite_place(self, data, status_code):
        cookies = getting_an_authorization_token()
        favorite_place = requests.post(URL, cookies=cookies, data=data)
        response = eval(favorite_place.content.decode())
        actual_status_code = favorite_place.status_code

        for key in data:
            assert key in response, f'Ключ {key} отсутствует в ответе'
            assert data[key] == response[key], f'Ожидается {data[key]}, фактически: {response[key]}'
        assert 'id' in response, 'Ожидается "id" в ответе'
        assert isinstance(response['id'], int), f'Значение "id" ожидается int, Фактически: {type(response["id"])}'
        assert isinstance(response['lat'], float), f'Значение "id" ожидается int, Фактически: {type(response["lat"])}'
        assert isinstance(response['lon'], float), f'Значение "id" ожидается int, Фактически: {type(response["lon"])}'
        assert 'created_at' in response, 'Ожидается "created_at" в ответе'
        assert actual_status_code == status_code, f'Ожидался статус-код {status_code}, фактически: {actual_status_code}'


    @pytest.mark.parametrize(
        "data, status_code",
        [
            pytest.param(
                {
                    'title': 123,
                    'lat': 55.028254,
                    'lon': 82.918501,
                    'color': 'BLUE'
                }, 200, marks=pytest.mark.set1),
            pytest.param(
                {
                    'title': -13.01,
                    'lat': 56.864356,
                    'lon': 60.649108,
                    'color': 'GREEN'
                }, 200, marks=pytest.mark.set2),
            pytest.param(
                {
                    'title': True,
                    'lat': 56.864356,
                    'lon': 60.649108,
                    'color': 'GREEN'
                }, 200, marks=pytest.mark.set3)
        ])
    def test_check_title_types(self, data, status_code):
        cookies = getting_an_authorization_token()
        favorite_place = requests.post(URL, cookies=cookies, data=data)
        response = eval(favorite_place.content.decode())
        actual_status_code = favorite_place.status_code

        assert isinstance(response['title'], str), f'Значение "id" ожидается str, Фактически: {type(response["title"])}'
        assert actual_status_code == status_code, f'Ожидался статус-код {status_code}, фактически: {actual_status_code}'


    @pytest.mark.parametrize(
        "data, status_code",
        [
            pytest.param(
                {
                    'title': 'valid',
                    'lat': 0.000001,
                    'lon': 0.000001,
                    'color': 'BLUE'
                }, 200, marks=pytest.mark.set1),
            pytest.param(
                {
                    'title': 'valid',
                    'lat': 90,
                    'lon': 180,
                    'color': 'GREEN'
                }, 200, marks=pytest.mark.set2),
            pytest.param(
                {
                    'title': 'Валидный тайтл',
                    'lat': -90,
                    'lon': -180,
                    'color': 'RED'
                }, 200, marks=pytest.mark.set3),
            pytest.param(
                {
                    'title': 'Валидный тайтл',
                    'lat': 0,
                    'lon': 0,
                    'color': 'YELLOW'
                }, 200, marks=pytest.mark.set4),
            pytest.param(
                {
                    'title': 'Валидный тайтл',
                    'lat': -0,
                    'lon': -0,
                    'color': 'YELLOW'
                }, 200, marks=pytest.mark.set5),
            pytest.param(
                {
                    'title': 'Валидный тайтл',
                    'lat': 0.000001,
                    'lon': 0,
                    'color': 'YELLOW'
                }, 200, marks=pytest.mark.set6),
            pytest.param(
                {
                    'title': 'Валидный тайтл',
                    'lat': 0,
                    'lon': 0.000001,
                    'color': 'YELLOW'
                }, 200, marks=pytest.mark.set7),
            pytest.param(
                {
                    'title': 'Валидный title',
                    'lat': 0.0000001,
                    'lon': 50,
                    'color': 'YELLOW'
                 }, 200, marks=pytest.mark.set8),
            pytest.param(
                {
                    'title': 'Валидный title',
                    'lat': 50,
                    'lon': 0.0000001,
                    'color': 'YELLOW'
                 }, 200, marks=pytest.mark.set9)
        ])
    def test_lat_lon(self, data, status_code):
        cookies = getting_an_authorization_token()
        favorite_place = requests.post(URL, cookies=cookies, data=data)
        response = eval(favorite_place.content.decode())
        actual_status_code = favorite_place.status_code

        for key in data:
            if data['lat'] == 0.0000001:
                assert response['lat'] == 0.0, f"Ожидается 'lat': 0.0, фактически: {response['lat']}"
                continue
            if data['lon'] == 0.0000001:
                assert response['lon'] == 0.0, f"Ожидается 'lon': 0.0, фактически: {response['lon']}"
                continue
            assert key in response, f'Ключ {key} отсутствует в ответе'
            assert data[key] == response[key], f'Ожидается {data[key]}, фактически: {response[key]}'
        assert actual_status_code == status_code, f'Ожидался статус-код {status_code}, фактически: {actual_status_code}'


    @pytest.mark.parametrize(
        "data, status_code",
        [
            pytest.param(
                {
                    'title': 'Валидное Название',
                    'lat': '55.028254',
                    'lon': 82.918501,
                    'color': 'BLUE'
                 }, 200, marks=pytest.mark.set1),
            pytest.param(
                {
                    'title': 'Валидный title',
                    'lat': 56.864356,
                    'lon': '60.649108',
                    'color': 'YELLOW'
                 }, 200, marks=pytest.mark.set2),
            pytest.param(
                {
                    'title': 'Валидный title',
                    'lat': 56,
                    'lon': 60,
                    'color': 'YELLOW'
                }, 200, marks=pytest.mark.set3)
        ])
    def test_check_lat_lon_types(self, data, status_code):
        cookies = getting_an_authorization_token()
        favorite_place = requests.post(URL, cookies=cookies, data=data)
        response = eval(favorite_place.content.decode())
        actual_status_code = favorite_place.status_code

        assert isinstance(response['lat'], float), f'Значение "id" ожидается float, Фактически: {type(response["lat"])}'
        assert isinstance(response['lon'], float), f'Значение "id" ожидается float, Фактически: {type(response["lon"])}'
        assert actual_status_code == status_code, f'Ожидался статус-код {status_code}, фактически: {actual_status_code}'


    def test_colors(self):
        colors = ('BLUE', 'GREEN', 'RED', 'YELLOW')
        data = {'title': 'Валидное Название',
                'lat': 55.028254,
                'lon': 82.918501,
                'color': None}

        for color in colors:
            data['color'] = color
            cookies = getting_an_authorization_token()
            favorite_place = requests.post(URL, cookies=cookies, data=data)
            response = eval(favorite_place.content.decode())
            actual_status_code = favorite_place.status_code
            assert response['color'] == data['color'], f'Ожидается {data["color"]}, фактически: {response["color"]}'
            assert actual_status_code == 200, f'Ожидался статус-код {200}, фактически: {actual_status_code}'

        del data['color']
        cookies = getting_an_authorization_token()
        favorite_place = requests.post(URL, cookies=cookies, data=data)
        response = favorite_place.content.decode()
        actual_status_code = favorite_place.status_code
        assert '"color": null' in response, f'Ожидается "color": null, фактически: {response[-57:-44]}'
        assert actual_status_code == 200, f'Ожидался статус-код {200}, фактически: {actual_status_code}'


    @pytest.mark.parametrize(
        "data, status_code",
        [
            ({
                'title': 'Валидное название',
                'lat': 55.028254,
                'lon': 82.918501,
                'color': 'RED'
             }, 200)
        ])
    def test_check_creation_datetime(self, data, status_code):
        cookies = getting_an_authorization_token()
        favorite_place = requests.post(URL, cookies=cookies, data=data)
        response = eval(favorite_place.content.decode())
        actual_status_code = favorite_place.status_code
        actual_datetime = response['created_at'][:16]
        actual_timezone = response['created_at'][19:]

        assert actual_datetime == current_datetime, f'Ожидается дата и время создания: {current_datetime}' \
                                                    f', фактически: {actual_datetime}'
        assert actual_timezone == '+00:00', f'Ожидается таймзона +00:00, фактически: {actual_timezone}'
        assert actual_status_code == status_code, f'Ожидался статус-код {status_code}, фактически: {actual_status_code}'


class TestNegativeScripts:
    @pytest.mark.parametrize(
        "data, status_code, message, cookies",
        [
            pytest.param(
                {
                    'title': 'Валидное Название',
                    'lat': 55.028254,
                    'lon': 82.918501,
                    'color': 'BLUE'
                }, 401, "Параметр 'token' является обязательным", None, marks=pytest.mark.set1),
            pytest.param(
                {
                    'title': 'Валидное Название',
                    'lat': 55.028254,
                    'lon': 82.918501,
                    'color': 'BLUE'
                }, 401, "Передан несуществующий или «протухший» 'token'", {'token': '49e61919622d4c7db3d447f12cec95ea'},
                marks=pytest.mark.set2)

        ])
    def test_sending_an_invalid_token(self, data, status_code, message, cookies):
        favorite_place = requests.post(URL, cookies=cookies, data=data)
        response_str = favorite_place.content.decode()
        response = eval(response_str)
        actual_status_code = favorite_place.status_code

        if 'error' in response_str:
            error_message = response['error']['message']
            assert error_message == message, f'Ожидается: {message}, фактически: {error_message}'
        else:
            assert 'error' in response_str, f'Ожидается сообщение об ошибке "{message}", фактически: {response}'
        assert actual_status_code == status_code, f'Ожидался статус-код {status_code}, фактически: {actual_status_code}'


    @pytest.mark.parametrize(
        "data, status_code, message",
        [
            pytest.param(
                {
                    'title': '',
                    'lat': 55.028254,
                    'lon': 82.918501,
                    'color': 'BLUE'
                }, 400, "Параметр 'title' не может быть пустым", marks=pytest.mark.set1),
            pytest.param(
                {
                    'title': BIG_NEGATIVE_TITLE,
                    'lat': 55.028254,
                    'lon': 82.918501,
                    'color': 'BLUE'
                }, 400, "Параметр 'title' не может быть больше 999 символов", marks=pytest.mark.set2),
            pytest.param(
                {
                    'title': '@#*/=',
                    'lat': 55.028254,
                    'lon': 82.918501,
                    'color': 'BLUE'
                }, 400, "Параметр 'title'  Может содержать латинские и кириллические символы, цифры и знаки препинания",
                marks=pytest.mark.set3)
        ])
    def test_negative_title(self, data, status_code, message):
        cookies = getting_an_authorization_token()
        favorite_place = requests.post(URL, cookies=cookies, data=data)
        response_str = favorite_place.content.decode()
        response = eval(response_str)
        actual_status_code = favorite_place.status_code

        if 'error' in response_str:
            error_message = response['error']['message']
            assert error_message == message, f'Ожидается: {message}, фактически: {error_message}'
        else:
            assert 'error' in response_str, f'Ожидается сообщение об ошибке "{message}", фактически: {response}'
        assert actual_status_code == status_code, f'Ожидался статус-код {status_code}, фактически: {actual_status_code}'


    @pytest.mark.parametrize(
        "data, status_code, message",
        [
            pytest.param(
                {
                    'title': 'Валидное Название',
                    'lat': 'a',
                    'lon': 0,
                    'color': 'BLUE'
                 }, 400, "Параметр 'lat' должен быть числом", marks=pytest.mark.set1),
            pytest.param(
                {
                    'title': 'Валидный title',
                    'lat': 0,
                    'lon': 'a',
                    'color': 'YELLOW'
                 }, 400, "Параметр 'lon' должен быть числом", marks=pytest.mark.set2),
            pytest.param(
                {
                    'title': 'Валидный title',
                    'lat': 90.000001,
                    'lon': 60,
                    'color': 'YELLOW'
                 }, 400, "Параметр 'lat' должен быть не более 90", marks=pytest.mark.set3),
            pytest.param(
                {
                    'title': 'Валидный title',
                    'lat': 50,
                    'lon': 180.000001,
                    'color': 'YELLOW'
                 }, 400, "Параметр 'lon' должен быть не более 180", marks=pytest.mark.set4),
            pytest.param(
                {
                    'title': 'Валидный title',
                    'lat': -90.000001,
                    'lon': 60,
                    'color': 'YELLOW'
                 }, 400, "Параметр 'lat' должен быть не менее -90", marks=pytest.mark.set5),
            pytest.param(
                {
                    'title': 'Валидный title',
                    'lat': 50,
                    'lon': -180.000001,
                    'color': 'YELLOW'
                 }, 400, "Параметр 'lon' должен быть не менее -180", marks=pytest.mark.set6)
        ])
    def test_negative_lat_lon(self, data, status_code, message):
        cookies = getting_an_authorization_token()
        favorite_place = requests.post(URL, cookies=cookies, data=data)
        response_str = favorite_place.content.decode()
        response = eval(response_str)
        actual_status_code = favorite_place.status_code

        if 'error' in response_str:
            error_message = response['error']['message']
            assert error_message == message, f'Ожидается: {message}, фактически: {error_message}'
        else:
            assert 'error' in response_str, f'Ожидается сообщение об ошибке "{message}", фактически: {response}'
        assert actual_status_code == status_code, f'Ожидался статус-код {status_code}, фактически: {actual_status_code}'


    @pytest.mark.parametrize(
        "data, status_code, message",
        [
            pytest.param(
                {
                    'title': 'Валидное имя',
                    'lat': 55.028254,
                    'lon': 82.918501,
                    'color': 'WHITE'
                }, 400, "Параметр 'color' может быть одним из следующих значений: BLUE, GREEN, RED, YELLOW",
                marks=pytest.mark.set1),
            pytest.param(
                {
                    'title': 'Валидное имя',
                    'lat': 55.028254,
                    'lon': 82.918501,
                    'color': 123
                }, 400, "Параметр 'color' может быть одним из следующих значений: BLUE, GREEN, RED, YELLOW",
                marks=pytest.mark.set2),
            pytest.param(
                {
                    'title': 'valid',
                    'lat': 55.028254,
                    'lon': 82.918501,
                    'color': 'Blue'
                }, 400, "Параметр 'color' может быть одним из следующих значений: BLUE, GREEN, RED, YELLOW",
                marks=pytest.mark.set3),
            pytest.param(
                {
                    'title': 'valid',
                    'lat': 55.028254,
                    'lon': 82.918501,
                    'color': 'Text'
                }, 400, "Параметр 'color' может быть одним из следующих значений: BLUE, GREEN, RED, YELLOW",
                marks=pytest.mark.set4)
        ])
    def test_negative_colors(self, data, status_code, message):
        cookies = getting_an_authorization_token()
        favorite_place = requests.post(URL, cookies=cookies, data=data)
        response_str = favorite_place.content.decode()
        response = eval(response_str)
        actual_status_code = favorite_place.status_code

        if 'error' in response_str:
            error_message = response['error']['message']
            assert error_message == message, f'Ожидается: {message}, фактически: {error_message}'
        else:
            assert 'error' in response_str, f'Ожидается сообщение об ошибке "{message}", фактически: {response}'
        assert actual_status_code == status_code, f'Ожидался статус-код {status_code}, фактически: {actual_status_code}'
