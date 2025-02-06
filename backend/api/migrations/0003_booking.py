# Generated by Django 5.1.5 on 2025-02-03 18:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_class_instructor'),
    ]

    operations = [
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
