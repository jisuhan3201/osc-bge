# Generated by Django 2.0.9 on 2018-11-24 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0045_auto_20181123_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counsel',
            name='student',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.Student'),
        ),
    ]
