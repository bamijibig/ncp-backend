# Generated by Django 4.1.2 on 2022-11-25 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0012_contract_application_profile_submitted_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractoruser',
            name='region',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
