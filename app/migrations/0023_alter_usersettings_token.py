# Generated by Django 4.1.2 on 2022-12-31 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_alter_usersettings_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersettings',
            name='token',
            field=models.CharField(default='KV7AL0P96f-qvHyAiDxp2Q', max_length=27, null=True),
        ),
    ]