# Generated by Django 2.0.9 on 2018-12-12 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0014_studentmonthlyreport_report_to_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/students/'),
        ),
    ]
