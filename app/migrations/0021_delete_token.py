# Generated by Django 4.1.4 on 2022-12-28 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_remove_token_token_usersettings_token'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Token',
        ),
    ]
