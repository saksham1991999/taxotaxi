# Generated by Django 2.2 on 2020-05-25 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20200511_1809'),
    ]

    operations = [
        migrations.CreateModel(
            name='TermsAndConditions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='faq',
            name='title',
            field=models.CharField(max_length=512),
        ),
    ]