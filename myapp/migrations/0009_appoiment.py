# Generated by Django 4.0.4 on 2022-07-06 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_remove_doctor_profile_doctor_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appoiment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=100)),
                ('discrpiton', models.TextField(max_length=100)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.doctor_profile')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
            ],
        ),
    ]
