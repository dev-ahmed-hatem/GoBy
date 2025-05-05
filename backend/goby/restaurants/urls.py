from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, SliderItemViewSet, MenuCategoryViewSet, MenuItemViewSet, OrderViewSet
from django.urls import path, include

router = DefaultRouter()
router.register('restaurants', RestaurantViewSet, basename='restaurant')
router.register('sliders', SliderItemViewSet, basename='slider')
router.register('menu-categories', MenuCategoryViewSet, basename='menu-category')
router.register('menu-items', MenuItemViewSet, basename='menu-item')
router.register('orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
