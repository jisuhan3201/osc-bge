# Generated by Django 2.0.9 on 2018-12-13 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0017_auto_20181213_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentmonthlyreport',
            name='counseling_date',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]