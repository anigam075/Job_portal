# Generated by Django 5.1 on 2024-08-22 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0002_alter_company_job_posted_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='company_url',
            field=models.URLField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='company',
            name='job_url',
            field=models.URLField(max_length=1000),
        ),
    ]
