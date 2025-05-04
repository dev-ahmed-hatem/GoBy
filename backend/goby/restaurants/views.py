from django.db.models import Q
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter

import rest_framework.custom_pagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .models import Restaurant, SliderItem, MenuItem, MenuCategory
from .serializers import (RestaurantReadSerializer, RestaurantWriteSerializer, SliderItemReadSerializer,
                          SliderItemWriteSerializer, MenuItemInlineSerializer,
                          MenuItemWriteSerializer, MenuItemReadSerializer, MenuCategoryWriteSerializer,
                          MenuCategoryReadSerializer)


@extend_schema_view(
    list=extend_schema(
        summary="List all restaurants",
        description="Retrieve a list of restaurants with optional filters.",
        parameters=[
            OpenApiParameter(name='name', type=str, description='Filter by name or description'),
            OpenApiParameter(name='recently', type=bool, description='Sort by newest first'),
            OpenApiParameter(name='best_sellers', type=bool, description='Sort by highest total_orders'),
        ],
        responses={200: RestaurantReadSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Retrieve a specific restaurant",
        responses={200: RestaurantReadSerializer}
    ),
    create=extend_schema(
        summary="Create a new restaurant",
        request=RestaurantWriteSerializer,
        responses={201: RestaurantReadSerializer}
    ),
    update=extend_schema(
        summary="Update an existing restaurant",
        request=RestaurantWriteSerializer,
        responses={200: RestaurantReadSerializer}
    ),
    partial_update=extend_schema(
        summary="Partially update a restaurant",
        request=RestaurantWriteSerializer,
        responses={200: RestaurantReadSerializer}
    ),
    destroy=extend_schema(
        summary="Delete a restaurant",
        responses={204: None}
    )
)
class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RestaurantWriteSerializer
        return RestaurantReadSerializer

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

    @action(methods=['GET'], detail=True)
    def detailed(self, request, pk=None):
        restaurant = self.get_object()
        serialized = self.get_serializer(restaurant)
        menu_items = MenuItem.objects.filter(restaurant=restaurant)
        serialized_menu_items = MenuItemInlineSerializer(menu_items, many=True, context={"request": request}).data

        response = {**serialized.data,
                    "menu-items": serialized_menu_items}
        return Response(response, )


class SliderItemViewSet(ModelViewSet):
    queryset = SliderItem.objects.order_by("order")
    pagination_class = rest_framework.custom_pagination.NoPagination

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return SliderItemWriteSerializer
        return SliderItemReadSerializer

    def get_queryset(self):
        queryset = self.queryset
        active = self.request.query_params.get('active')

        if active is not None and active.lower() == 'true':
            queryset = queryset.filter(is_active=True)

        return queryset


class MenuCategoryViewSet(ModelViewSet):
    queryset = MenuCategory.objects.all()
    pagination_class = rest_framework.custom_pagination.NoPagination

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return MenuCategoryWriteSerializer
        return MenuCategoryReadSerializer


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
