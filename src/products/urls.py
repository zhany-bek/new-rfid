from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login', views.login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('dash', views.dash, name='dashboard'),
    path('product-list/', views.product_list, name='product-list'),
    path('reg-product', views.reg_product, name='reg-product'),
]