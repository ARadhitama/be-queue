# Generated by Django 4.1.7 on 2023-12-13 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("oauth", "0005_delete_district"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="email",
            field=models.CharField(max_length=50, null=True),
        ),
    ]
