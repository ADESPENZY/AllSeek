# Generated by Django 4.2 on 2024-11-20 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0003_job_job_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Job Description'),
        ),
        migrations.AlterField(
            model_name='job',
            name='location',
            field=models.CharField(max_length=200, verbose_name='Location'),
        ),
    ]
