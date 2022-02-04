# Generated by Django 3.2.9 on 2021-11-28 05:04

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('client_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('short_name', models.CharField(max_length=4)),
                ('description', models.CharField(max_length=200)),
                ('extra_fields', models.CharField(max_length=40)),
                ('is_active', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False)),
                ('updated_date', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='ClientDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=20)),
                ('created_date', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False)),
                ('client', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='case_user.client', verbose_name='case_id')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=30, unique=True)),
                ('phone_number', models.CharField(max_length=10, null=True)),
                ('address', models.CharField(max_length=40, null=True)),
                ('password', models.CharField(max_length=32)),
                ('notify', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user_type', models.TextField(choices=[('client_user', 'Client User'), ('internal_user', 'Internal User'), ('admin_user', 'Admin User')], default='internal_user')),
                ('created_date', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False)),
                ('updated_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_login', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('client', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='case_user.client', verbose_name='client_id')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
