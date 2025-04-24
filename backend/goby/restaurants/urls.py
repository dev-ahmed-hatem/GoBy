from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, CategoryViewSet, SliderItemViewSet
from django.urls import path, include

router = DefaultRouter()
router.register('restaurants', RestaurantViewSet, basename='restaurant')
router.register('categories', CategoryViewSet, basename='category')
router.register('sliders', SliderItemViewSet, basename='slider')

urlpatterns = [
    path('', include(router.urls)),
]
