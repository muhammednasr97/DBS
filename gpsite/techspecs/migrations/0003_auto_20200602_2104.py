# Generated by Django 3.0.6 on 2020-06-02 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('techspecs', '0002_auto_20200602_0718'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='attributes',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='techspecs.Post'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='features',
            field=models.ManyToManyField(related_name='_equipment_features_+', to='techspecs.Post'),
        ),
    ]
