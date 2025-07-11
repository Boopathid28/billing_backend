# Generated by Django 4.2.4 on 2024-08-20 14:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=100, unique=True, verbose_name='Department name')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(null=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(null=True, verbose_name='Modified at')),
                ('modified_by', models.CharField(max_length=50, null=True, verbose_name='Modified By')),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
            ],
            options={
                'verbose_name': 'department',
                'verbose_name_plural': 'departments',
                'db_table': 'departments',
            },
        ),
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation_name', models.CharField(max_length=100, unique=True, verbose_name='Designation name')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(null=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(null=True, verbose_name='Modified at')),
                ('modified_by', models.CharField(max_length=50, null=True, verbose_name='Modified By')),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
            ],
            options={
                'verbose_name': 'designation',
                'verbose_name_plural': 'designations',
                'db_table': 'designations',
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff_id', models.CharField(max_length=100, unique=True, verbose_name='Staff id,')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Last Name')),
                ('email', models.EmailField(blank=True, max_length=60, null=True, unique=True, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='Phone no')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='City')),
                ('state', models.CharField(blank=True, max_length=100, null=True, verbose_name='State')),
                ('country', models.CharField(blank=True, max_length=100, null=True, verbose_name='Country')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='Address')),
                ('pincode', models.CharField(blank=True, max_length=10, null=True, verbose_name='Pincode')),
                ('aadhar_card', models.CharField(blank=True, max_length=500, null=True, verbose_name='Aadhar card')),
                ('pan_card', models.CharField(blank=True, max_length=500, null=True, verbose_name='Pan card')),
                ('user', models.CharField(blank=True, max_length=50, null=True, verbose_name='User')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(blank=True, null=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(blank=True, null=True, verbose_name='Modified at')),
                ('modified_by', models.CharField(blank=True, max_length=50, null=True, verbose_name='Modified By')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.branch', verbose_name='Branch')),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organizations.department', verbose_name='Department')),
                ('designation', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organizations.designation', verbose_name='Designation')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.location', verbose_name='Location')),
            ],
            options={
                'verbose_name': 'staff',
                'verbose_name_plural': 'staffs',
                'db_table': 'staffs',
            },
        ),
    ]
