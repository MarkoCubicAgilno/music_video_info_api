# Generated by Django 4.0.6 on 2022-08-18 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_musicvideo_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='musicvideo',
            name='genre',
            field=models.CharField(choices=[('green', 'GREEN'), ('blue', 'BLUE'), ('red', 'RED'), ('orange', 'ORANGE'), ('black', 'BLACK')], default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='artist',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
