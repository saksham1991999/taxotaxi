# Generated by Django 2.2 on 2020-05-11 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20200511_1806'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ride_booking',
            old_name='inital_charges',
            new_name='initial_charges',
        ),
    ]
