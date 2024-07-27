from django.contrib import admin
from . models import Listing, Shop

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ('shop_id','title', 'category', 'price', 'quantity') 

class ShopAdmin(admin.ModelAdmin):
    list_display = ("id",'name', 'shop_owner','location', 'created')

admin.site.register(Listing,ListingAdmin)
admin.site.register(Shop,ShopAdmin)
