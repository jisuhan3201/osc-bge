# Generated by Django 2.0.9 on 2018-12-10 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20181207_1433'),
        ('branch', '0010_auto_20181208_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='hoststudentreport',
            name='host_coordi',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.BgeBranchCoordinator'),
        ),
    ]
