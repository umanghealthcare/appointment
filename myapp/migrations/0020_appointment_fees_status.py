# Generated by Django 4.0.4 on 2022-07-10 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0019_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='fees_status',
            field=models.CharField(default='pending', max_length=100),
        ),
    ]
