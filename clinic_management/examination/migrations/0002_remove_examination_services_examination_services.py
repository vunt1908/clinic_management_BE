# Generated by Django 5.1.2 on 2024-12-20 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examination', '0001_initial'),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examination',
            name='services',
        ),
        migrations.AddField(
            model_name='examination',
            name='services',
            field=models.ManyToManyField(related_name='examinations', to='services.services'),
        ),
    ]
