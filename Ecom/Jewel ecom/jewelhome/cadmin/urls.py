from django.urls import path
from . import views
from django.conf import settings
from django.urls import path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from product.models import Category

from .views import create_product

urlpatterns = [

    path(r'^media/', serve, {'document_root': settings.MEDIA_ROOT}),

    path('superuser_login/', views.superuser_login, name='superuser_login'),

    path('custom_admin/', views.custom_admin_homepage, name='custom_admin_homepage'),
  path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),

  path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('user_list/', views.user_list, name='user_list'),
     path('create_user/', views.create_user, name='create_user'),
        path('adlogout/', views.logout_view, name='adlogout'),
        path('search_users/', views.search_users, name='search_users'),
         path('product_list/', views.products_list, name='products_list'),
    
         path('create_product/', views.create_product, name='create_product'),
         path('category/<int:category_pk>/', views.category_detail, name='category_detail'),
         path('create_category/', views.create_category, name='create_category'),
          path('gold_rate_list/', views.gold_rate_list, name='gold_rate_list'),
         path('create_gold_rate/', views.create_gold_rate, name='create_gold_rate'),
         path('viewcategory/', views.viewcategory, name='viewcategory'),
         path('product/<int:product_pk>/detail/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/edit/', views.product_edit, name='product_edit'),
  
 path('product/<int:product_pk>/soft-delete/', views.soft_delete_product, name='soft_delete_product'),
    path('category/<int:category_pk>/edit/', views.edit_category, name='edit_category'),
    path('category/<int:category_pk>/soft-delete/', views.soft_delete_category, name='soft_delete_category'),
     path('product/<int:product_pk>/delete/', views.product_delete, name='product_delete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

