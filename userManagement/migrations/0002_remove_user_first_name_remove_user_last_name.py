# Generated by Django 5.0.1 on 2024-01-30 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userManagement', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
    ]