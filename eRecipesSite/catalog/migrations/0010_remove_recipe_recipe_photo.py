# Generated by Django 4.1.4 on 2023-02-04 06:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_recipe_recipe_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='recipe_photo',
        ),
    ]
