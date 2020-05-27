from django.conf.urls import url
from . import views

app_name = "carts"

urlpatterns = [
    # url(r'^$', views.carts, name = "carts"),
    url(r'^$', views.carts_views, name="carts"),
    url(r'^(?P<id>[\d]+)/$', views.remove_from_cart, name="remove_from_cart"),
    url(r'^(?P<slug>[\w-]+)/$', views.add_to_cart, name="add_to_cart"),
]
