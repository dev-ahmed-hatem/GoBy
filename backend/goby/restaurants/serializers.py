from rest_framework import serializers
from .models import Restaurant, Category, SliderItem


class RestaurantSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='restaurant-detail')
    total_orders = serializers.IntegerField(read_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='category-detail')

    class Meta:
        model = Category
        fields = '__all__'


class SliderItemSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='slider-detail')

    class Meta:
        model = SliderItem
        fields = ['id', 'title', 'description', 'image', 'link', 'url']
