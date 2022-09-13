# Generated by Django 4.0.6 on 2022-09-05 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_alter_artist_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='description',
            field=models.TextField(max_length=1200),
        ),
        migrations.AlterField(
            model_name='artist',
            name='image',
            field=models.TextField(max_length=1200),
        ),
        migrations.AlterField(
            model_name='musicvideo',
            name='image',
            field=models.TextField(max_length=1200),
        ),
        migrations.AlterField(
            model_name='musicvideo',
            name='song_description',
            field=models.TextField(default='No info', max_length=1200),
        ),
    ]
