# Generated by Django 5.0 on 2024-02-25 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_remove_company_location_remove_company_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job_post',
            name='company_id',
        ),
    ]