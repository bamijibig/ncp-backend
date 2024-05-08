# Generated by Django 3.2 on 2024-01-30 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0006_remove_contractoruser_job_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractoruser',
            name='job_title',
            field=models.CharField(blank=True, choices=[('Administrator', 'Administrator'), ('CTO', 'CTO'), ('Network Administrator', 'Network Administrator'), ('Regional Head', 'Regional Head'), ('Technical Manager', 'Technical Manager'), ('Technical Engineer', 'Technical Engineer'), ('BusinessHub Manager', 'BusinessHub Manager'), ('Health&Safety', 'Health&Safety'), ('Head Billing', 'Head Billing'), ('Head Metering', 'Head Metering')], default='Administrator', max_length=100, null=True),
        ),
    ]
