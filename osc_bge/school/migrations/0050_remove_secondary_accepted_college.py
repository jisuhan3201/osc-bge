# Generated by Django 2.0.9 on 2018-12-23 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0049_secondary_accepted_college'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='secondary',
            name='accepted_college',
        ),
    ]