# Generated by Django 4.1.5 on 2023-03-02 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analystapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacancy',
            name='skill',
        ),
        migrations.AddField(
            model_name='vacancy',
            name='skill',
            field=models.ManyToManyField(blank=True, null=True, to='analystapp.skill'),
        ),
    ]
