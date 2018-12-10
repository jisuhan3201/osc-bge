# Generated by Django 2.0.9 on 2018-12-05 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communicationlog',
            name='host',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='branch.HostFamily'),
        ),
        migrations.AlterField(
            model_name='communicationlog',
            name='writer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.BgeBranchAdminUser'),
        ),
        migrations.AlterField(
            model_name='hostfamily',
            name='host_coordi',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.BgeBranchAdminUser'),
        ),
        migrations.AlterField(
            model_name='hoststudent',
            name='host',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='branch.HostFamily'),
        ),
        migrations.AlterField(
            model_name='hoststudentreport',
            name='host',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='branch.HostFamily'),
        ),
        migrations.AlterField(
            model_name='hoststudentreport',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.Student'),
        ),
    ]