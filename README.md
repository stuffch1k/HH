# Парсер навыков с hh ru по вакансиям
## Необходимые библиотеки
Python 3.10.6 (возможно несколько версий ниже)
## Деплой
1. `git clone https://github.com/stuffch1k/HH.git`
2. `cd HH`
3. `pip3 install -r requirements.txt`
4. `python3 ./hh/manage.py parse_vacancies [days]`, где [days] - количество дней для парсинга (до 30)
5. `python3 ./hh/manage.py runserver 8000`
6. Переходим на `http://127.0.0.1:8000/` и проверяем результат