# Generated by Django 4.2.4 on 2024-08-28 04:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
        ('refinery_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meltingissue',
            name='vendor_details',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='books.accountheaddetails', verbose_name='Vendor Details'),
        ),
        migrations.AddField(
            model_name='meltingrecipt',
            name='vendor_details',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='books.accountheaddetails', verbose_name='Vendor Details'),
        ),
        migrations.AddField(
            model_name='purificationrecipt',
            name='vendor_details',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='books.accountheaddetails', verbose_name='Vendor Details'),
        ),
        migrations.AlterField(
            model_name='purificationissue',
            name='smith',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='books.accountheaddetails', verbose_name='Smith Details'),
        ),
    ]
