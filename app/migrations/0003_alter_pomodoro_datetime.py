# Generated by Django 4.1.2 on 2022-10-18 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_usertoken_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pomodoro',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
