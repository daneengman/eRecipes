# Generated by Django 4.1.4 on 2023-02-04 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_remove_recipe_recipe_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='recipe_photo',
            field=models.ImageField(null=True, upload_to='recipes'),
        ),
    ]
