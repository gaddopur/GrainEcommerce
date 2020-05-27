from django.db import models
from products.models import Product, ProductVariation
# Create your models here.

class CartItem(models.Model):
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    variation = models.ManyToManyField(ProductVariation)
    notes = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.title

class Cart(models.Model):
    # items = models.ManyToManyField(CartItem)
    # products = models.ManyToManyField(Product)
    total = models.DecimalField(decimal_places=2, max_digits=100, default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        # return "%s" %(self.id)
        return "Cart id: %s" %(self.id)
