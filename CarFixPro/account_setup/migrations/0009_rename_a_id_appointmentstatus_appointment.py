# Generated by Django 4.2.5 on 2023-11-13 23:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account_setup', '0008_managerinfo_appointment_manager_finish_approval_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointmentstatus',
            old_name='a_id',
            new_name='appointment',
        ),
    ]
