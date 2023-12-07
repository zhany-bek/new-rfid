from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('product-list/', views.product_list, name='product-list'),
    path('product-list/<product>', views.product_cat, name='productcat'),
    path('reg-product', views.reg_product, name='reg-product'),
    path('archive', views.archive, name='archive')
]