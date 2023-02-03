# Generated by Django 3.2.17 on 2023-02-02 20:56

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Ports",
            fields=[
                ("code", models.TextField(primary_key=True, serialize=False)),
                ("name", models.TextField()),
            ],
            options={
                "db_table": "ports",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Prices",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("day", models.DateField()),
                ("price", models.IntegerField()),
            ],
            options={
                "db_table": "prices",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Regions",
            fields=[
                ("slug", models.TextField(primary_key=True, serialize=False)),
                ("name", models.TextField()),
            ],
            options={
                "db_table": "regions",
                "managed": False,
            },
        ),
    ]
