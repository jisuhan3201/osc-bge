# Generated by Django 2.0.9 on 2018-12-23 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0047_schoolcommunicationlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='school_file',
            field=models.FileField(blank=True, null=True, upload_to='informations/schools/'),
        ),
    ]
