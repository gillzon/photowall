# Generated by Django 3.0.3 on 2020-02-23 15:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_photos_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photos',
            name='slug',
        ),
        migrations.AlterField(
            model_name='photos',
            name='photo_room_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])]),
        ),
    ]
