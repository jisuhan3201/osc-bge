# Generated by Django 2.0.9 on 2018-12-11 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_studentmonthlyreport'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentmonthlyreport',
            name='chemh_current',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='studentmonthlyreport',
            name='chemh_lv',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='studentmonthlyreport',
            name='chemh_tg',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]