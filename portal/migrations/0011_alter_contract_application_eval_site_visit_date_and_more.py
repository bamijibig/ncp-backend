# Generated by Django 4.1.2 on 2022-12-26 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0010_delete_technicalevaluation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract_application',
            name='eval_site_visit_date',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='contract_application',
            name='precom_last_inspection_date',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]