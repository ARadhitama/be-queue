# Generated by Django 4.1.7 on 2023-12-12 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("oauth", "0004_remove_userprofile_email"),
    ]

    operations = [
        migrations.DeleteModel(
            name="District",
        ),
    ]
