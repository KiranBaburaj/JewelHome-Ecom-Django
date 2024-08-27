from django.urls import path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from product.models import Category
from . import views
from .views import Home

urlpatterns = [path('home/', views.Home, name='home'),]

from django.urls import path
from .views import Home, register, verify_otp, resend_otp, social_login

urlpatterns = [
    path('home/', Home, name='home'),]