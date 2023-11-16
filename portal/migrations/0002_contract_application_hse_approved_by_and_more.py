# Generated by Django 4.1.6 on 2023-11-16 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract_application',
            name='hse_approved_by',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='hse_is_connection_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='hse_is_contractor_approved_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='hse_memo',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='contractoruser',
            name='is_hse',
            field=models.BooleanField(default=False),
        ),
    ]
