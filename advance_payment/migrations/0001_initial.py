# Generated by Django 4.2.4 on 2024-08-20 14:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('masters', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvanceDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advance_id', models.CharField(max_length=150, unique=True, verbose_name='Advance ID')),
                ('total_advance_amount', models.FloatField(default=0.0, verbose_name='Total Advance Amount')),
                ('total_advance_weight', models.FloatField(default=0.0, verbose_name='Total Advance Weight')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='Remark')),
                ('is_redeemed', models.BooleanField(default=False, verbose_name='Redeem Status')),
                ('is_cancelled', models.BooleanField(default=False, verbose_name='Cancel Status')),
                ('created_at', models.DateTimeField(blank=True, null=True, verbose_name='Created at')),
            ],
            options={
                'verbose_name': 'advance_details',
                'verbose_name_plural': 'advance_details',
                'db_table': 'advance_details',
            },
        ),
        migrations.CreateModel(
            name='AdvancePurpose',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purpose_name', models.CharField(max_length=100, verbose_name='purpose Name')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(null=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(null=True, verbose_name='Modified at')),
                ('modified_by', models.CharField(max_length=50, null=True, verbose_name='Modified By')),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
            ],
            options={
                'verbose_name': 'advance_purpose',
                'verbose_name_plural': 'advance_purposes',
                'db_table': 'advance_purpose',
            },
        ),
        migrations.CreateModel(
            name='AdvanceLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('redeem_amount', models.FloatField(default=0.0, verbose_name='Redeem Amount')),
                ('redeem_weight', models.FloatField(default=0.0, verbose_name='Redeem Weight')),
                ('is_cancelled', models.BooleanField(default=False, verbose_name='Cancel Status')),
                ('advance_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advance_payment.advancedetails', verbose_name='Advance Details')),
            ],
            options={
                'verbose_name': 'advance_log_details',
                'verbose_name_plural': 'advance_log_details',
                'db_table': 'advance_log_details',
            },
        ),
        migrations.AddField(
            model_name='advancedetails',
            name='advance_purpose',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='advance_payment.advancepurpose', verbose_name='Advance Purpose'),
        ),
        migrations.AddField(
            model_name='advancedetails',
            name='advance_weight_purity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='masters.purity', verbose_name='Advance Weight Purity'),
        ),
        migrations.AddField(
            model_name='advancedetails',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.branch', verbose_name='Branch'),
        ),
        migrations.AddField(
            model_name='advancedetails',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='advancedetails',
            name='customer_details',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='customer.customer', verbose_name='Customer Details'),
        ),
    ]
