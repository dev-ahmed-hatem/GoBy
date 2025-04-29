from django.db.models import Q

from rest_framework.viewsets import ModelViewSet
from .models import Restaurant, Category, SliderItem, MenuItem, MenuCategory
from .serializers import (RestaurantSerializer, CategorySerializer, SliderItemSerializer,
                          MenuItemWriteSerializer, MenuItemReadSerializer, MenuCategoryWriteSerializer,
                          MenuCategoryReadSerializer)


class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        name = self.request.query_params.get('name')
        if name is not None:
            return self.queryset.filter(Q(name__icontains=name) | Q(description__icontains=name))

        return self.queryset


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SliderItemViewSet(ModelViewSet):
    queryset = SliderItem.objects.filter(is_active=True).order_by("order")
    serializer_class = SliderItemSerializer


class MenuCategoryViewSet(ModelViewSet):
    queryset = MenuCategory.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return MenuCategoryWriteSerializer
        return MenuCategoryReadSerializer

    def get_queryset(self):
        restaurant = self.request.query_params.get('restaurant')
        if restaurant:
            return self.queryset.filter(restaurant__id=restaurant)

        return self.queryset


class MenuItemViewSet(ModelViewSet):
    queryset = MenuItem.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return MenuItemWriteSerializer
        return MenuItemReadSerializer

    def get_queryset(self):
        category = self.request.query_params.get('category')
        if category:
            return self.queryset.filter(category__id=category)

        return self.queryset
