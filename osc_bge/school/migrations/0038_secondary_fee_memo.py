# Generated by Django 2.0.9 on 2018-12-12 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0037_auto_20181210_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='secondary',
            name='fee_memo',
            field=models.TextField(blank=True, null=True),
        ),
    ]
