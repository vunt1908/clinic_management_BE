# Generated by Django 5.1.2 on 2024-12-16 00:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('doctor', '0001_initial'),
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_slot', models.CharField(choices=[('07:30-08:30', '07:30-08:30'), ('08:30-09:30', '08:30-09:30'), ('09:30-10:30', '09:30-10:30'), ('10:30-11:30', '10:30-11:30'), ('13:30-14:30', '13:30-14:30'), ('14:30-15:30', '14:30-15:30'), ('15:30-16:30', '15:30-16:30'), ('16:30-17:30', '16:30-17:30'), ('18:00-19:00', '18:00-19:00'), ('19:00-20:00', '19:00-20:00'), ('20:00-21:00', '20:00-21:00')], max_length=20, null=True)),
                ('date', models.DateField()),
                ('notes', models.TextField(blank=True)),
                ('reason', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.patient')),
            ],
            options={
                'unique_together': {('doctor', 'date', 'time_slot')},
            },
        ),
    ]
