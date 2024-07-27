from rest_framework import serializers
from .models import Shop, Listing

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name', 'shop_owner']

class ListingSerializer(serializers.ModelSerializer):
    shop_details = ShopSerializer(source='shop_id', read_only=True)

    class Meta:
        model = Listing
        fields = ['id','shop_details', 'title', 'description', 'price','category', 'quantity', 'created_at', 'updated_at', 'image_url']