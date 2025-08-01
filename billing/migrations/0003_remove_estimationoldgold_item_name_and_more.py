# Generated by Django 4.2.4 on 2024-08-30 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_alter_billingdetails_created_by_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estimationoldgold',
            name='item_name',
        ),
        migrations.AddField(
            model_name='estimationoldgold',
            name='old_reduce_weight',
            field=models.FloatField(default=0.0, verbose_name='Old Reduce Weight'),
        ),
        migrations.AddField(
            model_name='estimationoldgold',
            name='old_touch',
            field=models.FloatField(default=0.0, verbose_name='Old Touch'),
        ),
    ]
