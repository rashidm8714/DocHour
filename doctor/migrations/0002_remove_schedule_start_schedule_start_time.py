# Generated by Django 4.1.4 on 2022-12-22 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("doctor", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="schedule",
            name="start",
        ),
        migrations.AddField(
            model_name="schedule",
            name="start_time",
            field=models.TimeField(auto_now=True),
        ),
    ]
