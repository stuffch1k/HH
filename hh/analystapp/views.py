import csv
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
import analystapp.models as models


def index(request):
    return render(request, 'search.html')


def prepare_rate(vname):
    result = {}
    vac_count = models.Vacancy.objects.filter(name__contains=vname)
    for vac in vac_count:
        for skill in vac.skill.all():
            if skill.name in result:
                result[skill.name][0] += 1
            else:
                result[skill.name] = [0, 0]
                result[skill.name][0] = 1

    for i in result.items():
        result[i[0]][1] = (i[1][0] / vac_count.count()) * 100
    return sorted(result.items(), key=lambda x: x[1][0], reverse=True)


def skills_rate(request):
    return render(request, 'skills_rate.html', {
        'stats': prepare_rate(request.GET['vacancies_name']),
        'vac_count': models.Vacancy.objects.filter(name__contains=request.GET['vacancies_name']).count()
    })


def skills_rate_csv(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename="{request.GET["vacancies_name"]}.csv"'},
    )

    writer = csv.writer(response)
    for i in prepare_rate(request.GET['vacancies_name']):
        writer.writerow([i[0], i[1][0], i[1][1]])

    return response
