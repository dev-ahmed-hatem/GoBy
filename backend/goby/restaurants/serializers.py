from rest_framework import serializers
from .models import Restaurant, SliderItem, MenuCategory, MenuItem, Order, OrderItem
from goby.utils import get_translated_field
from clients.models import Client


class RestaurantReadSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='restaurant-detail')
    total_orders = serializers.IntegerField(read_only=True)
    rating = serializers.FloatField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    categories = serializers.SerializerMethodField(read_only=True)
    merchant_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Restaurant
        fields = ["id", "url", "name", "image", "cover", "description", "total_orders", "rating", "categories",
                  "merchant_type"]

    def get_name(self, obj: Restaurant):
        return get_translated_field(self.context["request"], obj.name_ar, obj.name_en)

    def get_description(self, obj: Restaurant):
        return get_translated_field(self.context["request"], obj.description_ar, obj.description_en)

    def get_categories(self, obj: Restaurant):
        categories = MenuCategoryReadSerializer(obj.categories, many=True, context=self.context).data
        return [{"id": category["id"], "name": category["name"]} for category in categories]

    def get_merchant_type(self, obj: Restaurant):
        types = {"grocery": "بقالة", "hand-made": "انتاج منزلي", "restaurant": "مطعم"}
        if self.context["request"].lang == "en":
            return obj.merchant_type
        return types[obj.merchant_type]


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


class MenuItemBaseSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    def get_name(self, obj):
        return get_translated_field(self.context.get("request"), obj.name_ar, obj.name_en)

    def get_description(self, obj):
        return get_translated_field(self.context.get("request"), obj.description_ar, obj.description_en)

    def get_category(self, obj: MenuItem) -> dict:
        category = MenuCategoryReadSerializer(obj.category, context=self.context).data
        return {"id": category["id"], "name": category["name"]}


class MenuItemReadSerializer(MenuItemBaseSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='menu-item-detail')
    restaurant = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = ["id", "url", "name", "description", "category", "restaurant", "image", "price"]

    def get_restaurant(self, obj: MenuItem):
        restaurant = RestaurantReadSerializer(obj.restaurant, context=self.context).data
        return {"id": restaurant["id"], "name": restaurant["name"]}


class MenuItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class MenuItemInlineSerializer(MenuItemBaseSerializer):
    class Meta:
        model = MenuItem
        fields = ["id", "name", "description", "image", "price"]


class OrderReadSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='order-detail')
    client_name = serializers.SerializerMethodField()
    restaurant_name = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'url', 'client_name', 'restaurant_name', 'total_amount', 'total_price', 'status', 'created_at',
                  'address']

    def get_client_name(self, obj: Order):
        return obj.client.name

    def get_restaurant(self, obj: Order):
        return get_translated_field(self.context["request"], obj.restaurant.name_ar, obj.restaurant.name_en)

    def get_total_mount(self, obj: Order):
        return obj.total_amount()

    def get_total_price(self, obj: Order):
        return obj.total_price()


class OrderItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderWriteSerializer(serializers.ModelSerializer):
    items = OrderItemWriteSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def validate_items(self, obj):
        if len(obj) == 0:
            raise serializers.ValidationError({"items": "order cannot be empty."})

    def create(self, validated_data):
        client_id = validated_data.get("client")
        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            raise serializers.ValidationError({"client": "client does not exist."})

        address = validated_data.pop("address")
        if not address or address.strip() == "":
            address = client.address

        if not address or address.strip() == "":
            raise serializers.ValidationError({"address": "no address provided and client has no address."})

        items = self.initial_data.get("items", [])
        if not items:
            raise Exception()
