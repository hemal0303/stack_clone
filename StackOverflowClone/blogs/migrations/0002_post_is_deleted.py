# Generated by Django 4.1.7 on 2023-04-22 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
