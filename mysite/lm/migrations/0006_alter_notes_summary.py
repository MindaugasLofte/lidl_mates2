# Generated by Django 4.1.3 on 2022-12-06 12:29

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('lm', '0005_alter_myuser_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='summary',
            field=tinymce.models.HTMLField(default=0),
            preserve_default=False,
        ),
    ]
