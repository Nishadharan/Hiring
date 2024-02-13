# Generated by Django 5.0.1 on 2024-01-31 08:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userManagement', '0005_alter_user_managers_alter_user_empid'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRoles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Designation', models.CharField(max_length=50)),
                ('Name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='roles',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='UserRoles', to='userManagement.userroles'),
            preserve_default=False,
        ),
    ]