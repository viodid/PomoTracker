# Generated by Django 4.1.2 on 2022-10-18 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_pomodoro_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='tag',
            field=models.CharField(max_length=24, unique=True),
        ),
    ]
