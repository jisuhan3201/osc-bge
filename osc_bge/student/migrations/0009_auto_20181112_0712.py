# Generated by Django 2.0.9 on 2018-11-12 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_auto_20181111_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='status',
            field=models.CharField(blank=True, choices=[('unregistered', 'Unregistered'), ('registered', 'Registered')], default='unregistered', max_length=80, null=True),
        ),
    ]