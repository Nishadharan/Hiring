# Generated by Django 5.0.1 on 2024-02-14 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('technicalLevel', '0002_rename_status_technicalinterviewtable_shortliststatus_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='technicalinterviewtable',
            name='resumeId',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]