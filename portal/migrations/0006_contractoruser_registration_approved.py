# Generated by Django 4.1.2 on 2022-12-10 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0005_contractoruser_declined_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractoruser',
            name='registration_approved',
            field=models.BooleanField(default=False),
        ),
    ]
