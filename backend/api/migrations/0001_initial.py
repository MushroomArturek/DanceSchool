# Generated by Django 5.1.5 on 2025-02-06 23:58

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='Imię instruktora', max_length=50)),
                ('last_name', models.CharField(help_text='Nazwisko instruktora', max_length=50)),
                ('email', models.EmailField(help_text='E-mail kontaktowy', max_length=254, unique=True)),
                ('specialization', models.CharField(blank=True, help_text='Specjalizacja (np. Salsa, Tango)', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('role', models.CharField(choices=[('student', 'Student'), ('instructor', 'Instructor'), ('admin', 'Admin')], default='student', help_text='Rola użytkownika w systemie', max_length=50)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('style', models.CharField(help_text='Styl tańca (np. Salsa, Waltz)', max_length=100)),
                ('max_participants', models.PositiveIntegerField(help_text='Maksymalna liczba uczestników')),
                ('start_time', models.DateTimeField(help_text='Data i czas rozpoczęcia zajęć')),
                ('end_time', models.DateTimeField(help_text='Data i czas zakończenia zajęć')),
                ('room', models.CharField(blank=True, help_text='Sala zajęciowa', max_length=50, null=True)),
                ('instructor', models.ForeignKey(help_text='Wybierz instruktora spośród istniejących', on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='api.instructor')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('date_of_birth', models.DateField()),
                ('joined_date', models.DateField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('confirmed', 'Potwierdzona'), ('cancelled', 'Anulowana'), ('waiting', 'Oczekująca')], default='confirmed', max_length=20)),
                ('class_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='api.class')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='api.student')),
            ],
            options={
                'unique_together': {('student', 'class_model')},
            },
        ),
    ]
