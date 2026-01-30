from django.contrib import admin

from .models import RecipeArticle, Comment

# Register your models here.
admin.site.register(RecipeArticle)
admin.site.register(Comment)