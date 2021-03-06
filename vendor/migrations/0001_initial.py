# Generated by Django 2.2.10 on 2020-03-29 16:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='vendorprofile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('father_name', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.ImageField(upload_to='')),
                ('dob', models.DateField()),
                ('email', models.EmailField(max_length=254)),
                ('contact1', models.CharField(max_length=10)),
                ('contact2', models.CharField(blank=True, max_length=10, null=True)),
                ('street_1', models.CharField(max_length=100)),
                ('street_2', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=6)),
                ('pancard', models.FileField(upload_to='')),
                ('aadharcard_front', models.FileField(upload_to='')),
                ('aadharcard_rear', models.FileField(upload_to='')),
                ('votercard', models.FileField(blank=True, null=True, upload_to='')),
                ('driving_licence_front', models.FileField(blank=True, null=True, upload_to='')),
                ('driving_licence_rear', models.FileField(blank=True, null=True, upload_to='')),
                ('company_name', models.CharField(max_length=100)),
                ('gst_no', models.CharField(max_length=15)),
                ('account_name', models.CharField(max_length=50)),
                ('account_no', models.IntegerField()),
                ('bank_name', models.CharField(max_length=50)),
                ('account_type', models.CharField(choices=[('C', 'Current'), ('S', 'Saving')], max_length=1)),
                ('ifsc', models.CharField(max_length=20)),
                ('bank_address', models.CharField(max_length=200)),
                ('verified', models.BooleanField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Vendor Details',
            },
        ),
        migrations.CreateModel(
            name='vendor_cars',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_no', models.CharField(blank=True, max_length=50, null=True)),
                ('dateofregistration', models.DateField(blank=True, null=True)),
                ('image_front', models.ImageField(upload_to='')),
                ('image_rear', models.ImageField(upload_to='')),
                ('rc_front', models.FileField(upload_to='')),
                ('rc_rear', models.FileField(upload_to='')),
                ('touristpermit_front', models.FileField(upload_to='')),
                ('touristpermit_rear', models.FileField(blank=True, null=True, upload_to='')),
                ('permita_front', models.FileField(upload_to='')),
                ('permita_rear', models.FileField(blank=True, null=True, upload_to='')),
                ('permitb_front', models.FileField(upload_to='')),
                ('permitb_rear', models.FileField(blank=True, null=True, upload_to='')),
                ('insurance_front', models.FileField(upload_to='')),
                ('insurance_rear', models.FileField(blank=True, null=True, upload_to='')),
                ('pollution_certificate', models.FileField(blank=True, null=True, upload_to='')),
                ('car_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.car_types')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='vendor.vendorprofile')),
            ],
            options={
                'verbose_name_plural': 'Vendor Cars',
            },
        ),
        migrations.CreateModel(
            name='driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('father_name', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.ImageField(upload_to='')),
                ('dob', models.DateField()),
                ('driving_licence_no', models.CharField(max_length=50)),
                ('driving_licence_valid_from', models.DateField()),
                ('driving_licence_valid_till', models.DateField()),
                ('driving_experience', models.SmallIntegerField()),
                ('hill_experience', models.SmallIntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('contact1', models.CharField(max_length=10)),
                ('contact2', models.CharField(blank=True, max_length=10, null=True)),
                ('street_1', models.CharField(max_length=100)),
                ('street_2', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=6)),
                ('pancard', models.FileField(upload_to='')),
                ('aadharcard_front', models.FileField(upload_to='')),
                ('aadharcard_rear', models.FileField(upload_to='')),
                ('votercard', models.FileField(blank=True, null=True, upload_to='')),
                ('driving_licence_front', models.FileField(blank=True, null=True, upload_to='')),
                ('driving_licence_rear', models.FileField(blank=True, null=True, upload_to='')),
                ('police_verification_front', models.FileField(blank=True, null=True, upload_to='')),
                ('police_verification_rear', models.FileField(blank=True, null=True, upload_to='')),
                ('legal_accidental_case', models.BooleanField()),
                ('legal_accidental_case_details', models.TextField(blank=True, null=True)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='vendor.vendorprofile')),
            ],
        ),
    ]
