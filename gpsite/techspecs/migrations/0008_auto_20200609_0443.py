# Generated by Django 3.0.6 on 2020-06-09 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techspecs', '0007_auto_20200605_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='technical_report',
            name='addition_date',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='technical_report',
            name='modification_date',
            field=models.CharField(max_length=20),
        ),
    ]