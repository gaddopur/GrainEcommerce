from django.http import HttpResponse
from django.shortcuts import render
from products.models import Product

def home(request):
    templates = "home.html"
    products = Product.objects.all().order_by('update')
    context = {'products': products}
    return render(request, templates, context)
    
def search(request):
    try:
        q = request.GET.get('q')
    except:
        q = None
    if q:
        template="search.html"
        products = Product.objects.filter(title__icontains=q);
        context = {"products": products, "query":q }
    else:
        template = "home.html"
        products = Product.objects.all().order_by('update')
        context = {'products': products}
    return render(request, template, context)
