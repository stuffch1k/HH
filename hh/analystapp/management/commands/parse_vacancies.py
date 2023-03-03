from django.core.management import BaseCommand

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
        self.PR = []

        # Получить все IT профессии
        it_pr = requests.get(API_URL.format('professional_roles'), headers=HEADER).json()['categories'][7]['roles']
        for p in it_pr:
            self.PR.append(p['id'])

        # разделяем по временным интервалам
        date_from = datetime.datetime.now() - datetime.timedelta(days=options['days'])
        time = pd.date_range(date_from, datetime.datetime.now(), freq="H")

        for i, t in enumerate(time):
            if i + 1 < len(time):
                self.get_task([t, time[i + 1]], i)


        self.stdout.write(self.style.SUCCESS("Конец работы"))

    def get_task(self, freq, tnum):
        self.stdout.write(self.style.SUCCESS(f"Начало работы задачи номер {tnum}"))
        # если страниц несколько
        for p in range(0, 20 + 1):
            if len(self.get_post(freq[0], freq[1], p)) == 0:
                break

    def get_post_desc_and_skills(self, post_id):
        full_info = requests.get(API_URL.format('vacancies') + '/' + post_id, headers=HEADER).json()
        if 'error' in full_info or 'errors' in full_info:
            print(full_info)
            return
        return full_info['description'], full_info['key_skills'], full_info['professional_roles']

    def get_post(self, date_from, date_to, page=0):
        result = []
        params = {
            'professional_role': self.PR,
            'per_page': 100,
            'page': page,
            'date_from': date_from.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'date_to': date_to.strftime('%Y-%m-%dT%H:%M:%S%z'),
        }

        resp = requests.get(API_URL.format('vacancies'), headers=HEADER, params=params)
        self.stdout.write(f"Получение информации о последних 100 вакансиях")

        if 'items' in resp.json():
            for i in resp.json()['items']:
                # Если уже есть в БД - ничего не делаем
                if Vacancy.objects.filter(hh_id=i['id']).exists(): break
                # Отдельным запросом нужно получить блядские навыки
                others = self.get_post_desc_and_skills(i['id'])
                # Если нет навыков - нахуй
                if len(others[1]) == 0: break

                result.append({'name': i['name'], 'description': others[0], 'key_skills': others[1]})
                vac = Vacancy.objects.create(hh_id=i['id'], name=i['name'], description=others[0])
                for ks in others[1]: vac.skill.create(name=ks['name'])
                for pr in others[2]: vac.professional_roles.create(hh_id=pr['id'], name=pr['name'])
            self.stdout.write(f"Конец обработки 100 вакансий")
        else:
            print(resp.json())

        return result
