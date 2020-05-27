from django.shortcuts import render
from .models import Product

# Create your views here.

def products_list(request):
    products = Product.objects.all().order_by('update')
    context = {'products': products}
    template = 'products/products.html'
    return render(request, template, context)

def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    context = {'product': product}
    template = "products/product_detail.html"
    return render(request, template, context)
