# Generated by Django 3.2.9 on 2021-11-06 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20211105_0111'),
    ]

    operations = [
        migrations.AddField(
            model_name='topics',
            name='description',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]
