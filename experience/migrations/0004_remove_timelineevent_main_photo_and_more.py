# Generated by Django 4.2 on 2025-04-11 03:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experience', '0003_remove_timelineevent_icon_class_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timelineevent',
            name='main_photo',
        ),
        migrations.RemoveField(
            model_name='timelineevent',
            name='photo_1',
        ),
        migrations.RemoveField(
            model_name='timelineevent',
            name='photo_2',
        ),
        migrations.RemoveField(
            model_name='timelineevent',
            name='photo_3',
        ),
        migrations.RemoveField(
            model_name='timelineevent',
            name='photo_4',
        ),
        migrations.RemoveField(
            model_name='timelineevent',
            name='photo_5',
        ),
        migrations.RemoveField(
            model_name='timelineevent',
            name='photo_6',
        ),
        migrations.RemoveField(
            model_name='timelineevent',
            name='social_link',
        ),
    ]
