from django.db import models

# Create your models here.

class Vacancy(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True, null=True)
    skill = models.ManyToManyField('Skill',null=True, blank=True)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name

    
