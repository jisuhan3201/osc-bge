# Generated by Django 2.0.9 on 2018-12-16 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0042_auto_20181216_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='college',
            name='acceptance_percent',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]