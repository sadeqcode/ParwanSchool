# Generated by Django 3.2.9 on 2021-11-06 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_topics_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topics',
            name='description',
        ),
        migrations.AddField(
            model_name='class',
            name='description',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='course',
            name='description',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]
