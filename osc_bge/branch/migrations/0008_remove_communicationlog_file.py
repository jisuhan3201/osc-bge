# Generated by Django 2.0.9 on 2018-12-06 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0007_auto_20181206_1309'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='communicationlog',
            name='file',
        ),
    ]