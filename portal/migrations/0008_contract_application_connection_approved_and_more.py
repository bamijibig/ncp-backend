# Generated by Django 4.1.2 on 2022-12-21 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0007_remove_contract_application_te2_cabletypsiz_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract_application',
            name='connection_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='connection_status',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='ct_is_pre_requested',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='ct_is_pre_requested_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='cto_approved_by',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='cto_is_connection_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='cto_is_connection_approved_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='declined',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='declined_comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='hm_approved_by',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='hm_is_connection_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='hm_is_contractor_approved_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='in_approval_workflow',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='npd_is_connection_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='npd_is_connection_approved_by',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='npd_is_connection_approved_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='te_is_connection_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='te_is_connection_approved_by',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='te_is_connection_approved_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='tept_is_connection_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='tept_is_connection_approved_by',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='tept_is_connection_approved_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='tm_is_connection_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='tm_is_connection_approved_by',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='contract_application',
            name='tm_is_connection_approved_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contractoruser',
            name='is_hm',
            field=models.BooleanField(default=False),
        ),
    ]
