# Generated by Django 3.2.9 on 2021-11-06 22:07

from django.db import migrations, models
import swings.models


class Migration(migrations.Migration):

    dependencies = [
        ('swings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='swing',
            name='recording',
            field=models.FileField(blank=True, default='', upload_to=swings.models.user_directory_path),
        ),
    ]