# Generated by Django 3.0.5 on 2020-05-04 05:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200504_1029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='category',
        ),
    ]