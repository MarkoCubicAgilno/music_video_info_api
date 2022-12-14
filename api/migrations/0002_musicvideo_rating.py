# Generated by Django 4.0.6 on 2022-08-13 14:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MusicVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=50, unique=True)),
                ('release_year', models.CharField(max_length=255)),
                ('album', models.CharField(max_length=255)),
                ('image', models.CharField(max_length=1000)),
                ('ytEmbedded', models.CharField(max_length=255)),
                ('rateScore', models.CharField(max_length=255)),
                ('votesNumber', models.CharField(max_length=255)),
                ('duration', models.CharField(max_length=255)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.artist')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('rating', models.IntegerField()),
                ('musicVideo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.musicvideo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
