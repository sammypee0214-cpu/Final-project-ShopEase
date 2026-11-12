from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from products import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('api/products/', views.product_list_api, name='product_list_api'),
    path(
    'api/categories/',
    views.category_list_api,
    name='category_list_api'
),
path(
    'api/categories/<int:category_id>/',
    views.category_detail_api,
    name='category_detail_api'
),
    path(
    'api/products/<int:product_id>/',
    views.product_detail_api,
    name='product_detail_api'
),
path(
    'api/products/create/',
    views.create_product_api,
    name='create_product_api'
),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path(
    'update-cart/<int:product_id>/',
    views.update_cart,
    name='update_cart'
),
path('checkout/', views.checkout, name='checkout'),
path(
    'product/<int:product_id>/',
    views.product_detail,
    name='product_detail'
),
path(
    'register/',
    views.register,
    name='register'
),
path(
    'login/',
    views.user_login,
    name='login'
),
path('logout/', views.user_logout, name='logout'),
path(
    'api/products/<int:product_id>/update/',
    views.update_product_api,
    name='update_product_api'
),
path(
    'api/products/<int:product_id>/delete/',
    views.delete_product_api,
    name='delete_product_api'
),
path(
    'api/categories/create/',
    views.create_category_api,
    name='create_category_api'
),
path(
    'api/categories/<int:category_id>/update/',
    views.update_category_api,
    name='update_category_api'
),
path(
    'api/categories/<int:category_id>/delete/',
    views.delete_category_api,
    name='delete_category_api'
),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)