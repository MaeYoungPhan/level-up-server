# Generated by Django 4.1.6 on 2023-02-10 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('levelupapi', '0002_remove_gamer_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='game_id',
            new_name='game',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='gamer_id',
            new_name='gamer',
        ),
    ]