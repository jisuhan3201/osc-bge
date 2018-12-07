# Generated by Django 2.0.9 on 2018-12-06 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0003_auto_20181206_0826'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hostfamily',
            name='next_year_plan',
        ),
        migrations.AddField(
            model_name='hoststudent',
            name='next_year_plan',
            field=models.CharField(blank=True, choices=[('same_student', 'Same-Student'), ('change_student', 'Change-student'), ('na', 'N/A'), ('a', 'A')], max_length=140, null=True),
        ),
    ]
