# Generated by Django 4.0.6 on 2022-08-13 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_rename_rating_rating_rating_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='rating_id',
            new_name='rating',
        ),
        migrations.RenameField(
            model_name='rating',
            old_name='user_id',
            new_name='user',
        ),
    ]
