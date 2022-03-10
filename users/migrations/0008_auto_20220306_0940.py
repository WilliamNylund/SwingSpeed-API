# Generated by Django 3.2.9 on 2022-03-06 09:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20220127_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(150)]),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.IntegerField(blank=True, choices=[(0, 'Male'), (1, 'Female'), (2, 'Other')], null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='handicap',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(36)]),
        ),
        migrations.AlterField(
            model_name='user',
            name='height',
            field=models.FloatField(blank=True, null=True),
        ),
    ]