# Generated by Django 5.0.1 on 2024-01-30 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userManagement', '0004_remove_user_last_login'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='empId',
            field=models.CharField(default='M1372', max_length=10, unique=True),
        ),
    ]
