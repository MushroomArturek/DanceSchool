# Generated by Django 5.1.5 on 2025-02-19 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_payment_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Gotówka'), ('transfer', 'Przelew bankowy'), ('blik', 'BLIK'), ('card', 'Karta płatnicza w studio')], max_length=20),
        ),
    ]
