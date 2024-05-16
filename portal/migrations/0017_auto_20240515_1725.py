# Generated by Django 3.2 on 2024-05-15 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0016_remove_contractoruser_corenexpired'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract_application',
            name='compdate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='comprojcert',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='ct_is_completed',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='ct_is_completed_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='inspbynemsa',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='letterofdonation',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='nemsatestcert',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='projsignedoff',
            field=models.BooleanField(default=False),
        ),
    ]
