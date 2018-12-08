# Generated by Django 2.0.9 on 2018-12-08 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_auto_20181203_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='status',
            field=models.CharField(blank=True, choices=[('unregistered', 'Unregistered'), ('registered', 'Registered'), ('transferred', 'Transferred')], default='unregistered', max_length=80, null=True),
        ),
    ]
