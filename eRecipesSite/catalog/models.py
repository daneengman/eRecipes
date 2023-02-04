from django.db import models

# Create your models here.
class Cuisine(models.Model):
    """Model representing a recipe cuisine."""
    name = models.CharField(max_length=200, help_text='Enter a recipe cuisine (e.g. Italian, Japanese)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

# Create your models here.
class Diet(models.Model):
    """Model representing a diet that a recipe may fall under."""
    name = models.CharField(max_length=200, help_text='Enter a diet (e.g. Vegan, Gluten-free)')

    # probably should include diets this includes as a super-set

    def __str__(self):
        """String for representing the Model object."""
        return self.name


from django.urls import reverse # Used to generate URLs by reversing the URL patterns

import uuid # Required for unique book instances
class Recipe(models.Model):
    """Model representing a recipe."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular recipe across whole library')

    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author is a string rather than an object because it hasn't been declared yet in the file
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    # need to figure out ingredients and stuff...
    # later fields: ingredients (quantities? uniqueness?) last made, rating, personal notes, pictures??? 
    # uploaded, whatever else

    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the recipe')
    # isbn = models.CharField('ISBN', max_length=13, unique=True,
    #                          help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    cuisine = models.ManyToManyField(Cuisine, help_text='Select a cuisine for this recipe')
    diet = models.ManyToManyField(Diet, help_text='Select a diet for this recipe')

    class Meta:
        ordering = ['title']

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this recipe."""
        return reverse('recipe-detail', args=[str(self.id)])

# probably could have some other things in here
class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'
