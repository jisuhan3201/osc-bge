# Generated by Django 2.0.9 on 2018-12-25 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0028_studentacthistory_studentsathistory_studenttoeflhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentmonthlyreport',
            name='status',
            field=models.CharField(blank=True, choices=[('incomplete', 'Incomplete'), ('complete', 'Complete'), ('submitted', 'Submitted'), ('manager_confirmed', 'Manager Confirmed'), ('send_to_agent', 'Send to Agent'), ('agent_confirmed', 'Agent Confirmed')], max_length=80, null=True),
        ),
    ]
