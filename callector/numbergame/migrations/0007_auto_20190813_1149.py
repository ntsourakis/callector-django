# Generated by Django 2.1.2 on 2019-08-13 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('numbergame', '0006_callectorgamesscores'),
    ]

    operations = [
        migrations.RenameField(
            model_name='callectorgamesscores',
            old_name='appId',
            new_name='namespace',
        ),
    ]
