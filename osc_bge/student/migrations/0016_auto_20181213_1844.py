# Generated by Django 2.0.9 on 2018-12-13 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0015_auto_20181212_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='status',
            field=models.CharField(blank=True, choices=[('unregistered', 'Unregistered'), ('registered', 'Registered'), ('transferred', 'Transferred'), ('graduated', 'Graduated'), ('terminated', 'Terminated')], default='unregistered', max_length=80, null=True),
        ),
    ]
