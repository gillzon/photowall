# Generated by Django 3.0.3 on 2020-02-23 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_createpartyroom_room_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photos',
            name='name',
        ),
        migrations.RemoveField(
            model_name='photos',
            name='photo_room',
        ),
    ]
