# Generated by Django 4.2 on 2024-11-21 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='job_title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
