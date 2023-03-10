# Generated by Django 4.1.6 on 2023-02-04 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0014_recipe_recipe_pdf_alter_recipe_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='recipe_pdf',
            field=models.FileField(blank=True, help_text='Or, if you prefer, upload a pdf here.', null=True, upload_to='catalog/static/media/recipes/pdfs'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='recipe_photo',
            field=models.ImageField(blank=True, help_text='Upload an image of the recipe here', null=True, upload_to='catalog/static/media/recipes/images'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='title',
            field=models.CharField(default='testing 0.9857889506512711', max_length=200),
        ),
    ]
