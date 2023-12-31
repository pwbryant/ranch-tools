# Generated by Django 4.2.3 on 2023-10-10 02:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("preg_check", "0011_rename_pregnant_pregcheck_is_pregnant"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cow",
            name="animal_id",
            field=models.CharField(max_length=10),
        ),
        migrations.AlterUniqueTogether(
            name="cow",
            unique_together={("animal_id", "birth_year")},
        ),
    ]
