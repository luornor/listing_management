from rest_framework import serializers
from .models import Shop, Listing

class ShopSerializer(serializers.ModelSerializer):
    listings = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Shop
        fields = ['id', 'name', 'shop_owner', 'listings']


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ['id', 'shop_id', 'title', 'description', 'price', 'quantity', 'created_at', 'updated_at',"image_url"]
