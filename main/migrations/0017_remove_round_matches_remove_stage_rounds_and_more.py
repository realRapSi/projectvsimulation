# Generated by Django 4.0.2 on 2022-03-14 21:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_round_stage_tournament'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='round',
            name='matches',
        ),
        migrations.RemoveField(
            model_name='stage',
            name='rounds',
        ),
        migrations.RemoveField(
            model_name='tournament',
            name='stage',
        ),
        migrations.AddField(
            model_name='match',
            name='round',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.stage'),
        ),
        migrations.AddField(
            model_name='round',
            name='stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.stage'),
        ),
        migrations.AddField(
            model_name='stage',
            name='tournament',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.tournament'),
        ),
        migrations.CreateModel(
            name='LadderMatch',
            fields=[
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('type', models.CharField(default='', max_length=200)),
                ('number', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=200)),
                ('date', models.DateTimeField(blank=True)),
                ('teamA_score', models.IntegerField(default=0)),
                ('teamB_score', models.IntegerField(default=0)),
                ('match_type', models.CharField(blank=True, max_length=200)),
                ('compute', models.BooleanField(default=False)),
                ('teamA', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_team_A', to='main.team')),
                ('teamB', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_team_B', to='main.team')),
            ],
        ),
    ]
