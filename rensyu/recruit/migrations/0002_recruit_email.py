# Generated by Django 5.2 on 2025-05-25 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recruit", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="recruit",
            name="email",
            field=models.EmailField(default="no-email@example.com", max_length=100),
        ),
    ]
