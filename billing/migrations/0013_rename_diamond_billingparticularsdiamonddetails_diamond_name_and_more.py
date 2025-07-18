# Generated by Django 4.2.4 on 2024-09-10 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tagging', '0001_initial'),
        ('billing', '0012_alter_billingparticulardetails_gst_percent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='billingparticularsdiamonddetails',
            old_name='diamond',
            new_name='diamond_name',
        ),
        migrations.RenameField(
            model_name='billingparticularstonedetails',
            old_name='stone',
            new_name='stone_name',
        ),
        migrations.RemoveField(
            model_name='billingparticularsdiamonddetails',
            name='reduce_weight',
        ),
        migrations.RemoveField(
            model_name='billingparticularstonedetails',
            name='reduce_weight',
        ),
        migrations.AddField(
            model_name='billingparticularsdiamonddetails',
            name='diamond_rate',
            field=models.FloatField(blank=True, max_length=50, null=True, verbose_name='Diamond Rate'),
        ),
        migrations.AddField(
            model_name='billingparticularsdiamonddetails',
            name='diamond_rate_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='tagging.ratetype', verbose_name='Rate Type'),
        ),
        migrations.AddField(
            model_name='billingparticularsdiamonddetails',
            name='diamond_weight_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='tagging.stoneweighttype', verbose_name='Weight Type'),
        ),
        migrations.AddField(
            model_name='billingparticularsdiamonddetails',
            name='include_stone_weight',
            field=models.BooleanField(default=True, verbose_name='Include Stone Weight'),
        ),
        migrations.AddField(
            model_name='billingparticularstonedetails',
            name='include_stone_weight',
            field=models.BooleanField(default=True, verbose_name='Include Stone Weight'),
        ),
        migrations.AddField(
            model_name='billingparticularstonedetails',
            name='stone_rate',
            field=models.FloatField(blank=True, max_length=50, null=True, verbose_name='Stone Rate'),
        ),
        migrations.AddField(
            model_name='billingparticularstonedetails',
            name='stone_rate_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='tagging.ratetype', verbose_name='Rate Type'),
        ),
        migrations.AddField(
            model_name='billingparticularstonedetails',
            name='stone_weight_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='tagging.stoneweighttype', verbose_name='Weight Type'),
        ),
        migrations.AlterField(
            model_name='billingparticularsdiamonddetails',
            name='diamond_weight',
            field=models.FloatField(blank=True, max_length=50, null=True, verbose_name='Diamond Weight'),
        ),
    ]
