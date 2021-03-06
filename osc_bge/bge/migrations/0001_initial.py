# Generated by Django 2.0.9 on 2018-11-28 16:18

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BgeBranch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('country', django_countries.fields.CountryField(max_length=2, null=True)),
                ('state', models.CharField(max_length=255, null=True)),
                ('address', models.CharField(max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
