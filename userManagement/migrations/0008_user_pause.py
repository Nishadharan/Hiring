# Generated by Django 5.0.1 on 2024-02-02 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userManagement', '0007_rename_designation_userroles_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='pause',
            field=models.BooleanField(default=False),
        ),
    ]
