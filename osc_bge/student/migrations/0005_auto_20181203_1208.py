# Generated by Django 2.0.9 on 2018-12-03 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_graduatestudentreview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentstudentreview',
            name='student',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='graduatestudentreview',
            name='student',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]