# Generated by Django 4.1.4 on 2022-12-29 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("client", "0005_uploads_caption_alter_uploads_filename"),
    ]

    operations = [
        migrations.AlterField(
            model_name="uploads",
            name="link",
            field=models.FileField(upload_to="media/uploads/"),
        ),
    ]
