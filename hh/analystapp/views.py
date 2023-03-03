from django.shortcuts import render

# Create your views here.
import analystapp.models as models


def index(request):
    return render(request, 'search.html')


def skills_rate(request):
    vac_count = models.Vacancy.objects.filter(name__contains=request.GET['vacancies_name'])
    result = {}
    for vac in vac_count:
        for skill in vac.skill.all():
            if skill.name in result: result[skill.name] += 1
            else: result[skill.name] = 1

    for i in result.items():
        result[i[0]] = (i[1] / vac_count.count()) * 100

    return render(request, 'skills_rate.html', {'stats': sorted(result.items(), key=lambda x: x[1], reverse=True)})