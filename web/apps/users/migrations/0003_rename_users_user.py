# Generated by Django 5.1.5 on 2025-04-28 18:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_users_telegram_id_alter_users_username"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Users",
            new_name="User",
        ),
    ]
