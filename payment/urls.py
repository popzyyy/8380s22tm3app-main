from django.urls import path, include
from . import views

app_name = 'payment'

urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('done/', views.payment_done, name='done'),
    path('canceled/', views.payment_canceled, name='canceled'),
    path('accounts/', include('allauth.urls')),
    path('registration/', include('social_django.urls', namespace="social")),
]