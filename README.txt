Для запуска тестов необходимо запустить виртуальное окружение и открыть главную папку проекта, где лежит файл "test_creating_a_favorite_place.py".
Запуск всех тестов:
  pytest -v -l
Запуск положительных или отрицательных сценариев:
  Положительные и отрицательные сценарии объединены в классы TestPositiveScripts и TestNegativeScripts.
  Для запуска всех положительных или отрицательных сценариев, необходимо обратиться к имени класса:
  pytest test_creating_a_favorite_place.py::TestPositiveScripts -v -l
Запуск отдельных тестов:
  Чтобы запустить проверку отдельных элементов, например широты и долготы, необходимо внутри класса обратиться к функции, проверяющей широту и долготу:
  pytest test_creating_a_favorite_place.py::TestPositiveScripts::test_lat_lon -v -l
Запуск отдельного тестового случая:
  В каждом тесте присутствует от 1 до n наборов тестовых данных, при запуске теста(функции), функция прогоняет все тестовые случаи.
  Для того, чтобы запустить определённый набор данных, необходимо использовать флаг "-m" и номер сета "set1", например:
  pytest test_creating_a_favorite_place.py::TestNegativeScripts::test_negative_colors -m set1 -v -l
  Чтобы исключить 1 или несколько наборов тестовых данных, необходимо использовать конструкцию '-k "not set1"' или '-k "not set1 and not set2"', например:
  pytest test_creating_a_favorite_place.py::TestNegativeScripts::test_negative_colors -k "not set1 and not set2" -v -l
