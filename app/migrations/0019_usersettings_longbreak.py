# Generated by Django 4.1.2 on 2022-12-25 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_alter_rewards_ranks'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersettings',
            name='longBreak',
            field=models.PositiveSmallIntegerField(default=15),
        ),
    ]
