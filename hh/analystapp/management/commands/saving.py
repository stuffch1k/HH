from django.core.management import BaseCommand
from analystapp.models import *
from .getting import *

class Saving(BaseCommand):
    def get_post(self, date_from, date_to, page=0):
        result = []

        resp = Query().get_resp(date_from,date_to,page)
        self.stdout.write(f"Получение информации о последних 100 вакансиях")

        if 'items' in resp:
            for i in resp['items']:
                # Если уже есть в БД - ничего не делаем
                if Vacancy.objects.filter(hh_id=i['id']).exists(): break
                # Отдельным запросом нужно получить блядские навыки
                others = Query().get_post_skills(i['id'])
                # Если нет навыков - нахуй
                if len(others[0]) == 0: break

                result.append({'name': i['name'], 'key_skills': others[0]})
                vac = Vacancy.objects.create(hh_id=i['id'], name=i['name'])
                for ks in others[0]: vac.skill.create(name=ks['name'])
                for pr in others[1]: vac.professional_roles.create(hh_id=pr['id'], name=pr['name'])
            self.stdout.write(f"Конец обработки 100 вакансий")
        else:
            print(resp)

        return result