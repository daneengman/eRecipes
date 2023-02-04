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



import datetime

# from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import UpdateLastMadeForm

# @login_required
# @permission_required('catalog.can_mark_returned', raise_exception=True)
def update_last_made(request, pk):
    """View function for updating the last time a recipe was used."""
    print(request, pk)
    recipe = get_object_or_404(Recipe, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = UpdateLastMadeForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            recipe.last_made = form.cleaned_data['last_made']
            recipe.save()

            # redirect to a new URL:
            uri = request.build_absolute_uri()
            return HttpResponseRedirect(uri[:uri.strip('/').rfind('/')]) # this is kind of janky

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_last_made = datetime.date.today()
        form = UpdateLastMadeForm(initial={'last_made': proposed_last_made})

    context = {
        'form': form,
        'recipe': recipe,
    }

    return render(request, 'catalog/update_last_made.html', context)

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.models import Author

class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    # initial = {'date_of_death': '11/06/2020'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death', 'biography']
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


from catalog.models import Recipe

"""
https://stackoverflow.com/questions/62727762/django-call-custom-function-within-generic-views
class QuoteUpdate(UpdateView):
    model = Quote
    fields = ['quote_text']
    
    def my_custom_function(self):  
        # your code
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.my_custom_function()
        return super().post(request, *args, **kwargs)
        """


# this needs to be replaced with something more boutique
class RecipeCreate(CreateView):
    model = Recipe
    fields = ['title', 'author', 'description', 'cuisine', 'diet', 'last_made', 'recipe_photo']

    # initial = {'date_of_death': '11/06/2020'}

class RecipeUpdate(UpdateView):
    model = Recipe
    fields = ['title', 'author', 'description', 'cuisine', 'diet', 'last_made', 'recipe_photo'] # Not recommended (potential security issue if more fields added)

class RecipeDelete(DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipes')
