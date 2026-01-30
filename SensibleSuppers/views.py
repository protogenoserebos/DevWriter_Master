from django.shortcuts import render, redirect
from .models import RecipeArticle, Comment
from django.views.generic import DetailView, ListView
from django.db.models import Avg


from django.shortcuts import render
from .models import RecipeArticle

# Home view (shows everything)
class RecipeListView(ListView):
    model = RecipeArticle
    template_name = 'SensibleSuppers/home.html'
    context_object_name = 'recipes'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Recent Recipes"
        return context

def category_view(request, meal_type_key):
    # This filters based on the key ('Breakfast', 'Entree', etc.)
    recipes = RecipeArticle.objects.filter(mealtype=meal_type_key)
    
    # This maps the key to a nice human-readable title
    titles = {
        'Breakfast': 'Breakfast Recipes',
        'Sides': 'Sides, Dips, and Appetizers',
        'Entree': 'Entree Recipes',
        'Dessert': 'Dessert Recipes',
    }
    
    context = {
        'recipes': recipes,
        'page_title': titles.get(meal_type_key, 'Recipes')
    }
    return render(request, 'SensibleSuppers/home.html', context)

# Category Views
def entrees(request):
    recipes = RecipeArticle.objects.filter(mealtype='Entree')
    return render(request, "SensibleSuppers/home.html", {
        'recipes': recipes, 
        'page_title': 'Entree Recipes'
    })

def breakfast(request):
    recipes = RecipeArticle.objects.filter(mealtype='Breakfast')
    return render(request, "SensibleSuppers/home.html", {
        'recipes': recipes, 
        'page_title': 'Breakfast Recipes'
    })

def desserts(request):
    recipes = RecipeArticle.objects.filter(mealtype='Dessert')
    return render(request, "SensibleSuppers/home.html", {
        'recipes': recipes, 
        'page_title': 'Dessert Recipes'
    })

def snacksdips(request):
    # Match the 'Sides' key from your model
    recipes = RecipeArticle.objects.filter(mealtype='Sides')
    return render(request, "SensibleSuppers/home.html", {
        'recipes': recipes, 
        'page_title': 'Sides, Dips, and Appetizers'
    })

class RecipeDetailView(DetailView):
    model = RecipeArticle
    template_name = 'recipe_detail.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter for Parent comments that HAVE a rating
        comments = self.object.comments.filter(parent__isnull=True).exclude(rating__isnull=True)
        
        total_count = comments.count()
        avg_rating = comments.aggregate(Avg('rating'))['rating__avg']
        
        context['average_rating'] = round(avg_rating, 1) if avg_rating else 0
        context['total_ratings'] = total_count

        breakdown = []
        for i in range(5, 0, -1):
            count = comments.filter(rating=i).count()
            # Ensure we don't divide by zero and provide a fallback
            percentage = int((count / total_count * 100)) if total_count > 0 else 0
            breakdown.append({
                'stars': i,
                'count': count,
                'percentage': percentage
            })
        
        context['rating_breakdown'] = breakdown
        return context
    
    def post(self, request, *args, **kwargs):
        # We need the recipe object to associate the comment with it
        recipe = self.get_object()
        
        name = request.POST.get('name')
        body = request.POST.get('body')
        rating = request.POST.get('rating')
        parent_id = request.POST.get('parent_id')

        # Logic to create the comment
        if parent_id:
            # It's a reply
            parent_comment = Comment.objects.get(id=parent_id)
            Comment.objects.create(
                post=recipe,
                name=name,
                body=body,
                parent=parent_comment,
                rating=None # Replies don't get ratings
            )
        else:
            # It's a top-level comment
            Comment.objects.create(
                post=recipe,
                name=name,
                body=body,
                rating=int(rating) if rating else 5
            )

        # Redirect back to the recipe page to clear the form and show the comment
        return redirect('recipe_detail', slug=recipe.slug)
