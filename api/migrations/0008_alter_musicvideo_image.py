# Generated by Django 4.0.6 on 2022-08-15 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_uservideolist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musicvideo',
            name='image',
            field=models.CharField(max_length=255),
        ),
    ]
