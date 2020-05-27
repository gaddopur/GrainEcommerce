from django.urls import reverse
from django.db import models

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=100, default=True)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('title', 'slug')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("products:product_detail", kwargs={"slug":  self.slug})

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete='CASCADE')
    image = models.ImageField(upload_to='products/images', default="products/images/default.png")
    featured = models.BooleanField(default=False)
    thumbnail = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.product.title

class ProductVariationManager(models.Manager):
    def all(self):
        return super(ProductVariationManager, self).filter(active=True)
    def sizes(self):
        return self.all().filter(category='size')
    def colors(self):
        return self.all().filter(category='color')


VAR_CATEGORIES = (
    ('size', 'size'),
    ('color', 'color'),
)

class ProductVariation(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=VAR_CATEGORIES)
    objects = ProductVariationManager()

    def __str__(self):
        return self.title
