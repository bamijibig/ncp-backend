# Generated by Django 4.1.2 on 2022-11-14 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portal", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="contractoruser",
            name="is_admin",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="contractoruser",
            name="is_contractor",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="contractoruser",
            name="is_cto",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="contractoruser",
            name="is_hsch",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="contractoruser",
            name="is_md",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="contractoruser",
            name="is_npd",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="contractoruser",
            name="is_te",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="contractoruser",
            name="is_tm",
            field=models.BooleanField(default=False),
        ),
    ]