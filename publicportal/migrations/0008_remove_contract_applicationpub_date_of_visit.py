# Generated by Django 3.2 on 2024-05-14 20:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publicportal', '0007_auto_20240514_2107'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract_applicationpub',
            name='date_of_visit',
        ),
    ]
