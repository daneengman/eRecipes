from django.contrib import admin

# Register your models here.
from .models import Author, Cuisine, Recipe, Diet # , BookInstance
admin.site.register(Cuisine)
admin.site.register(Author)
admin.site.register(Recipe)
admin.site.register(Diet)
# admin.site.register(BookInstance)

# possibly make this fancier later...
