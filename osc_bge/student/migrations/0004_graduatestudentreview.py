# Generated by Django 2.0.9 on 2018-12-01 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0012_auto_20181201_1011'),
        ('student', '0003_currentstudentreview'),
    ]

    operations = [
        migrations.CreateModel(
            name='GraduateStudentReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('attended', models.CharField(blank=True, max_length=80, null=True)),
                ('init_eng', models.CharField(blank=True, max_length=80, null=True)),
                ('gpa_china', models.CharField(blank=True, max_length=80, null=True)),
                ('toefl', models.CharField(blank=True, max_length=80, null=True)),
                ('gpa', models.CharField(blank=True, max_length=80, null=True)),
                ('sat_act', models.CharField(blank=True, max_length=80, null=True)),
                ('activities', models.CharField(blank=True, max_length=80, null=True)),
                ('college', models.CharField(blank=True, max_length=80, null=True)),
                ('major', models.CharField(blank=True, max_length=80, null=True)),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.School')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.Student')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]