# Generated by Django 2.0.9 on 2018-11-10 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_auto_20181110_1700'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='parentinfo',
        ),
        migrations.RemoveField(
            model_name='student',
            name='skype',
        ),
        migrations.AddField(
            model_name='student',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='parentemail',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='parentname',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='parentphone',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='parentwechat',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='ParentInfo',
        ),
    ]
