# Generated by Django 4.1.2 on 2022-10-18 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertoken',
            name='token',
            field=models.CharField(max_length=27, null=True),
        ),
    ]
