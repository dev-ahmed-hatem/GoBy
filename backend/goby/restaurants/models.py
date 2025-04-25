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
