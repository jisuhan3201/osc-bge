# Generated by Django 2.0.9 on 2018-12-06 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0005_auto_20181206_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostfamily',
            name='host_coordi',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='host', to='users.BgeBranchCoordinator'),
        ),
    ]
