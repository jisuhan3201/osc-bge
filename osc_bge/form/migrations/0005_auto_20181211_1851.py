# Generated by Django 2.0.9 on 2018-12-11 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0004_auto_20181207_0559'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='counselorsellingpoint',
            name='classification',
        ),
        migrations.RemoveField(
            model_name='counselorsellingpoint',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='counselorsellingpoint',
            name='emphasis',
        ),
        migrations.RemoveField(
            model_name='counselorsellingpoint',
            name='evaluation',
        ),
        migrations.RemoveField(
            model_name='counselorsellingpoint',
            name='information',
        ),
        migrations.AddField(
            model_name='counselorsellingpoint',
            name='admission_requirement_cm',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='counselorsellingpoint',
            name='admission_requirement_ev',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='counselorsellingpoint',
            name='ap_cm',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='counselorsellingpoint',
            name='ap_ev',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='counselorsellingpoint',
            name='application_fee_cm',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='counselorsellingpoint',
            name='application_fee_ev',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='counselorsellingpoint',
            name='clubs_cm',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='counselorsellingpoint',
            name='clubs_ev',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='counselorsellingpoint',
            name='esl_cm',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='counselorsellingpoint',
            name='esl_ev',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='counselorsellingpoint',
            name='honor_cm',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='counselorsellingpoint',
            name='honor_ev',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='counselorsellingpoint',
            name='intl_student_number_cm',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='counselorsellingpoint',
            name='intl_student_number_ev',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='counselorsellingpoint',
            name='location_cm',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='counselorsellingpoint',
            name='location_ev',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='counselorsellingpoint',
            name='program_fee_cm',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='counselorsellingpoint',
            name='program_fee_ev',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='counselorsellingpoint',
            name='sports_cm',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='counselorsellingpoint',
            name='sports_ev',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='counselorsellingpoint',
            name='student_number_cm',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='counselorsellingpoint',
            name='student_number_ev',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='counselorsellingpoint',
            name='student_teacher_ratio_cm',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='counselorsellingpoint',
            name='student_teacher_ratio_ev',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
