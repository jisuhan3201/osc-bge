# Generated by Django 2.0.9 on 2018-11-28 16:18

from django.db import migrations, models
import django.db.models.deletion
import osc_bge.form.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccommodationFormality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('with_animal', models.NullBooleanField()),
                ('with_child', models.NullBooleanField()),
                ('with_other_student', models.NullBooleanField()),
                ('other_preference', models.TextField(blank=True, null=True)),
                ('application_at', models.DateTimeField(blank=True, null=True)),
                ('recommendation_a', models.FileField(blank=True, null=True, upload_to=osc_bge.form.models.accommodation_directory_path)),
                ('recommendation_a_comment', models.CharField(blank=True, max_length=255, null=True)),
                ('recommendation_b', models.FileField(blank=True, null=True, upload_to=osc_bge.form.models.accommodation_directory_path)),
                ('recommendation_c', models.FileField(blank=True, null=True, upload_to=osc_bge.form.models.accommodation_directory_path)),
                ('recommendation_b_comment', models.CharField(blank=True, max_length=255, null=True)),
                ('homestay_recommendation_at', models.DateTimeField(blank=True, null=True)),
                ('host_selection', models.CharField(blank=True, choices=[('a', 'A-Host'), ('b', 'B-Host'), ('c', 'C-Host')], max_length=140, null=True)),
                ('host_selection_at', models.DateTimeField(blank=True, null=True)),
                ('parent_accommodation_guest_num', models.CharField(blank=True, max_length=80, null=True)),
                ('parent_length_of_stay', models.CharField(blank=True, max_length=80, null=True)),
                ('parent_other_preference', models.TextField(blank=True, null=True)),
                ('parent_accommodation_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Counsel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('counseling_date', models.DateField(blank=True, null=True)),
                ('desire_country', models.CharField(blank=True, max_length=80, null=True)),
                ('program_interested', models.CharField(blank=True, max_length=255, null=True)),
                ('possibility', models.CharField(blank=True, max_length=80, null=True)),
                ('expected_departure', models.DateField(blank=True, null=True)),
                ('client_class', models.CharField(blank=True, max_length=80, null=True)),
                ('detail', models.TextField(null=True)),
                ('contact_first', models.CharField(blank=True, max_length=140, null=True)),
                ('contact_second', models.CharField(blank=True, max_length=140, null=True)),
                ('contact_third', models.CharField(blank=True, max_length=140, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Formality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('payment_complete', models.NullBooleanField()),
                ('apply_at', models.DateTimeField(blank=True, null=True)),
                ('canceled_at', models.DateTimeField(blank=True, null=True)),
                ('cancel_reason', models.TextField(blank=True, null=True)),
                ('visa_reserve_date', models.DateField(blank=True, null=True)),
                ('visa_reserve_time', models.TimeField(blank=True, null=True)),
                ('visa_granted_date', models.DateField(blank=True, null=True)),
                ('visa_granted_time', models.TimeField(blank=True, null=True)),
                ('visa_copy_recieved', models.NullBooleanField()),
                ('visa_rejected_date', models.DateField(blank=True, null=True)),
                ('visa_rejected_time', models.TimeField(blank=True, null=True)),
                ('eticket_attached', models.NullBooleanField()),
                ('air_departure_date', models.DateField(blank=True, null=True)),
                ('air_departure_time', models.TimeField(blank=True, null=True)),
                ('air_departure_port', models.CharField(blank=True, max_length=140, null=True)),
                ('air_arrive_date', models.DateField(blank=True, null=True)),
                ('air_arrive_time', models.TimeField(blank=True, null=True)),
                ('air_arrive_port', models.CharField(blank=True, max_length=140, null=True)),
                ('pickup_num', models.CharField(blank=True, max_length=80, null=True)),
                ('departure_ot', models.DateField(blank=True, null=True)),
                ('departure_confirmed', models.DateField(blank=True, null=True)),
                ('counsel', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='formality', to='form.Counsel')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='FormalityFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, max_length=140, null=True)),
                ('file_source', models.FileField(blank=True, null=True, upload_to=osc_bge.form.models.file_directory_path)),
                ('formality', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='formality_file', to='form.Formality')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SchoolFormality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('school_priority', models.SmallIntegerField(blank=True, null=True)),
                ('class_start_at', models.DateField(blank=True, null=True)),
                ('course', models.CharField(blank=True, max_length=80, null=True)),
                ('processing_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('processing_fee_done', models.NullBooleanField()),
                ('enrolment_apply_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('enrolment_apply_done', models.NullBooleanField()),
                ('enrolment_apply_done_date', models.DateTimeField(blank=True, null=True)),
                ('prepared_passport', models.NullBooleanField()),
                ('prepared_transcript', models.NullBooleanField()),
                ('prepared_eng_exams', models.NullBooleanField()),
                ('prepared_recommendation', models.NullBooleanField()),
                ('prepared_essay', models.NullBooleanField()),
                ('school_interview_date', models.DateField(blank=True, null=True)),
                ('school_interview_time', models.TimeField(blank=True, null=True)),
                ('mock_interview', models.NullBooleanField()),
                ('school_interview_done', models.NullBooleanField()),
                ('acceptance_date', models.DateField(blank=True, null=True)),
                ('acceptance_letter', models.NullBooleanField()),
                ('cancel_enrolment_date', models.DateField(blank=True, null=True)),
                ('cancel_enrolment_time', models.TimeField(blank=True, null=True)),
                ('i20_completed', models.NullBooleanField()),
                ('i20_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('i20_receipt', models.NullBooleanField()),
                ('i20_received_date', models.DateField(blank=True, null=True)),
                ('i20_copy', models.NullBooleanField()),
                ('i20_tracking', models.CharField(blank=True, max_length=255, null=True)),
                ('provider_application', models.NullBooleanField()),
                ('bge_program_application', models.NullBooleanField()),
                ('immunization', models.NullBooleanField()),
                ('financial_support', models.NullBooleanField()),
                ('program_fee_completed', models.NullBooleanField()),
                ('program_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('program_fee_receipt', models.NullBooleanField()),
                ('formality', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='school_formality', to='form.Formality')),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.School')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
