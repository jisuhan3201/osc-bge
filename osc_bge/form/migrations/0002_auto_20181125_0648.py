# Generated by Django 2.0.9 on 2018-11-25 02:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('student', '0001_initial'),
        ('form', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='counsel',
            name='counseler',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='counseling', to='users.Counseler'),
        ),
        migrations.AddField(
            model_name='counsel',
            name='student',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='counsel', to='student.Student'),
        ),
        migrations.AddField(
            model_name='accommodationformality',
            name='formality',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accommodation', to='form.Formality'),
        ),
    ]
