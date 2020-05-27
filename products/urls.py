from django.conf.urls import url
from . import views

app_name = "products"

urlpatterns = [
    url(r'^$', views.products_list, name = "products_list"),
    url(r'^(?P<slug>[\w-]+)/$', views.product_detail, name="product_detail"),
]
