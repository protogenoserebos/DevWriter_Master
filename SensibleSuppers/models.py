from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
   



class RecipeArticle(models.Model):
    """
    Represents a recipe published on the Sensible Suppers site.
    """

    # --- Choice Constants ---
    MEAL_TYPE = [
        ('Breakfast', 'Breakfast'),
        ('Sides', 'Sides, Dips, and Appetizers'),
        ('Entree', 'Entree'),
        ('Dessert', 'Dessert'),
    ]

    # --- Core Info ---
    title = models.CharField(max_length=200, help_text="Recipe Title")
    slug = models.SlugField(unique=True, help_text="URL-friendly version of the title")
    author = models.CharField(max_length=200, help_text="Your First and Last Names")
    # Fixed default to match a valid choice key ('Entree') rather than 'blue'
    mealtype = models.CharField(max_length=20, choices=MEAL_TYPE, default='Entree') 
    
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    
    # --- Ingredients & Instructions ---
    recipe_ingredients = models.TextField(blank=True,null=True, help_text="Enter key ingredients on separate lines")
    # Added this field as requested in your description
    recipe_instructions = models.TextField(blank=True, null=True, help_text="Step-by-step cooking instructions")

    recipe_short_card_description = models.TextField(blank=True, null=True, help_text="Short description for cards")
    # --- Alternating Content Fields ---
    description_blurb_1 = models.TextField(blank=True, help_text="1st Description")
    recipe_image_1 = models.ImageField(upload_to='recipe_photos/', blank=True)
    
    description_blurb_2 = models.TextField(blank=True, help_text="2nd Description")
    recipe_image_2 = models.ImageField(upload_to='recipe_photos/', blank=True)
    
    description_blurb_3 = models.TextField(blank=True, help_text="3rd Description")
    recipe_image_3 = models.ImageField(upload_to='recipe_photos/', blank=True)
    
    description_blurb_4 = models.TextField(blank=True, help_text="4th Description")
    recipe_image_4 = models.ImageField(upload_to='recipe_photos/', blank=True)
    
    description_blurb_5 = models.TextField(blank=True, help_text="5th Description")
    recipe_image_5 = models.ImageField(upload_to='recipe_photos/', blank=True)

    # --- Video Media ---
    recipe_video = models.URLField(blank=True, null=True, help_text="Optional YouTube Video")

    class Meta:
        ordering = ['-date_added']
        verbose_name = "Recipe Article"

    def __str__(self):
        return f"{self.title} - {self.mealtype}"

    def get_absolute_url(self):
        # This tells Django how to calculate the URL for an instance
        return reverse('recipe_detail', kwargs={'slug': self.slug})
    
    def get_mealtype_color(self):
        """Returns a specific brand color based on the meal type."""
        colors = {
            'Entree': '#BC6C25',    # Terracotta/Peach
            'Breakfast': '#D4A373', # Gold/Mustard
            'Dessert': '#2A9D8F',   # Teal/Aqua
            'Sides': '#264653',     # Deep Dark Blue
        }
        return colors.get(self.mealtype, '#FF7F50') # Default to orange if not found

    def get_content_blocks(self):
        """
        Helper method to group descriptions and images for the template loop.
        Returns a list of tuples: [(desc1, img1), (desc2, img2), ...]
        """
        blocks = [
            (self.description_blurb_1, self.recipe_image_1),
            (self.description_blurb_2, self.recipe_image_2),
            (self.description_blurb_3, self.recipe_image_3),
            (self.description_blurb_4, self.recipe_image_4),
            (self.description_blurb_5, self.recipe_image_5),
        ]
        # Filter out empty blocks so blank fields don't take up space
        return [b for b in blocks if b[0] or b[1]]
    
    def get_mealtype_url(self):
        """Returns the URL for the specific meal type category."""
        mapping = {
            'Breakfast': 'breakfast',
            'Sides': 'snacks-dips',
            'Entree': 'entrees',
            'Dessert': 'desserts',
        }
        # Look up the URL name using the mealtype key
        url_name = mapping.get(self.mealtype)
        return reverse(url_name) if url_name else "#"
        # Recipe Comment Chain Models

class Comment(models.Model):
    post = models.ForeignKey(RecipeArticle, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    rating = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True
    )
    
    def __str__(self):
        return f"{self.post.title} - {self.parent} - {self.name} - {self.body}"
    
