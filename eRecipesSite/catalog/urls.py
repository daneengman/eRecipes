from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipes/', views.RecipeListView.as_view(), name='recipes'),
    path('recipe/<int:pk>', views.RecipeDetailView.as_view(), name='recipe-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),

    # path('recipe/<int:pk>/update/', views.update_last_made, name='update-last-made'), # i'd sure like the recipe field to be better bring this back later?
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
# urlpatterns += [
#     path('static/media/recipes/<str:pk>', )
# ]

urlpatterns += [
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]

urlpatterns += [
    path('recipe/create/', views.RecipeCreate.as_view(), name='recipe-create'),
    path('recipe/<int:pk>/update/', views.RecipeUpdate.as_view(), name='recipe-update'),
    path('recipe/<int:pk>/delete/', views.RecipeDelete.as_view(), name='recipe-delete'),
]

urlpatterns += [
    path('search', views.RecipeSearch, name='search'),
]