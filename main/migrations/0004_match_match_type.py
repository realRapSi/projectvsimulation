# Generated by Django 4.0.2 on 2022-02-13 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_match_teama_alter_match_teamb'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='match_type',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
