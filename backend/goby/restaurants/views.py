from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework.viewsets import ModelViewSet
from .models import Restaurant, Category, SliderItem, MenuItem, MenuCategory
from .serializers import (RestaurantSerializer, CategorySerializer, SliderItemSerializer,
                          MenuItemWriteSerializer, MenuItemReadSerializer, MenuCategoryWriteSerializer,
                          MenuCategoryReadSerializer)


class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(name='name', type=str, description='Filter by name or description'),
            OpenApiParameter(name='recently', type=bool, description='Sort by newest'),
            OpenApiParameter(name='best_sellers', type=bool, description='Sort by most ordered'),
        ]
    )
    def get_queryset(self):
        queryset = self.queryset
        name = self.request.query_params.get('name')
        recently = self.request.query_params.get('recently')
        best_sellers = self.request.query_params.get('best_sellers')

        if recently and recently.lower() == 'true':
            queryset = queryset.order_by('-id')

        if best_sellers and best_sellers.lower() == 'true':
            queryset = queryset.order_by('-total_orders')

        if name:
            queryset = queryset.filter(Q(name__icontains=name) | Q(description__icontains=name))

        return queryset


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SliderItemViewSet(ModelViewSet):
    queryset = SliderItem.objects.filter(is_active=True).order_by("order")
    serializer_class = SliderItemSerializer
    pagination_class = None


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
