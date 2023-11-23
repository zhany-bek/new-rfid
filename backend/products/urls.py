from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('product-list/', views.product_list, name='product-list'),
    path('reg-product', views.reg_product, name='reg-product'),
]