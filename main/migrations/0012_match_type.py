# Generated by Django 4.0.2 on 2022-03-08 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_team_last_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='type',
            field=models.CharField(default='', max_length=200),
        ),
    ]
