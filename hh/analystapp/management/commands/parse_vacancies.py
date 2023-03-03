from django.core.management import BaseCommand

import threading

import pandas as pd
import requests
import datetime

from analystapp.models import Vacancy

API_URL = 'https://api.hh.ru/{}'
HEADER = {"User-Agent": "HHRu_Parser/1.0 (volkov03dima@gmail.com)"}


class Command(BaseCommand):
    help = "Парсит все по возможности вакансии с hh.ru"

    def add_arguments(self, parser):
        parser.add_argument('days', default=15, type=int)

    def handle(self, *args, **options):
        self.stdout.write("Начало парсинга вакансий")

        # разделяем по временным интервалам
        date_from = datetime.datetime.now() - datetime.timedelta(days=options['days'])
        time = pd.date_range(date_from, datetime.datetime.now(), freq="4H")

        # ебучие пи... потоки
        threads = []
        for i, t in enumerate(time):
            if i + 1 < len(time):
                t = threading.Thread(target=self.get_task, args=([t, time[i + 1]], i))
                threads.append(t)
                t.start()

        [thread.join() for thread in threads]

        self.stdout.write(self.style.SUCCESS("Конец работы"))

    def get_task(self, freq, thread_num):
        self.stdout.write(self.style.SUCCESS(f"Начало работы потока {thread_num}"))
        result = []
        # если страниц несколько
        for p in range(0, 20 + 1):
            out = self.get_post(freq[0], freq[1], p)
            if len(out) == 0: break
            result += out
        self.on_end_parse(result, thread_num)

    def get_post_desc_and_skills(self, post_id):
        full_info = requests.get(API_URL.format('vacancies') + '/' + post_id, headers=HEADER).json()
        return full_info['description'] if 'description' in full_info else "", full_info['key_skills'] if 'key_skills' in full_info else []

    def get_post(self, date_from, date_to, page=0):
        result = []
        params = {
            'specialization': 1,
            'per_page': 100,
            'page': page,
            'date_from': date_from.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'date_to': date_to.strftime('%Y-%m-%dT%H:%M:%S%z'),
        }
        resp = requests.get(API_URL.format('vacancies'), headers=HEADER, params=params)
        for i in resp.json()['items']:
            # Отдельным запросом нужно получить блядские навыки
            others = self.get_post_desc_and_skills(i['id'])
            result.append({'name': i['name'], 'description': others[0], 'key_skills': others[1]})
        return result

    def on_end_parse(self, response, tnum):
        self.stdout.write(self.style.SUCCESS(f"Завершение работы потока {tnum}"))
        # заполняем данные в бд
        for r in response:
            vac = Vacancy.objects.create(name=r['name'], description=r['description'])
            for ks in r['key_skills']: vac.skill.create(name=ks['name'])
