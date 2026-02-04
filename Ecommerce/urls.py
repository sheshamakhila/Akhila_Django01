from django.urls import path
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    path('', views.home, name='home'),

    # Cart operations
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-quantity/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='Ecommerce/login.html'), name='login'),

    # Cart and checkout views
    path('cart/', views.cart_view, name='cart_view'),
    path('checkout/', views.checkout, name='checkout'),
]
