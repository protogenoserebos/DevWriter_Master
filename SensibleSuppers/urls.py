from django.urls import path
from . import views
from .views import RecipeDetailView, RecipeListView

urlpatterns = [

      # Homepage
 
    path('', views.RecipeListView.as_view(), name='home'),
    # ... your other paths like recipe_detail ...

    # The <slug:slug> part captures the url-friendly title (e.g., 'avocado-toast')
    path('recipe/<slug:slug>/', RecipeDetailView.as_view(), name='recipe_detail'),

    path('entrees/', views.entrees, name='entrees'),

    path('dips/', views.dips, name='dips'),
    
    path('breakfast/', views.breakfast, name='breakfast'),

    path('desserts/', views.desserts, name='desserts'),

    path('snacks-dips/', views.snacksdips, name='snacks-dips'),

  
]

