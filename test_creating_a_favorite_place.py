from getting_an_authorization_token import get_auth_token
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
        ],
        # Идентификаторы для каждого набора тестовых данных:
        ids=["set1", "set2", "set3", "set4"]
    )
    # Смоук-тест на валидных данных:
    def test_smoke_create_fav_place(self, data, status_code):
        cookies = get_auth_token()
        favorite_place = requests.post(URL, cookies=cookies, data=data)
        response = eval(favorite_place.content.decode())
        actual_status_code = favorite_place.status_code

        for key in data:
            assert key in response, f'Ключ {key} отсутствует в ответе'
            assert data[key] == response[key], f'Ожидается {data[key]}, фактически: {response[key]}'
        assert 'id' in response, 'Ожидается "id" в ответе'
        assert isinstance(response['id'], int), f'Значение "id" ожидается int, Фактически: {type(response["id"])}'
        assert isinstance(response['lat'], float), f'Значение "id" ожидается float, Фактически: {type(response["lat"])}'
        assert isinstance(response['lon'], float), f'Значение "id" ожидается float, Фактически: {type(response["lon"])}'
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
        ],
        # Идентификаторы для каждого набора тестовых данных:
        ids=["set1: title-int", "set2: title-float", "set3: title-bool"]
    )
    def test_title_types(self, data, status_code):
        cookies = get_auth_token()
        favorite_place = requests.post(URL, cookies=cookies, data=data)
        response = eval(favorite_place.content.decode())
        actual_status_code = favorite_place.status_code

        assert isinstance(response['title'], str), f'Значение "id" ожидается str, Фактически: {type(response["title"])}'
        assert actual_status_code == 200, f'Ожидался статус-код {status_code}, фактически: {actual_status_code}'



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
        ],
        # Идентификаторы для каждого набора тестовых данных:
        ids=["set1: lat, lon = 0.000001", "set2: lat=90, lon=180", "set3: lat=-90, lon=-180", "set4: lat, lon = 0",
             "set5: lat, lon = -0", "set6: lat=0.000001, lon=0", "set7: lat=0, lon=0.000001",
             "set8: lat-7 characters after the period", "set9: lon-7 characters after the period"]
    )
    def test_lat_lon(self, data, status_code):
        cookies = get_auth_token()
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
        ],
        # Идентификаторы для каждого набора тестовых данных:
        ids=["set1: lat-str", "set2: lon-str", "set3: lat, lon - int"]
    )
    def test_lat_lon_types(self, data, status_code):
        cookies = get_auth_token()
        favorite_place = requests.post(URL, cookies=cookies, data=data)
        response = eval(favorite_place.content.decode())
        actual_status_code = favorite_place.status_code

        assert isinstance(response['lat'], float), f'Значение "id" ожидается float, Фактически: {type(response["lat"])}'
        assert isinstance(response['lon'], float), f'Значение "id" ожидается float, Фактически: {type(response["lon"])}'
        assert actual_status_code == status_code, f'Ожидался статус-код {status_code}, фактически: {actual_status_code}'


    def test_colors(self):
        #Кортеж валидных цветов:
        colors = ('BLUE', 'GREEN', 'RED', 'YELLOW')
        data = {'title': 'Валидное Название',
                'lat': 55.028254,
                'lon': 82.918501,
                'color': None}

        #Подставляем валидные цвета в словарь и проверяем ответ от сервера:
        for color in colors:
            data['color'] = color
            cookies = get_auth_token()
            favorite_place = requests.post(URL, cookies=cookies, data=data)
            response = eval(favorite_place.content.decode())
            actual_status_code = favorite_place.status_code
            assert response['color'] == data['color'], f'Ожидается {data["color"]}, фактически: {response["color"]}'
            assert actual_status_code == 200, f'Ожидался статус-код {200}, фактически: {actual_status_code}'

        #Удаляем цвет из словаря и отправляем на сервер
        del data['color']
        cookies = get_auth_token()
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
        ],
        ids=["Valid data"]
    )
    #Проверяем корректность даты и времени в ответе от сервера на валидных данных:
    def test_creation_datetime(self, data, status_code):
        cookies = get_auth_token()
        favorite_place = requests.post(URL, cookies=cookies, data=data)
        response = eval(favorite_place.content.decode())
        actual_status_code = favorite_place.status_code
        actual_datetime = response['created_at'][:16]
        actual_timezone = response['created_at'][19:]

        assert actual_datetime == current_datetime, f'Ожидается дата и время создания: {current_datetime}' \
                                                    f', фактически: {actual_datetime}'
        assert actual_timezone == '+00:00', f'Ожидается таймзона +00:00, фактически: {actual_timezone}'
        assert actual_status_code == status_code, f'Ожидался статус-код {status_code}, фактически: {actual_status_code}'

    @pytest.mark.parametrize(
        "data, status_code",
        [
            pytest.param(
                {
                    'title': ' Valid ',
                    'lat': 55.028254,
                    'lon': 82.918501,
                    'color': 'BLUE'
                }, 200, marks=pytest.mark.set1),
            pytest.param(
                {
                    'title': 'Valid',
                    'lat': ' 89.999999 ',
                    'lon': 179.999999,
                    'color': 'GREEN'
                }, 200, marks=pytest.mark.set2),
            pytest.param(
                {
                    'title': 'Валидный тайтл',
                    'lat': 90,
                    'lon': ' -180 ',
                    'color': 'RED'
                }, 200, marks=pytest.mark.set3),
            pytest.param(
                {
                    'title': 'Valid',
                    'lat': 1,
                    'lon': 1,
                    'color': ' YELLOW '
                }, 200, marks=pytest.mark.set4)
        ],
        # Идентификаторы для каждого набора тестовых данных:
        ids=["set1: title = ' Valid '", "set2: lat = ' 89.999999 '", "set3: lon = ' -180 '", "set4: color = ' YELLOW '"]
    )
    #Проверка удаления лишних пробелов:
    def test_data_strips(self, request, data, status_code):
        cookies = get_auth_token()
        favorite_place = requests.post(URL, cookies=cookies, data=data)
        response_str = favorite_place.content.decode()
        response = eval(response_str)
        actual_status_code = favorite_place.status_code

        if 'set1' in request.node.keywords:
            removed_spaces = data['title'].strip()
            response_spaces = response['title']
            assert removed_spaces == response_spaces, f"Ожидание: '{removed_spaces}', Реальность: '{response_spaces}'"
        if 'set2' in request.node.keywords:
            removed_spaces = float(data['lat'])
            response_spaces = response['lat']
            assert removed_spaces == response_spaces, f"Ожидание: '{removed_spaces}', Реальность: '{response_spaces}'"
        if 'set3' in request.node.keywords:
            removed_spaces = float(data['lon'])
            response_spaces = response['lon']
            assert removed_spaces == response_spaces, f"Ожидание: '{removed_spaces}', Реальность: '{response_spaces}'"
        if 'set4' in request.node.keywords:
            if '"color": "YELLOW"' not in response_str:
                assert False, f"Ожидается ключ 'color' в ответе, Фактически: {response}"
            else:
                removed_spaces = data['color'].strip()
                response_spaces = response['color']
                assert removed_spaces == response_spaces, f"Ожидание: '{removed_spaces}', Реальность: '{response_spaces}'"
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

        ],
        # Идентификаторы для каждого набора тестовых данных:
        ids=["set1: without token", "set2: invalid token"]
    )
    #Проверяем отправку валидных данных без токена и с протухшим токеном
    def test_send_invalid_token(self, data, status_code, message, cookies):
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
                marks=pytest.mark.set3),
            pytest.param(
                {
                    'title': '峠',
                    'lat': 55.028254,
                    'lon': 82.918501,
                    'color': 'BLUE'
                }, 400, "Параметр 'title'  Может содержать латинские и кириллические символы, цифры и знаки препинания",
                marks=pytest.mark.set4)
        ],
        # Идентификаторы для каждого набора тестовых данных:
        ids=["set1: blank title", "set2: 1000 characters", "set3: unacceptable symbols", "set4: Chinese character"]
    )
    def test_negative_title(self, data, status_code, message):
        cookies = get_auth_token()
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
        ],
        # Идентификаторы для каждого набора тестовых данных:
        ids=["set1: lat-'a'", "set2: lon-'a'", "set3: lat > 90", "set4: lon > 180", "set5: lat < -90",
             "set6: lon < -180"]
    )
    def test_negative_lat_lon(self, data, status_code, message):
        cookies = get_auth_token()
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
        ],
        # Идентификаторы для каждого набора тестовых данных:
        ids=["set1: color='WHITE'", "set2: color-int", "set3: color - not uppercase letters", "set4: color='Text'"]
    )
    def test_negative_colors(self, data, status_code, message):
        cookies = get_auth_token()
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
