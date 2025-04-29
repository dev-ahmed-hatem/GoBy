from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/categories/')

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/restaurants/images', null=True)
    cover = models.ImageField(upload_to='images/restaurants/covers', null=True)
    description = models.TextField()
    total_orders = models.IntegerField(default=0)
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.name


# models.py
class SliderItem(models.Model):
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/sliders/')
    link = models.URLField(blank=True, null=True, help_text="Optional link or deep link")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title or f"Slider #{self.pk}"


class MenuCategory(models.Model):
    name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_categories')

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"


class MenuItem(models.Model):
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images/menu_items/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.price} EGP"
