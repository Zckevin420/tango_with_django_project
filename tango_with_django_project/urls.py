"""tango_with_django_project URL Configuration

The `urlpatterns` list routes URLs to templates. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function templates
    1. Add an import:  from my_app import templates
    2. Add a URL to urlpatterns:  path('', templates.home, name='home')
Class-based templates
    1. Add an import:  from other_app.templates import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from apptest import views
#from .views import test_db
# from tango_with_django_project.apptest import templates

urlpatterns = [
    #path('test-db/', test_db, name='test_db'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('manager/', views.manager, name='manager'),
    path('registersuccess/', views.registerSuccess, name='registersuccess'),
    path('logout/', views.logout, name="logout"),
    path('deleteuser/<userid>', views.deleteUser, name='deleteuser'),
    path('updateuser/<int:userid>/', views.updateUser, name='updateuser'),
    path('deleteitem/<int:itemid>/', views.deleteItem, name='deleteitem'),
    path('updateitem/<int:itemid>/', views.updateItem, name='updateitem'),
    path('additem/', views.additem, name='additem'),
    path('updateprofileandwallet/', views.updateProfileAndWallet, name='updateprofileandwallet'),
    path('verifypassword/', views.verifyPassword, name='verifypassword'),
    path('topup/', views.topUp, name='topup'),
    path('searchitem/', views.searchItem, name='searchitem'),
    path('addToCart/<int:itemid>/', views.addToCart, name='addtocart'),
    path('cartItems/', views.cartItems, name='cartitems'),
    # path('payCart/', views.payCart, name='paycart'),
    path('checkWallet/', views.checkWallet, name='checkwallet'),
    path('payTheBill/', views.payTheBill, name='paythebill'),
    path('addressPage/', views.addressPage, name='addresspage'),
    path('removeFromCart/<int:itemid>/', views.removeFromCart, name='removefromcart')
    # path('search/', views.search, name='search'),
    # path('login/', templates.login, name='login'),
]
