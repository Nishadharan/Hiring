# Generated by Django 5.0.1 on 2024-02-07 07:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('technicalLevel', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='technicalinterviewtable',
            old_name='status',
            new_name='shortlistStatus',
        ),
        migrations.AddField(
            model_name='technicalinterviewtable',
            name='submissionStatus',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='skillstable',
            name='techReview',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='technicalLevel.technicalinterviewtable'),
        ),
    ]