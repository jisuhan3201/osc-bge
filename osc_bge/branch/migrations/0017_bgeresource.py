# Generated by Django 2.0.9 on 2018-12-13 09:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('branch', '0016_hoststudent_communication_log'),
    ]

    operations = [
        migrations.CreateModel(
            name='BgeResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('cateogry', models.CharField(blank=True, max_length=80, null=True)),
                ('sub_category', models.CharField(blank=True, max_length=80, null=True)),
                ('title', models.CharField(blank=True, max_length=140, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='resources/')),
                ('writer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
