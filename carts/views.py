from django.shortcuts import render, redirect
from .models import Cart, CartItem
from products.models import Product, ProductVariation
# Create your views here.

def carts_views(request):
    try:
        the_id = request.session['cart_id']
    except:
        the_id = None
    if the_id:
        cart = Cart.objects.get(id=the_id)
        context = {'cart': cart}
    else:
        context = {'empty': True}
    templates = "carts/carts_view.html"
    return render(request, templates, context)

def remove_from_cart(request, id):
    try:
        the_id = request.session['cart_id']
    except:
        the_id = None
    if the_id:
        cart = Cart.objects.get(id=the_id)
        cart_item = CartItem.objects.get(id=id)
        cart_item.delete()
        cart.total = 0
        for item in cart.cartitem_set.all():
            cart.total += item.product.price*item.quantity
        request.session['items_count'] = cart.cartitem_set.count()
        cart.save()
    return redirect("carts:carts")

def add_to_cart(request, slug):
    request.session.set_expiry(300)
    if request.method == "POST":
        qty = int(request.POST['qty'])
        if qty > 0:
            try:
                product = Product.objects.get(slug=slug)
            except Product.DoesNotExist:
                pass
            except:
                pass
            product_var = []
            for item in request.POST:
                val = request.POST[item]
                try:
                    variation = ProductVariation.objects.get(products=product, category__iexact=item, title__iexact=val)
                    product_var.append(variation)
                except:
                    pass
            try:
                the_id = request.session['cart_id']
            except:
                new_cart = Cart()
                new_cart.save()
                request.session['cart_id'] = new_cart.id
                the_id = new_cart.id
            cart = Cart.objects.get(id=the_id)

            cart_item = CartItem.objects.create(cart=cart, product=product)
            print(product_var)
            if len(product_var) > 0:
                for vars in product_var:
                    cart_item.variation.add(vars)
            cart_item.quantity = qty
            cart_item.save()
            cart.total = 0
            for item in cart.cartitem_set.all():
                cart.total += item.product.price*item.quantity

            cart.save()
            request.session['items_count'] = cart.cartitem_set.count()
        return redirect("carts:carts")
    else:
        return redirect("carts:carts")
