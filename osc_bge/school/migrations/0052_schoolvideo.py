# Generated by Django 2.0.9 on 2018-12-25 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0051_school_program_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('video', models.FileField(blank=True, null=True, upload_to='videos/schools/')),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='school_video', to='school.School')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]