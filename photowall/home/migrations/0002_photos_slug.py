# Generated by Django 3.0.3 on 2020-02-23 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photos',
            name='slug',
            field=models.CharField(default=1, max_length=60),
            preserve_default=False,
        ),
    ]
