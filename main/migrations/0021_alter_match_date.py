# Generated by Django 4.0.2 on 2022-03-14 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_remove_match_stage_match_round'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
