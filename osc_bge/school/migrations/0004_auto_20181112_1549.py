# Generated by Django 2.0.9 on 2018-11-12 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_auto_20181108_1421'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='country',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='address',
            field=models.CharField(blank=True, max_length=140, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='ap_process',
            field=models.CharField(blank=True, max_length=140, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='honor_process',
            field=models.CharField(blank=True, max_length=140, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='lang',
            field=models.CharField(max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='name',
            field=models.CharField(max_length=140, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='pop_major',
            field=models.CharField(blank=True, max_length=140, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='religion',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='rep_major',
            field=models.CharField(blank=True, max_length=140, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='semester',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='setting',
            field=models.CharField(blank=True, choices=[('urban', 'Urban'), ('suburban', 'SubUrban')], max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='sort',
            field=models.CharField(choices=[('elementary', 'Elementary'), ('middle', 'Middle'), ('high', 'High'), ('college', 'College')], max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='state',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='types',
            field=models.CharField(blank=True, choices=[('private', 'Private'), ('public', 'Public'), ('only_male', 'Only-Male'), ('only_female', 'Only-Female'), ('Coed', 'Coed')], max_length=80, null=True),
        ),
    ]