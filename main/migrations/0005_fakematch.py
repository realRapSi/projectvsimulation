# Generated by Django 4.0.2 on 2022-02-17 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_match_match_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='FakeMatch',
            fields=[
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('compute', models.BooleanField(default=False)),
                ('points_deduction', models.IntegerField(blank=True, null=True)),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.team')),
            ],
        ),
    ]
