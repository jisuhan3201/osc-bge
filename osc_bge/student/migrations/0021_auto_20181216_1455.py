# Generated by Django 2.0.9 on 2018-12-16 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0020_auto_20181216_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentaccounting',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accounting', to='student.Student'),
        ),
    ]
