# Generated by Django 2.0.9 on 2018-12-06 13:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0006_auto_20181206_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communicationlog',
            name='writer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
