# Generated by Django 2.2.9 on 2019-12-20 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0003_profile_indicators'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='indicators',
        ),
        migrations.DeleteModel(
            name='ProfileIndicator',
        ),
    ]