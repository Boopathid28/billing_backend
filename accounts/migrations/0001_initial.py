# Generated by Django 4.2.4 on 2024-08-20 14:15

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(max_length=100, unique=True, verbose_name='Location name')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(null=True, verbose_name='Created at')),
                ('created_by', models.CharField(max_length=50, null=True, verbose_name='Modified By')),
                ('modified_at', models.DateTimeField(null=True, verbose_name='Modified at')),
                ('modified_by', models.CharField(max_length=50, null=True, verbose_name='Modified By')),
            ],
            options={
                'verbose_name': 'location',
                'verbose_name_plural': 'locations',
                'db_table': 'locations',
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=50, unique=True, verbose_name='Role name')),
                ('is_active', models.BooleanField(default=True, verbose_name='Status')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Admin Status')),
                ('created_at', models.DateTimeField(blank=True, null=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(blank=True, null=True, verbose_name='Modified at')),
            ],
            options={
                'verbose_name': 'user_role',
                'verbose_name_plural': 'user_roles',
                'db_table': 'user_roles',
            },
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_name', models.CharField(max_length=100, unique=True, verbose_name='Branch name')),
                ('branch_shortcode', models.CharField(blank=True, max_length=50, null=True, verbose_name='branch short code')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(null=True, verbose_name='Created at')),
                ('created_by', models.CharField(max_length=50, null=True, verbose_name='Modified By')),
                ('modified_at', models.DateTimeField(null=True, verbose_name='Modified at')),
                ('modified_by', models.CharField(max_length=50, null=True, verbose_name='Modified By')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.location', verbose_name='Location')),
            ],
            options={
                'verbose_name': 'branch',
                'verbose_name_plural': 'branches',
                'db_table': 'branches',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='Email')),
                ('phone', models.CharField(max_length=10, unique=True, verbose_name='Phone no')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('is_loggedin', models.BooleanField(default=False, verbose_name='Logged in')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='Last Login')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Django user')),
                ('is_staff', models.BooleanField(default=True, verbose_name='Employee')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Deleted')),
                ('created_at', models.DateTimeField(blank=True, null=True, verbose_name='Created at')),
                ('created_by', models.CharField(blank=True, max_length=50, null=True, verbose_name='Created By')),
                ('modified_at', models.DateTimeField(blank=True, null=True, verbose_name='Modified at')),
                ('modified_by', models.CharField(blank=True, max_length=50, null=True, verbose_name='Modified By')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted at')),
                ('deleted_by', models.CharField(blank=True, max_length=50, null=True, verbose_name='Deleted By')),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounts.branch', verbose_name='User Branch')),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounts.userrole', verbose_name='User Role')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'db_table': 'users',
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]
