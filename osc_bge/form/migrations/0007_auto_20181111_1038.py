# Generated by Django 2.0.9 on 2018-11-11 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0006_auto_20181111_0601'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='counsel',
            options={'ordering': ['-counseling_date']},
        ),
    ]