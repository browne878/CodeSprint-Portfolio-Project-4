# Generated by Django 3.2 on 2022-11-05 23:20

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('planner', '0013_auto_20220624_2016'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User_Profile',
            new_name='UserProfile',
        ),
    ]