# Generated by Django 4.1.2 on 2023-02-24 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portal", "0020_contractoruser_staff_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="contractoruser",
            name="region",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
