# Generated by Django 5.0 on 2024-02-17 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_rename_location_userprofile_locations'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='locations',
            new_name='location',
        ),
    ]