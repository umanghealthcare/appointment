# Generated by Django 4.0.4 on 2022-06-29 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_remove_user_counter_remove_user_isverified'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='usertype',
            field=models.CharField(default='patient', max_length=100),
        ),
    ]