# Generated by Django 4.1.2 on 2022-11-15 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "portal",
            "0002_contractoruser_is_admin_contractoruser_is_contractor_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Headquarter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("hq_name", models.CharField(blank=True, max_length=200, null=True)),
                ("location", models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Region",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("rh_name", models.CharField(blank=True, max_length=200, null=True)),
                ("location", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "hq",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="portal.headquarter",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BusinessHub",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bh_name", models.CharField(blank=True, max_length=200, null=True)),
                ("location", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "rh",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="portal.region",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="contract_application",
            name="bh",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="portal.businesshub",
            ),
        ),
        migrations.AddField(
            model_name="contractoruser",
            name="bh",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="portal.businesshub",
            ),
        ),
    ]
