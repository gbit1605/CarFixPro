# Generated by Django 4.2.5 on 2023-11-14 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_setup', '0010_alter_technicianinfo_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='technicianinfo',
            name='hourly_rate',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
    ]
