# Generated by Django 2.0.9 on 2018-12-23 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0048_school_school_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='secondary',
            name='accepted_college',
            field=models.TextField(blank=True, null=True),
        ),
    ]
