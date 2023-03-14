from django.core.management import BaseCommand
import pandas as pd
import datetime

from .getting import *
from .saving import *


class Command(BaseCommand):
    help = "Парсит все по возможности вакансии с hh.ru"

    def add_arguments(self, parser):
        parser.add_argument('days', default=15, type=int)

    def handle(self, *args, **options):
        self.stdout.write("Начало парсинга вакансий")
        self.PR = []

        # Получить все IT профессии
        self.PR = Query().get_all_profession()

        date_from = datetime.datetime.now() - datetime.timedelta(days=options['days'])
        time = pd.date_range(date_from, datetime.datetime.now(), freq="H")

        for i, t in enumerate(time):
            if i + 1 < len(time):
                self.stdout.write(self.style.SUCCESS(f"Начало работы задачи номер {i}"))
                # если страниц несколько
                for p in range(0, 20 + 1):
                    if len(Saving().get_post(t, time[i+1], p)) == 0:
                        break

        self.stdout.write(self.style.SUCCESS("Конец работы"))
