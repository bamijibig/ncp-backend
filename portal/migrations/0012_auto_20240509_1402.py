# Generated by Django 3.2 on 2024-05-09 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0011_auto_20240508_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractoruser',
            name='corenexpired',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contractoruser',
            name='corenissued',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]