# Generated by Django 4.1.4 on 2023-11-01 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloneT', '0004_profile_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='profile_image',
        ),
    ]
