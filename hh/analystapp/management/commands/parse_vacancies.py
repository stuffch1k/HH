from django.core.management import BaseCommand

import multiprocessing

import pandas as pd
import requests
import datetime

from analystapp.models import Vacancy
from analystapp.models import Skill

API_URL = 'https://api.hh.ru/{}'
HEADER = {"User-Agent": "HHRu_Parser/1.0 (volkov03dima@gmail.com)"}

class Command(BaseCommand):

    help = "Парсит все по возможности вакансии с hh.ru"

    def handle(self, *args, **options):
        print("Заглушка")
        # date_from = datetime.datetime.now() - datetime.timedelta(days=30)
        # time = pd.date_range(date_from, datetime.datetime.now(), freq="H")
        #
        # times = []
        # for i, t in enumerate(time):
        #     if i + 1 < len(time): times.append([t, time[i + 1]])
        #
        # pool = multiprocessing.Pool(multiprocessing.cpu_count())
        # pool.map_async(self.get_task, times, callback=self.on_end_parse)
        # pool.close()
        # pool.join()

    def get_task(self, freq):
        result = []
        for p in range(0, 20 + 1):
            out = self.get_post(freq[0], freq[1], p)
            if len(out) == 0: break
            result += out
        return result

    def get_post(self, date_from, date_to, page=0):
        params = {
            'specialization': 1,
            'per_page': 100,
            'page': page,
            'date_from': date_from.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'date_to': date_to.strftime('%Y-%m-%dT%H:%M:%S%z'),
        }
        resp = requests.get(API_URL.format('vacancies'), headers=HEADER, params=params)
        return resp.json()['items'] if 'items' in resp.json() else []

    def on_end_parse(self, response):
        print("Заглушка")
        # for resp in response:
        #     for r in resp:
        #         for ks in r['key_skills']: Skill.objects.update_or_create(name=ks['name'])
        #         Vacancy.objects.create(
        #             name=r['name'],
        #             description=r['description']
        #         )