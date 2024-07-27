from django.db import models

class Shop(models.Model):
    shop_owner = models.CharField(max_length=100,unique=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100,default='not specified')
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f"shop - {self.id}"

class Listing(models.Model):
    class Category(models.TextChoices):
        ELECTRONICS = 'electronics'
        FASHION = 'fashion'
        HOME = 'home'
        BEAUTY = 'beauty'
        BOOKS = 'books'
        TOYS = 'toys'
        OTHER = 'other'
    shop_id = models.ForeignKey(Shop, related_name='listings', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=50, choices=Category.choices, default=Category.OTHER)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_url = models.CharField(max_length=255,blank=True,null=True)
    quantity = models.PositiveIntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title if self.title else f"Listing {self.id}"
