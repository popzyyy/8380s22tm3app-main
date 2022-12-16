from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'magictea'

urlpatterns = [
        path('', views.product_list, name='product_list'),
        path('product_list', views.product_list, name='product_list'),
        path('product_detail', views.product_detail, name='product_detail'),
        path('product/create/', views.product_new, name='product_new'),
        path('product/<int:pk>/edit/', views.product_edit, name='product_edit'),
        path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
        path('unit_list', views.unit_list, name='unit_list'),
        path('unit/create/', views.unit_new, name='unit_new'),
        path('unit/<int:pk>/edit/', views.unit_edit, name='unit_edit'),
        path('unit/<int:pk>/delete/', views.unit_delete, name='unit_delete'),
        path('category_list', views.category_list, name='category_list'),
        path('category/create/', views.category_new, name='category_new'),
        path('category/<int:pk>/edit/', views.category_edit, name='category_edit'),
        path('category/<int:pk>/delete/', views.category_delete, name='category_delete'),
        path('order_list', views.order_list, name='order_list'),
        path('order/create/', views.order_create, name='order_create'),
        path('order/<int:pk>/edit/', views.order_edit, name='order_edit'),
        path('order/<int:pk>/delete/', views.order_delete, name='order_delete'),
        path('order/<int:order_id>/pdf/', views.admin_order_pdf, name='admin_order_pdf'),
        path('cart/detail', views.cart_detail, name='cart_detail'),
        path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
        path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
        path('get_recipe', views.get_recipes, name='get_recipe'),
        path('accounts/', include('allauth.urls')),
        path('registration/', include('social_django.urls', namespace="social")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()
