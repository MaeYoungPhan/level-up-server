# Generated by Django 4.1.6 on 2023-02-09 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('levelupapi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamer',
            name='username',
        ),
    ]
