# Generated by Django 5.0 on 2024-02-17 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_userprofile_location'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='location',
            new_name='locations',
        ),
    ]