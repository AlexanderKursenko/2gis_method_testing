Для запуска тестов необходимо запустить виртуальное окружение и открыть главную папку проекта, где лежит файл "test_creating_a_favorite_place.py".
Запуск всех тестов:
  pytest -v
Запуск положительных или отрицательных сценариев:
  Положительные и отрицательные сценарии объединены в классы TestPositiveScripts и TestNegativeScripts.
  Для запуска всех положительных или отрицательных сценариев, необходимо обратиться к имени класса:
  pytest test_creating_a_favorite_place.py::TestPositiveScripts -v
Запуск отдельных тестов:
  Чтобы запустить проверку отдельных элементов, например широты и долготы, необходимо внутри класса обратиться к функции, проверяющей широту и долготу:
  pytest test_creating_a_favorite_place.py::TestPositiveScripts::test_lat_lon -v
Запуск отдельного тестового случая:
  В каждом тесте присутствует от 1 до n тестовых случаев, при запуске теста(функции), функция прогоняет все тестовые случаи.
  Для того, чтобы запустить определённый тестовый случай, необходимо использовать флаг "-m" и номер сета "set1", например:
  pytest test_creating_a_favorite_place.py::TestNegativeScripts::test_negative_colors -m set1 -v
  Чтобы исключить 1 или несколько тестовых случаев, необходимо использовать конструкцию '-k "not set1"' или '-k "not set1 and not set2"', например:
  pytest test_creating_a_favorite_place.py::TestNegativeScripts::test_negative_colors -k "not set1 and not set2" -v