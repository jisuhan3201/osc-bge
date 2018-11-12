# Generated by Django 2.0.9 on 2018-11-10 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_auto_20181110_1717'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParentInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('wechat', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='student',
            name='address',
        ),
        migrations.RemoveField(
            model_name='student',
            name='country',
        ),
        migrations.RemoveField(
            model_name='student',
            name='grade',
        ),
        migrations.RemoveField(
            model_name='student',
            name='major',
        ),
        migrations.RemoveField(
            model_name='student',
            name='parentemail',
        ),
        migrations.RemoveField(
            model_name='student',
            name='parentname',
        ),
        migrations.RemoveField(
            model_name='student',
            name='parentphone',
        ),
        migrations.RemoveField(
            model_name='student',
            name='parentwechat',
        ),
        migrations.RemoveField(
            model_name='studenthistory',
            name='abroad_year',
        ),
        migrations.RemoveField(
            model_name='studenthistory',
            name='ibt',
        ),
        migrations.RemoveField(
            model_name='studenthistory',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='studenthistory',
            name='is_school_active',
        ),
        migrations.RemoveField(
            model_name='studenthistory',
            name='past_eng',
        ),
        migrations.RemoveField(
            model_name='studenthistory',
            name='past_gpa',
        ),
        migrations.RemoveField(
            model_name='studenthistory',
            name='school',
        ),
        migrations.AddField(
            model_name='studenthistory',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='studenthistory',
            name='apply_grade',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='studenthistory',
            name='current_grade',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='studenthistory',
            name='eng_level',
            field=models.CharField(blank=True, max_length=140, null=True),
        ),
        migrations.AddField(
            model_name='studenthistory',
            name='toefl',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='studenthistory',
            name='toefljr',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.CharField(max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='phone',
            field=models.CharField(blank=True, max_length=140, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='status',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='wechat',
            field=models.CharField(blank=True, max_length=140, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='parent_info',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.ParentInfo'),
        ),
    ]