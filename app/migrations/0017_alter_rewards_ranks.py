# Generated by Django 4.1.2 on 2022-12-10 15:52

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_rewards_ranks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rewards',
            name='ranks',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None), default=0, size=None),
        ),
    ]
