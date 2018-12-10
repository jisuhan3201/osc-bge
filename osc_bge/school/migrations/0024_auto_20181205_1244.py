# Generated by Django 2.0.9 on 2018-12-05 12:44

from django.db import migrations, models
import django.db.models.deletion
import osc_bge.school.models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0023_auto_20181205_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=osc_bge.school.models.school_directory_path),
        ),
        migrations.AlterField(
            model_name='school',
            name='provider_branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='schools', to='bge.BgeBranch'),
        ),
    ]