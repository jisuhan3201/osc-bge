# Generated by Django 2.0.9 on 2018-12-08 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0009_auto_20181206_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostfamily',
            name='status',
            field=models.CharField(blank=True, choices=[('active', 'Active'), ('inactive', 'Inactive'), ('prospective', 'Prospective')], max_length=80, null=True),
        ),
    ]
