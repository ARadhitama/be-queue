# Generated by Django 4.1.7 on 2023-12-13 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_alter_service_city_alter_service_province"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="servicecategory",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="servicecategory",
            name="updated_at",
        ),
    ]
