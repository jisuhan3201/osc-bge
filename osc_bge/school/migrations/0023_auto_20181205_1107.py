# Generated by Django 2.0.9 on 2018-12-05 11:07

from django.db import migrations, models
import osc_bge.school.models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0022_auto_20181204_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=osc_bge.school.models.school_directory_path),
        ),
    ]
