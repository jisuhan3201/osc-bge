# Generated by Django 2.0.9 on 2018-11-08 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_auto_20181107_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='ap_process',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='application_deadline',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='application_fee',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='school',
            name='asian_ratio',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='boarding_fee',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='school',
            name='class_num',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='club_num',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='college_pass_ratio',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='end_ena_deadline',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='end_ena_noti',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='ent_approve_ratio',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='files',
            field=models.FileField(blank=True, null=True, upload_to='school'),
        ),
        migrations.AlterField(
            model_name='school',
            name='founded',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='fulltime_teacher_ratio',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='grade',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='honor_process',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='ibt',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='itn_student_num',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='offered_grade',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='pop_major',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='program_fee',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='school',
            name='rank',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='religion',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='rep_major',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='sat25',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='sat75',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='sat_avg',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='semester',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='setting',
            field=models.CharField(blank=True, choices=[('urban', 'Urban'), ('suburban', 'SubUrban')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='state',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='student_num',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='teacher_student_ratio',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='tenpercent_ratio',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='types',
            field=models.CharField(blank=True, choices=[('private', 'Private'), ('public', 'Public'), ('only_male', 'Only-Male'), ('only_female', 'Only-Female'), ('Coed', 'Coed')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='under_twenty_ratio',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
