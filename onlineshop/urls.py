"""onlineshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from magictea import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('payment/', include('payment.urls', namespace='payment')),
    path('user/', include('user.urls', namespace='user')),
    path('', include('magictea.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('registration/', include('social_django.urls', namespace="social")),
    path('auth/', obtain_jwt_token),
    path('orders/', views.order_details),
    url(r'^api/orders/$', views.order_details),
    url(r'^api/orders/(?P<pk>[0-9]+)$', views.getOrder),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
]
