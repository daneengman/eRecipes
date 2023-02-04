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
import pdf2image
import cv2

# extracts specified ingredient from recipe dict as a new singleton 
# dictionary
def process_word(ingredient):
    
    ingredient = ingredient.lower().strip()

    punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    word = ingredient
    for c in word.lower().strip():
        if c in punctuation:
            word = word.replace(c, "")
    return word

# create a new dictionary that extracts ingredients from the recipe_dict
def process_ingredients(ing_lst):
    d = {}

    for ingredient in ing_lst:
        processed = process_word(ingredient)
        d[processed] = d.get(processed, 0) + 1 # dict.update(process_word(ingredient, recipe_dict))
    return d

from pathlib import Path
from django.core.files import File
import pytesseract
def form_valid_helper(self, form):
    # isvalid = super(RecipeCreate, self).form_valid(form)
    # s = Subcategory.objects.get(pk=self.kwargs['subcat_id'].encode('utf-8'))
    # this_object = self.get_object()
    # print("hello world")
    # print(self.request.POST.keys())
    # self.object.save()
    # print(self.request.FILES)

    if self.request.FILES.get('recipe_pdf'):
        # print("Now attempting to process a pdf, hahaha")
        pdf_path = str(self.object.recipe_pdf)
        # print()
        pdf = pdf2image.convert_from_path(pdf_path)

        png_path_tail = os.path.splitext(os.path.split(pdf_path)[1])[0]+".png"
        png_path_head = os.path.split(os.path.split(pdf_path)[0])[0] # i'm sure there is a better way to do this
        
        images = []
        for i in range(len(pdf)):
            png_path = f'{png_path_head}/images/{i+1}-{png_path_tail}'
            # print("png path", png_path)
            pdf[i].save(png_path, 'PNG')
            if i == 0:
                # self.object.recipe_picture = f'{png_path}'
                # self.object.save()
                path = Path(png_path)
                with path.open(mode='rb') as f:
                    self.object.recipe_photo = File(f)
                    self.object.save()# update_fields=['recipe_photo'])
                    # print("saved")
            images.append(cv2.imread(png_path))
            

            words = []
            for img in images:
                text = pytesseract.image_to_string(img)
                words += text.split()
            ingredient_dictionary = process_ingredients(words)

            self.object.words = ingredient_dictionary
            self.object.save()
            # print(process_ingredients(words))
        # print(pdf_path)
        

        # need path to jpg land

        # pdf[0].save(f'{self.object.recipe_title}_cbbr_page{1}.png', 'PNG')
        # self.object.recipe_picture = 


    # if self.request.FILES.get('recipe_photo'):
    #     print("hello world 2")
    #     image = form.cleaned_data['recipe_photo']
    #     # print("hello world 2")
    #     print("keys")
    #     for key in form.cleaned_data:
    #         print(key, form.cleaned_data[key])
    #     # title = form.cleaned_data['art_title'].encode('utf-8')
    #     # year_of_creation = form.cleaned_data['year_of_creation']
    #     m = Recipe.objects.get_or_create(recipe_photo=image)[0]
        # Recipe.objects.recipe_photo.add(m) # idk
        # self.object.save()

import os
# from django import Media
# this needs to be replaced with something more boutique
class RecipeCreate(CreateView):
    model = Recipe
    fields = ['title', 'author', 'description', 'cuisine', 'diet', 'last_made', 'recipe_photo', 'recipe_pdf']

    def form_valid(self, form):
        isvalid = super(RecipeCreate, self).form_valid(form)
        form_valid_helper(self, form)
        return isvalid

    # def post(self, request, *args, **kwargs):
    #     # self.object = self.get_object() // what does this do
    #     self.process_files()
    #     return super().post(request, *args, **kwargs)
    # # initial = {'date_of_death': '11/06/2020'}

class RecipeUpdate(UpdateView):
    model = Recipe
    fields = ['title', 'author', 'description', 'cuisine', 'diet', 'last_made', 'recipe_photo', 'recipe_pdf'] # Not recommended (potential security issue if more fields added)

    def form_valid(self, form):
        isvalid = super(RecipeUpdate, self).form_valid(form)
        form_valid_helper(self, form)
        return isvalid

class RecipeDelete(DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipes')



#models.py
from .models import *
#views

def RecipeSearch(request):
    """ search function  """
    if request.method == "POST":
        query_name = request.POST.get('ingredients', None)
        if query_name:
            words_results = Recipe.objects.filter(words__contains=query_name) # need to adjust this to properly filter
            title_results = Recipe.objects.filter(title__contains=query_name)
            context={"title_results":title_results, "words_results":words_results, "query_name":query_name}
            return render(request, 'recipe-search.html', context=context)
    print('didn"t find anything')
    return render(request, 'recipe-search.html')
    # return render(request, 'index.html', context=context)

# User.objects.filter(data__campaigns__contains=[{'key': 'value'}])
"""
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
    """
