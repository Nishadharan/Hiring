# Generated by Django 5.0.1 on 2024-01-30 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userManagement', '0003_remove_user_date_joined_remove_user_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='last_login',
        ),
    ]
