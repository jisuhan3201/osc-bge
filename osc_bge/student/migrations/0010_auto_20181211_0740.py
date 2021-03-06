# Generated by Django 2.0.9 on 2018-12-11 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0009_auto_20181211_0708'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentmonthlyreport',
            name='agent_confirmed',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentmonthlyreport',
            name='status',
            field=models.CharField(blank=True, choices=[('incomplete', 'Incomplete'), ('submitted', 'Submiited'), ('manager_confirmed', 'Manager Confirmed'), ('agent_confirmed', 'Agent Confirmed')], max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='studentmonthlyreport',
            name='submit_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
