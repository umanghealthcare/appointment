# Generated by Django 4.0.4 on 2022-07-06 10:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_alter_appoiment_date_alter_appoiment_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appoiment',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
