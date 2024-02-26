# Generated by Django 5.0 on 2024-02-07 05:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_rename_job_id_job_post_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('company', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('applied_at', models.DateTimeField(auto_now_add=True)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.applicant')),
                ('job_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.job_post')),
            ],
        ),
    ]