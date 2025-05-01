from rest_framework import serializers
from .models import Restaurant, SliderItem, MenuCategory, MenuItem
from goby.utils import get_translated_field


class RestaurantReadSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='restaurant-detail')
    total_orders = serializers.IntegerField(read_only=True)
    rating = serializers.FloatField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    categories = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Restaurant
        fields = ["id", "url", "name", "image", "cover", "description", "total_orders", "rating", "categories"]

    def get_name(self, obj: Restaurant):
        return get_translated_field(self.context["request"], obj.name_ar, obj.name_en)

    def get_description(self, obj: Restaurant):
        return get_translated_field(self.context["request"], obj.description_ar, obj.description_en)

    def get_categories(self, obj: Restaurant):
        categories = MenuCategoryReadSerializer(obj.categories, many=True, context=self.context).data
        return [{"id": category["id"], "name": category["name"]} for category in categories]


class RestaurantWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class SliderItemReadSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='slider-detail')
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = SliderItem
        fields = ['id', "url", 'title', 'description', 'image', 'link', 'url']

    def get_title(self, obj: SliderItem):
        return get_translated_field(self.context["request"], obj.title_ar, obj.title_en)

    def get_description(self, obj: SliderItem):
        return get_translated_field(self.context["request"], obj.description_ar, obj.description_en)


class SliderItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SliderItem
        fields = '__all__'


class MenuCategoryReadSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = MenuCategory
        fields = ["id", "name", "image"]

    def get_name(self, obj: MenuCategory):
        return get_translated_field(self.context["request"], obj.name_ar, obj.name_en)


class MenuCategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = '__all__'


class MenuItemReadSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='menu-item-detail')
    category = serializers.SerializerMethodField()
    restaurant = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = ["id", "url", "name", "description", "category", "restaurant", "image", "price"]

    def get_name(self, obj: MenuItem):
        return get_translated_field(self.context["request"], obj.name_ar, obj.name_en)

    def get_description(self, obj: MenuItem):
        return get_translated_field(self.context["request"], obj.description_ar, obj.description_en)

    def get_category(self, obj: MenuItem) -> dict:
        category = MenuCategoryReadSerializer(obj.category, context=self.context).data
        return {"id": category["id"], "name": category["name"]}

    def get_restaurant(self, obj: MenuItem):
        restaurant = RestaurantReadSerializer(obj.restaurant, context=self.context).data
        return {"id": restaurant["id"], "name": restaurant["name"]}


class MenuItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'
