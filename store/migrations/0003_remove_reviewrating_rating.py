# Generated by Django 4.0 on 2022-03-23 01:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_reviewrating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewrating',
            name='rating',
        ),
    ]
