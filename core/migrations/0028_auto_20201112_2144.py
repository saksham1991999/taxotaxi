# Generated by Django 2.2 on 2020-11-12 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20200922_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride_booking',
            name='ride_status',
            field=models.CharField(choices=[('Booked', 'Booked'), ('Rejected', 'Rejected'), ('Selected Vendors', 'Selected Vendors'), ('Assigned Vendor', 'Assigned Vendor'), ('Assigned Car/Driver', 'Assigned Car/Driver'), ('Ongoing', 'Ongoing'), ('Completed', 'Completed'), ('Verified', 'Verified'), ('Cancelled', 'Cancelled'), ('User Cancelled', 'User Cancelled')], max_length=32),
        ),
    ]