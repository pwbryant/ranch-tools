# Generated by Django 4.2.3 on 2023-10-30 14:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("preg_check", "0015_alter_pregcheck_check_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="currentbreedingseason",
            name="breeding_season",
            field=models.PositiveIntegerField(),
        ),
    ]