# Generated by Django 2.0.9 on 2018-11-23 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0039_auto_20181123_0835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formality',
            name='pickup_num',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
