# Generated by Django 2.0.9 on 2018-12-06 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20181202_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bgebranchcoordinator',
            name='position',
            field=models.CharField(choices=[('admission_coordi', 'Admission coordinator'), ('school_coordi', 'School coordinator'), ('student_coordi', 'Student coordinator'), ('host_coordi', 'Host coordinator')], max_length=255, null=True),
        ),
    ]