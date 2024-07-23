from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"), 
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('login/', views.loginPage, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logoutUser, name="logout"),
    path('order_confirmation/<str:order_id>/', views.order_confirmation, name="order_confirmation"),
    path('products_management/', views.products_management, name="products_management"),

]
