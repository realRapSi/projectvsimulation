# Generated by Django 4.0.2 on 2022-03-16 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_pointsystem_recalculate_ladder'),
    ]

    operations = [
        migrations.AddField(
            model_name='pointsystem',
            name='ladder_calculated',
            field=models.BooleanField(default=False),
        ),
    ]
