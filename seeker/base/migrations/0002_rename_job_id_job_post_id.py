# Generated by Django 5.0 on 2024-02-02 20:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job_post',
            old_name='job_id',
            new_name='id',
        ),
    ]
