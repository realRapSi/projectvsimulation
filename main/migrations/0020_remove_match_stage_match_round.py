# Generated by Django 4.0.2 on 2022-03-14 21:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_rename_round_match_stage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='stage',
        ),
        migrations.AddField(
            model_name='match',
            name='round',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.round'),
        ),
    ]
