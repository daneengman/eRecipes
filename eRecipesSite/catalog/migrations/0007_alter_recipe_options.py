# Generated by Django 4.1.4 on 2023-02-04 04:53

from django.db import migrations
import django.db.models.functions.text


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_rename_last_used_recipe_last_made'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': [django.db.models.functions.text.Upper('title')]},
        ),
    ]
