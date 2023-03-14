from django.db import models

# Create your models here.

class Vacancy(models.Model):
    hh_id = models.CharField(max_length=15, null=True, blank=True)
    name = models.CharField(max_length=255, db_index=True)
    professional_roles = models.ManyToManyField('ProfessionalRole', blank=True)
    skill = models.ManyToManyField('Skill', blank=True)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name


class ProfessionalRole(models.Model):
    hh_id = models.CharField(max_length=15, db_index=True)
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name
