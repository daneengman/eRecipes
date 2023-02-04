from django.shortcuts import render

# Create your views here.
from .models import Recipe, Author, Cuisine, Diet

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_recipes = Recipe.objects.all().count()

    # Available books (status = 'a')
    # num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    num_diets = Diet.objects.count()

    num_cuisines = Cuisine.objects.count()

    context = {
        'num_recipes': num_recipes,
        # 'num_instances': num_instances,
        # 'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_cuisines': num_cuisines,
        'num_diets': num_diets,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

from django.views import generic

class RecipeListView(generic.ListView):
    model = Recipe
    paginate_by = 10

class RecipeDetailView(generic.DetailView):
    model = Recipe

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author