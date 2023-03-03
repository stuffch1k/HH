# Generated by Django 4.1.7 on 2023-03-03 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analystapp', '0002_remove_vacancy_skill_vacancy_skill'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfessionalRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hh_id', models.CharField(db_index=True, max_length=15)),
                ('name', models.CharField(db_index=True, max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='vacancy',
            name='hh_id',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='skill',
            field=models.ManyToManyField(blank=True, to='analystapp.skill'),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='professional_roles',
            field=models.ManyToManyField(blank=True, to='analystapp.professionalrole'),
        ),
    ]
