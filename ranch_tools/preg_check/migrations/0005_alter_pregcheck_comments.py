# Generated by Django 4.2.3 on 2023-07-11 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preg_check', '0004_alter_cow_animal_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pregcheck',
            name='comments',
            field=models.TextField(blank=True),
        ),
    ]
