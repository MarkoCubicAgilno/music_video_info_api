# Generated by Django 4.0.6 on 2022-08-22 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_alter_musicvideo_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musicvideo',
            name='song_description',
            field=models.CharField(default='No info', max_length=1000),
        ),
    ]
