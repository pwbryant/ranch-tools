# Generated by Django 4.2.3 on 2023-10-01 05:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("preg_check", "0006_remove_pregcheck_location_alter_pregcheck_cow_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cow",
            name="birth_year",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
