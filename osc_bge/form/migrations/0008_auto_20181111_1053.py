# Generated by Django 2.0.9 on 2018-11-11 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0007_auto_20181111_1038'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='counsel',
            options={'ordering': ['-created_at']},
        ),
    ]
