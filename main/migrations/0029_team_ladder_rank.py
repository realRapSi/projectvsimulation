# Generated by Django 4.0.2 on 2022-03-16 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_pointsystem_ladder_calculated'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='ladder_rank',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]