# Generated by Django 2.0.9 on 2018-11-25 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='country',
        ),
        migrations.RemoveField(
            model_name='user',
            name='group',
        ),
        migrations.RemoveField(
            model_name='user',
            name='state',
        ),
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.CharField(blank=True, choices=[('bge_admin', 'BGE_Admin'), ('agency', 'Agency'), ('counseler', 'Counseler')], max_length=140, null=True),
        ),
    ]