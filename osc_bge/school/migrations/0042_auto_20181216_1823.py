# Generated by Django 2.0.9 on 2018-12-16 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0041_auto_20181216_1724'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='college',
            name='national_univ',
        ),
        migrations.AddField(
            model_name='college',
            name='partition',
            field=models.CharField(choices=[('private', 'Private'), ('public', 'Public')], max_length=80, null=True),
        ),
    ]