# Generated by Django 2.1.2 on 2019-08-12 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('numbergame', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='State',
            new_name='CALLectorGames',
        ),
        migrations.RenameField(
            model_name='callectorgames',
            old_name='current',
            new_name='laststate',
        ),
    ]