# Generated by Django 4.0.6 on 2022-08-19 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('api', '0010_uservideolist_slug_alter_musicvideo_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='musicvideo',
            name='content_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='musicvideo',
            name='artist',
            field=models.PositiveIntegerField(),
        ),
    ]