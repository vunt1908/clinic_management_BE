# Generated by Django 5.1.2 on 2024-12-23 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='job',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
