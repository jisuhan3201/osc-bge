# Generated by Django 2.0.9 on 2018-11-13 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0011_auto_20181113_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formality',
            name='departure_complete',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='formality',
            name='is_allergy',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='formality',
            name='is_child',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='formality',
            name='is_pet',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='formality',
            name='payment_complete',
            field=models.NullBooleanField(),
        ),
    ]
