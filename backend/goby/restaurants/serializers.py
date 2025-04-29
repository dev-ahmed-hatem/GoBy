from rest_framework import serializers
from .models import Restaurant, Category, SliderItem, MenuCategory, MenuItem


class RestaurantSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='restaurant-detail')
    total_orders = serializers.IntegerField(read_only=True)
    rating = serializers.FloatField(read_only=True)

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


class MenuCategoryReadSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='menu-category-detail')
    restaurant = serializers.SerializerMethodField()

    class Meta:
        model = MenuCategory
        fields = '__all__'

    def get_restaurant(self, obj: MenuCategory):
        return {"name": obj.restaurant.name, "id": obj.restaurant.id}


class MenuCategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = '__all__'


class MenuItemReadSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='menu-item-detail')
    category = serializers.SerializerMethodField()

    # category = MenuCategoryReadSerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = '__all__'

    def get_category(self, obj: MenuItem) -> dict:
        return {"id": obj.category.id, "name": obj.category.name,
                "restaurant": {"name": obj.category.restaurant.name}}


class MenuItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'
