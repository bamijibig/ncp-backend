# Generated by Django 4.1.2 on 2022-12-08 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0003_contractoruser_in_approval_workflow'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractoruser',
            name='registration_status',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
