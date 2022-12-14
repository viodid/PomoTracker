# Generated by Django 4.1.2 on 2022-12-09 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_usersettings_breakcolor_usersettings_focuscolor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersettings',
            name='startSound',
            field=models.CharField(choices=[('#ding', 'ding'), ('#nana', 'nanana')], default='#ding', max_length=16),
        ),
        migrations.AlterField(
            model_name='usersettings',
            name='stopSound',
            field=models.CharField(choices=[('#minion', 'minion'), ('#whoose', 'whoose')], default='#whoose', max_length=16),
        ),
    ]
